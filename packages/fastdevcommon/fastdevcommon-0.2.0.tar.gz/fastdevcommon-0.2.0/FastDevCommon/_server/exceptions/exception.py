"""自定义异常类，用来替换原来的HTTPException"""
from typing import Any, Dict, Optional
from typing_extensions import Annotated, Doc
import http


class HTTPException(Exception):
    def __init__(
            self,
            status_code: int,
            detail: str | None = None,
            headers: dict[str, str] | None = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


class CustomException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    '''获取异常信息，将其格式化后返回'''

    def get_message(self):
        res = {
            "code": self.code,
            "message": self.message
        }
        return res


class CodeException(HTTPException):

    def __init__(
            self,
            status_code: Annotated[
                int,
                Doc(
                    """
                    HTTP status code to send to the client.
                    """
                ),
            ],
            msg: Annotated[
                Any,
                Doc(
                    """
                    Any data to be sent to the client in the `detail` key of the JSON
                    response.
                    """
                ),
            ] = None,
            headers: Annotated[
                Optional[Dict[str, str]],
                Doc(
                    """
                    Any headers to send to the client in the response.
                    """
                ),
            ] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=msg, headers=headers)
