from .operate_enum import OperateCode, MessageEnum
from pydantic import BaseModel

class OperateResult:
    """操作，业务等统一返回"""

    def __init__(self, code=OperateCode.SUCCESS.value, message: str | MessageEnum|None = "success", data=None):
        """
        code 状态码
        message 消息
        data 数据
        camel 是否启用驼峰
        """
        if isinstance(code, OperateCode):
            self.code = code  # 确保code初始化为枚举的值
        elif isinstance(code, int):
            self.code = code
        else:
            raise TypeError("code must be OperateCode or int")
        if isinstance(message, MessageEnum):
            self.msg = message.value
        else:
            self.msg = message
        if isinstance(data, BaseModel):
            data = data.model_dump(by_alias=True)
        self.data = data

    @classmethod
    def success(cls, message: str | MessageEnum = "success", data=None):
        """success"""
        return cls(code=200, message=message, data=data)

    @classmethod
    def warning(cls, message: str | MessageEnum, data=None):
        """warning"""
        return cls(code=400, message=message, data=data)

    @classmethod
    def error(cls, message: str | MessageEnum, data=None):
        """error"""
        return cls(code=OperateCode.ERROR.value, message=message, data=data)


    @classmethod
    def unauthorized(cls, message: str | MessageEnum, data=None):
        """not authorized"""
        return cls(code=OperateCode.UNAUTHORIZED.value, message=message, data=data)
    @classmethod
    def denied(cls, message: str | MessageEnum, data=None):
        """denied"""
        return cls(code=OperateCode.DENIED.value, message=message, data=data)

    @classmethod
    def from_dict(cls, input_dict: dict):
        """从一个字典（json）转成OperateResult"""

        return cls(
            code=input_dict.get("code", 400),
            message=input_dict.get("message", "fail"),
            data=input_dict.get("data", None),
        )

    def dumps(self):
        body = {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
        return body
