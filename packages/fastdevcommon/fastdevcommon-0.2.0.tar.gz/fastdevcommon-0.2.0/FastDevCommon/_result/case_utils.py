import re

from pydantic import BaseModel
from pydantic.v1.datetime_parse import parse_time


class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str):
        """
        下划线形式字符串(snake_case)转换为小驼峰形式字符串(camelCase)
        :param snake_str: 下划线形式字符串
        :return: 小驼峰形式字符串
        """
        # 分割字符串
        if "_" in snake_str and not snake_str.startswith("_"):
            words = snake_str.split('_')
            # 小驼峰命名，第一个词首字母小写，其余词首字母大写
            return words[0] + ''.join(word.capitalize() for word in words[1:])
        else:
            return snake_str

    @classmethod
    def transform(cls, result):
        if result is None or isinstance(result, str) or isinstance(result, int) or isinstance(result, float):
            return result
        elif isinstance(result, list):
            return [cls.transform(row) for row in result]
        elif isinstance(result, dict):
            mapping = {}
            for k, v in result.items():
                if isinstance(v, object) and not isinstance(v, str):
                    mapping[cls.snake_to_camel(k)] = cls.transform(v)
                else:
                    mapping[cls.snake_to_camel(k)] = v
            return mapping
        elif isinstance(result, BaseModel):
            mapping = {}
            for k, v in result.model_dump().items():
                if isinstance(v, object) and not isinstance(v, str):
                    mapping[cls.snake_to_camel(k)] = cls.transform(v)
                else:
                    mapping[cls.snake_to_camel(k)] = v
            return mapping
        elif isinstance(result, object) and not isinstance(result, str) and hasattr(result, "__dict__"):
            mapping = {}
            for key, val in vars(result).items():
                if isinstance(val, object):
                    mapping[cls.snake_to_camel(key)] = cls.transform(val)
                else:
                    mapping[cls.snake_to_camel(key)] = val
            return mapping
        else:
            return result


class SnakeCaseUtil:
    @classmethod
    def camel_to_snake(cls, camel_str):
        """
        小驼峰形式字符串(camelCase)转换为下划线形式字符串(snake_case)
        :param camel_str: 小驼峰形式字符串
        :return: 下划线形式字符串
        """
        # 在大写字母前添加一个下划线，然后将整个字符串转为小写
        if not camel_str.startswith("_"):
            words = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', words).lower()
        else:
            return camel_str

    @classmethod
    def transform(cls, result):
        if result is None or isinstance(result, str) or isinstance(result, int) or isinstance(result, float):
            return result
        elif isinstance(result, list):
            return [cls.transform(row) for row in result]
        elif isinstance(result, dict):
            mapping = {}
            for k, v in result.items():
                if isinstance(v, object) and not isinstance(v, str):
                    mapping[cls.camel_to_snake(k)] = cls.transform(v)
                else:
                    mapping[cls.camel_to_snake(k)] = v
            return mapping
        elif isinstance(result, object) and not isinstance(result, str):
            mapping = {}
            for key, val in vars(result).items():
                if isinstance(val, object):
                    mapping[cls.camel_to_snake(key)] = cls.transform(val)
                else:
                    mapping[cls.camel_to_snake(key)] = val
            return mapping
        else:
            return result
