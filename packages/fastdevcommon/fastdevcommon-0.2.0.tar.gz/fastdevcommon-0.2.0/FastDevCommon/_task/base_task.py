import asyncio
import datetime
from abc import ABC, abstractmethod
from typing import List, Any

from .._logger import logger
from ..utils import AsyncSnowflakeIdGenerator

from .async_task_pool import AsyncTaskPool


class BaseTask(ABC):
    def __init__(self, sleep_time=5):
        self.task_pool:AsyncTaskPool|None = None
        self.loop = None
        self.sleep_time = sleep_time

    @abstractmethod
    async def fetch_generate_task(self, top_k=50) -> List[Any]:
        """
        获取任务的方式
        :return:
        """
        pass

    @abstractmethod
    async def process_generate_task(self, task: Any) -> Any:
        """
        处理任务
        :return:
        """
        pass

    async def before(self):
        """
        执行任务前的操作
        :return:
        """
        pass

    def get_or_new_loop(self):
        """
        获取当前的时间循环
        :return:
        """
        try:
            self.loop = asyncio.get_running_loop()  # 尝试获取当前正在运行的事件循环
        except RuntimeError:
            self.loop = asyncio.new_event_loop()  # 如果获取失败，说明没有正在运行的，就创建一个新的
            asyncio.set_event_loop(self.loop)
        return self.loop

    async def run(self):
        while True:
            try:
                tasks = await self.fetch_generate_task()
                if tasks:
                    for task in tasks:
                        task_id = task.get("task_id",None)
                        if not task_id:
                            task_id = await AsyncSnowflakeIdGenerator().generate_id()
                        await self.task_pool.submit(lambda: self.process_generate_task(task),task_id=task_id,metadata=task)
                        await asyncio.sleep(0.2)
                else:
                    await asyncio.sleep(self.sleep_time)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(e)
                await asyncio.sleep(self.sleep_time)

    def start(self):
        """
        循环遍历任务
        :return:
        """
        self.loop = self.get_or_new_loop()
        self.loop.run_until_complete(self.before())
        if not self.task_pool:
            self.task_pool = AsyncTaskPool(max_workers=10,enable_deduplication=True)
        self.loop.run_until_complete(self.run())

    @classmethod
    def generate_image_store_key(cls, task_id, index=None, format_str: str = ".png"):
        current_date = datetime.datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        oss_key = f"static/task/{formatted_date}/{task_id}{'/' + str(index) + format_str if index or index == 0 else format_str}"
        return oss_key



