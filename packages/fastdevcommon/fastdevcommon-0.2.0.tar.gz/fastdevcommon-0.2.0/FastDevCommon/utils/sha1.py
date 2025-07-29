import hashlib
import hmac


class SHAUtil:
    """
    SHA 工具类
    """

    @classmethod
    def sha1_encrypt(cls, message: str | bytes):
        """
        sha1加密
        :param message: 字符串
        :return:
        """
        if not isinstance(message, bytes):
            message = str(message).encode('utf - 8')
        sha1_hash = hashlib.sha1()
        sha1_hash.update(message)
        return sha1_hash.hexdigest()

    @classmethod
    def hmac_sha1(cls, key, code):
        hmac_code = hmac.new(key.encode(), code.encode(), hashlib.sha1)
        return hmac_code.digest()
