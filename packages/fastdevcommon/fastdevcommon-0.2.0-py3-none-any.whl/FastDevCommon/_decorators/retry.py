import time
from functools import wraps
import asyncio


def SyncMaxRetry(exceptions=(Exception,), tries=3, delay=3, backoff=2):
    """
    装饰器：在遇到指定异常时重试函数。

    参数:
    exceptions: 可以触发重试的异常类型。
    tries: 最大重试次数。
    delay: 每次重试之间的延迟秒数。
    backoff: 延迟时间的倍增因子，用于实现指数退避策略。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ntries, ndelay = tries, delay
            while ntries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    time.sleep(ndelay)
                    ntries -= 1
                    ndelay *= backoff
                    print(f"重试中... 剩余重试次数: {ntries}, 下次重试延迟: {ndelay}秒,失败原因:{e}")
            return func(*args, **kwargs)  # 最后一次尝试

        return wrapper

    return decorator


def AsyncMaxRetry(exceptions=(Exception,), tries=3, delay=3, backoff=2):
    """
    装饰器：在遇到指定异常时异步重试函数。

    参数:
    exceptions: 可以触发重试的异常类型。
    tries: 最大重试次数。
    delay: 每次重试之间的延迟秒数。
    backoff: 延迟时间的倍增因子，用于实现指数退避策略。
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            ntries, ndelay = tries, delay
            while ntries > 1:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    await asyncio.sleep(ndelay)
                    ntries -= 1
                    ndelay *= backoff
                    print(f"重试中... 剩余重试次数: {ntries}, 下次重试延迟: {ndelay}秒, 失败原因: {e}")
            return await func(*args, **kwargs)  # 最后一次尝试

        return wrapper

    return decorator
