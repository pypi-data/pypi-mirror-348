from enum import Enum


class MessageEnum(Enum):
    NOT_CREATE_TASK_ERROR = "任务创建失败"


class OperateCode(Enum):
    """返回code枚举"""

    SUCCESS = 200  # 成功
    WARNING = 400  # 友好提示
    DENIED = 403  # 拒绝访问
    ERROR = 500  # 应用错误
    UNAUTHORIZED = 401  # 登录过期
