from typing import Any

from pydantic import BaseModel, Field


# 自定义类型转换函数，用于判断并转换长整型为字符串
def bigint_to_str(value):
    if isinstance(value, int) and abs(value) > 100000000:  # 参考JavaScript中Number类型的最大安全整数
        return str(value)
    return value


class BaseDTO(BaseModel):
    class Config:
        populate_by_name = True
        json_encoders = {
            int: bigint_to_str
        }


class PageDTO(BaseDTO):
    total_count: int = Field(default=0, alias="totalCount")
    list: Any = Field(default=0, alias="list")