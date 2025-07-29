import codecs
import json
import re
import traceback
from json import JSONDecodeError

from .._decorators import AsyncMaxRetry
from .._logger import logger
import aiohttp


class RequestException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request.
    """

    def __init__(self, *args, **kwargs):
        """Initialize RequestException with `request` and `response` objects."""
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = self.response.request
        super().__init__(*args, **kwargs)


class HTTPError(RequestException):
    """An HTTP error occurred."""


_null = "\x00".encode("ascii")  # encoding to ASCII for Python 3
_null2 = _null * 2
_null3 = _null * 3


def guess_json_utf(data):
    """
    :rtype: str
    """
    # JSON always starts with two ASCII characters, so detection is as
    # easy as counting the nulls and from their location and count
    # determine the encoding. Also detect a BOM, if present.
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        return "utf-32"  # BOM included
    if sample[:3] == codecs.BOM_UTF8:
        return "utf-8-sig"  # BOM included, MS style (discouraged)
    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return "utf-16"  # BOM included
    nullcount = sample.count(_null)
    if nullcount == 0:
        return "utf-8"
    if nullcount == 2:
        if sample[::2] == _null2:  # 1st and 3rd are null
            return "utf-16-be"
        if sample[1::2] == _null2:  # 2nd and 4th are null
            return "utf-16-le"
        # Did not detect 2 valid UTF-16 ascii-range characters
    if nullcount == 3:
        if sample[:3] == _null3:
            return "utf-32-be"
        if sample[1:] == _null3:
            return "utf-32-le"
        # Did not detect a valid UTF-32 ascii-range character
    return None


def parse_header_links(value):
    """Return a list of parsed link headers proxies.

    i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"

    :rtype: list
    """

    links = []

    replace_chars = " '\""

    value = value.strip(replace_chars)
    if not value:
        return links

    for val in re.split(", *<", value):
        try:
            url, params = val.split(";", 1)
        except ValueError:
            url, params = val, ""

        link = {"url": url.strip("<> '\"")}

        for param in params.split(";"):
            try:
                key, value = param.split("=")
            except ValueError:
                break

            link[key.strip(replace_chars)] = value.strip(replace_chars)

        links.append(link)

    return links


class Response:
    """The :class:`Response <Response>` object, which contains a
    server's response to an HTTP request.
    """

    __attrs__ = [
        "status_code",
        "headers",
        "url",
        "encoding",
        "cookies",
        "request",
    ]

    def __init__(self, status_code, headers, url, content, reason: str = ""):
        self._content = content
        self.status_code = status_code
        self.headers = headers
        self.url = url
        self.reason = reason
        self.encoding = "utf-8"

    def raise_for_status(self):
        """Raises :class:`HTTPError`, if one occurred."""
        http_error_msg = ""

        if 400 <= self.status_code < 500:
            http_error_msg = (
                f"{self.status_code} Client Error: {self.reason} for url: {self.url}"
            )

        elif 500 <= self.status_code < 600:
            http_error_msg = (
                f"{self.status_code} Server Error: {self.reason} for url: {self.url}"
            )

        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)

    @property
    def text(self):
        """Content of the response, in unicode.

        If Response.encoding is None, encoding will be guessed using
        ``charset_normalizer`` or ``chardet``.

        The encoding of the response content is determined based solely on HTTP
        headers, following RFC 2616 to the letter. If you can take advantage of
        non-HTTP knowledge to make a better guess at the encoding, you should
        set ``r.encoding`` appropriately before accessing this property.
        """

        # Try charset from content-type
        encoding = self.encoding

        if not self.content:
            return ""

        # Fallback to auto-detected encoding.
        if self.encoding is None:
            encoding = "utf-8"

        # Decode unicode from given encoding.
        try:
            content = str(self.content, encoding, errors="replace")
        except (LookupError, TypeError):
            # A LookupError is raised if the encoding was not found which could
            # indicate a misspelling or similar mistake.
            #
            # A TypeError can be raised if encoding is None
            #
            # So we try blindly encoding.
            content = str(self.content, errors="replace")

        return content

    def json(self, **kwargs):
        r"""Returns the json-encoded content of a response, if any.

        :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
        :raises requests.exceptions.JSONDecodeError: If the response body does not
            contain valid json.
        """

        if not self.encoding and self.content and len(self.content) > 3:
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return json.loads(self.content.decode(encoding), **kwargs)
                except UnicodeDecodeError:
                    # Wrong UTF codec detected; usually because it's not UTF-8
                    # but some other 8-bit codec.  This is an RFC violation,
                    # and the server didn't bother to tell us what codec *was*
                    # used.
                    pass
                except JSONDecodeError as e:
                    raise ValueError(e.msg, e.doc, e.pos)

        try:
            return json.loads(self.text, **kwargs)
        except JSONDecodeError as e:
            # Catch JSON-related errors and raise as requests.JSONDecodeError
            # This aliases json.JSONDecodeError and simplejson.JSONDecodeError
            raise ValueError(e.msg, e.doc, e.pos)

    @property
    def ok(self):
        """Returns True if :attr:`status_code` is less than 400, False if not.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        try:
            self.raise_for_status()
        except HTTPError:
            return False
        return True

    @property
    def is_redirect(self):
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """
        REDIRECT_STATI = (
            301,  # 301
            302,  # 302
            303,  # 303
            307,  # 307
            308,  # 308
        )
        return "location" in self.headers and self.status_code in REDIRECT_STATI

    @property
    def content(self):
        return self._content

    @property
    def links(self):
        """Returns the parsed header links of the response, if any."""

        header = self.headers.get("link")

        resolved_links = {}

        if header:
            links = parse_header_links(header)

            for link in links:
                key = link.get("rel") or link.get("url")
                resolved_links[key] = link

        return resolved_links

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    def __bool__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __nonzero__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __enter__(self):
        return self


class HttpClient:
    @classmethod
    async def get(cls, url, timeout=30, headers=None, **kwargs) -> Response:
        return await cls.request(url, method="GET", timeout=timeout, headers=headers, **kwargs)

    @classmethod
    async def post(cls, url, timeout=30, headers=None, **kwargs) -> Response:
        return await cls.request(url, method="POST", timeout=timeout, headers=headers, **kwargs)
    @classmethod
    async def put(cls, url, timeout=30, headers=None, **kwargs) -> Response:
        return await cls.request(url, method="PUT", timeout=timeout, headers=headers, **kwargs)

    @classmethod
    async def request(cls, url, method, timeout=30, headers=None, **kwargs) -> Response:
        session = Session()
        response = await session.request(url=url, method=method, timeout=timeout, headers=headers, **kwargs)
        return response

    @classmethod
    def session(cls):
        return Session()
    @classmethod
    async def delete(cls, url, timeout=30, headers=None, **kwargs):
        return await cls.request(url, method="DELETE", timeout=timeout, headers=headers, **kwargs)


class Session:
    def __init__(self):
        self.headers = {}
        self.cookies = {}

    async def get(self, url, timeout=30, headers=None, **kwargs) -> Response:
        return await self.request(url, method="GET", timeout=timeout, headers=headers, **kwargs)

    async def post(self, url, timeout=30, headers=None, **kwargs) -> Response:
        return await self.request(url, method="POST", timeout=timeout, headers=headers, **kwargs)

    @AsyncMaxRetry()
    async def request(self, url, method, timeout=30, headers=None, **kwargs) -> Response | None:
        try:
            headers = headers or {}
            headers.update(self.headers)
            headers = {k: str(v) if v is None else v for k, v in headers.items() if isinstance(k, str)}
            headers[
                "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout), headers=headers) as session:
                async with session.request(url=url, method=method, cookies=self.cookies,
                                           **kwargs) as res:
                    self.cookies = dict(res.cookies)
                    logger.log("发起请求", url, method, res.status)
                    response = Response(status_code=res.status, headers=res.headers, url=res.url,
                                        content=await res.read(),
                                        reason=res.reason)
                    return response
        except Exception as e:
            logger.error(e, traceback.format_exc())
        return None
