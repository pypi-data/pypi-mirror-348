"""
一些不方便归集在字符串操作，字典操作等的帮助类
"""
import hashlib
import random
import re
import socket
import string
from typing import Literal
from urllib.parse import urlparse


def select_by_weight(input_data, weight_key='weight'):
    """
    根据权重对应的概率分布从输入数据中随机选择一个元素返回。

    该函数主要用于处理包含字典元素的集合（如列表），通过每个元素中特定的权重键对应的值，
    计算其概率分布，然后基于该概率分布随机选择一个元素并返回。

    :param input_data: 包含字典元素的集合（如列表），字典中应包含权重相关键值对，且不能为空，
                       要求集合中的所有字典元素结构一致，都包含由 `weight_key` 指定的权重键。
    :param weight_key: 权重对应的键名，用于提取每个元素的权重值，该键必须存在于 `input_data` 集合内的字典元素中。默认：weight
    :return: 按照权重概率分布随机选择的一个元素（字典类型）
    :raises TypeError: 如果 `input_data` 不是列表类型或者 `weight_key` 不是合法的字符串类型。
    :raises ValueError: 如果 `input_data` 为空列表或者 `weight_key` 不存在于 `input_data` 中字典元素内。
    """
    selected_item = None
    # 检查输入的input_data是否为列表类型
    if not isinstance(input_data, list):
        raise TypeError("input_data must be a list.")

    # 检查输入的input_data是否为空列表
    if not input_data:
        raise ValueError("input_data cannot be empty.")

    # 检查weight_key是否为字符串类型，通常权重键名应为字符串表示
    if not isinstance(weight_key, str):
        raise TypeError("weight_key must be a string.")

    # 检查weight_key是否存在于input_data中第一个字典元素内（假设集合内字典结构一致）
    if weight_key not in input_data[0]:
        raise ValueError(f"{weight_key} does not exist in the elements of input_data.")

    # 计算每个元素对应的概率
    probabilities = []
    total_weight = sum(item[weight_key] for item in input_data)
    for item in input_data:
        probabilities.append(item[weight_key] / total_weight)

    # 生成一个0到1之间的随机数
    random_prob = random.random()

    # 根据概率区间选择元素
    cumulative_prob = 0
    for i in range(len(input_data)):
        cumulative_prob += probabilities[i]
        if random_prob < cumulative_prob:
            selected_item = input_data[i]
            break

    return selected_item


def clean_midjourney_prompt(prompt):
    """
    获取提示词文本不包含指令
    """
    instructions = {}
    if "--" in prompt:
        clean_prompt_str = prompt.split("--")[0].strip()
        for item in prompt.split("--")[1:]:
            parts = item.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                instructions[key] = value
    else:
        clean_prompt_str = prompt
    return clean_prompt_str, instructions


def generate_random_string(
        length: int,
        string_type: Literal[
            "letters", "digits", "alphanumeric", "special"
        ] = "alphanumeric",
) -> str:
    """
    生成指定长度和类型的随机字符串。

    Args:
        length (int): 要生成的字符串的长度。
        string_type (Literal['letters', 'digits', 'alphanumeric', 'special']): 字符串的类型，定义生成的字符串包含的字符集:
            'letters' - 只包含字母。
            'digits' - 只包含数字。
            'alphanumeric' - 包含字母和数字。
            'special' - 包含字母、数字和特殊字符。

    Returns:
        str: 生成的随机字符串。

    Examples:
        >>> generate_random_string(10, 'letters')
        'eAdBcFgHiJ'
        >>> generate_random_string(10, 'digits')
        '1234567890'
        >>> generate_random_string(10, 'alphanumeric')
        '1a2B3c4D5e'
        >>> generate_random_string(10, 'special')
        '1a#2B$c%4^'
    """
    # 字符集选择
    character_sets = {
        "letters": string.ascii_letters,
        "digits": string.digits,
        "alphanumeric": string.ascii_letters + string.digits,
        "special": string.ascii_letters + string.digits + string.punctuation,
    }

    # 根据string_type选择相应的字符集
    characters = character_sets[string_type]  # 使用字典直接访问

    # 生成随机字符串
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


def is_chinese_sentence(sentence):
    """
    判断是否存在中文
    """
    pattern = re.compile("[^\u4e00-\u9fa5]")
    filtered_text = pattern.sub("", sentence)
    return bool(filtered_text)


def process_image_resize(image_url, length):
    if not image_url or not image_url.startswith('http'):
        return image_url
    if "?" in image_url:
        image_url = image_url.split("?")[0]
    image_url = image_url + f"?imageMogr2/thumbnail/!{length}x{length}r"
    return image_url


def replace_value_in_dict(target_dict, target_key, new_value):
    """
    在字典中查找并替换指定键对应的的值（支持多层嵌套字典）
    :rtype: object
    :param target_dict: 要操作的目标字典
    :param target_key: 需要替换值的目标键
    :param new_value: 要替换成的新值
    :return: 替换后的字典（原字典会被修改）
    """
    for key, value in target_dict.items():
        if key == target_key:
            target_dict[key] = new_value
        elif isinstance(value, dict):
            replace_value_in_dict(value, target_key, new_value)
        elif isinstance(value, list):
            for element in value:
                if isinstance(element, dict):
                    replace_value_in_dict(element, target_key, new_value)
    return target_dict


def md5_encrypt_string(input_string):
    # 创建 MD5 对象
    md5 = hashlib.md5()
    # 将输入字符串编码为字节类型
    input_bytes = input_string.encode('utf-8')
    # 更新 MD5 对象的内容
    md5.update(input_bytes)
    # 获取加密后的十六进制字符串
    encrypted_string = md5.hexdigest()
    return encrypted_string


def parse_url_object_key(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    if path.startswith("/"):
        path = path[1:]
    return path


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'