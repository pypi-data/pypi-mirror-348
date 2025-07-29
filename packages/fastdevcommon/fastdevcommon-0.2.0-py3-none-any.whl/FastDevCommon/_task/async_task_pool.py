import asyncio
from typing import Callable, Dict, List, Any, Coroutine, Optional, Union
import uuid
from enum import Enum
import time

from .._logger import logger

# 配置日志
class TaskStatus(Enum):
    PENDING = "pending"    # 等待执行
    RUNNING = "running"    # 正在执行
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"      # 执行失败
    CANCELLED = "cancelled"  # 任务被取消

class Task:
    """任务类，用于封装异步任务"""
    
    def __init__(self, coro_func: Callable[[], Coroutine], task_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        self.coro_func = coro_func
        self.task_id = task_id or str(uuid.uuid4())
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self._task: Optional[asyncio.Task] = None
        self._processing = False  # 标记任务是否正在被处理
        self.created_at = time.time()  # 任务创建时间
        self.started_at = None  # 任务开始执行时间
        self.completed_at = None  # 任务完成时间
        self.metadata = metadata or {}  # 任务元数据，可用于存储任务相关信息
        
        # 计算任务指纹，用于去重
        self.fingerprint = self._calculate_fingerprint()
    
    def _calculate_fingerprint(self) -> str:
        """计算任务指纹，用于去重"""
        # 这里使用简单的方法，实际应用中可能需要更复杂的逻辑
        # 注意：这里只是示例，实际应用中需要根据具体情况调整
        return f"{id(self.coro_func)}_{str(self.metadata)}"
    
    def __str__(self):
        return f"Task(id={self.task_id}, status={self.status.value})"

class AsyncTaskPool:
    """异步任务池，用于管理和执行异步任务"""
    
    def __init__(self, max_workers: int = 10, enable_deduplication: bool = True):
        """
        初始化异步任务池
        
        Args:
            max_workers: 最大并发工作数量
            enable_deduplication: 是否启用任务去重
        """
        self.max_workers = max_workers
        self.tasks: Dict[str, Task] = {}
        self.task_fingerprints: Dict[str, str] = {}  # 任务指纹到任务ID的映射
        self.semaphore = asyncio.Semaphore(max_workers)
        self._running = False
        self._worker_task = None
        self._lock = asyncio.Lock()  # 添加锁以保护任务状态更新
        self.enable_deduplication = enable_deduplication
        self.task_execution_count = 0  # 任务执行计数器
    
    async def submit(self, coro_func: Callable[[], Coroutine], task_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        提交一个异步任务到池中
        
        Args:
            coro_func: 返回协程的函数
            task_id: 任务ID，如果不提供则自动生成
            metadata: 任务元数据，可用于存储任务相关信息
            
        Returns:
            任务ID
        """
        task = Task(coro_func, task_id, metadata)
        
        # 如果启用了去重，检查是否有相同的任务
        if self.enable_deduplication:
            async with self._lock:
                existing_task_id = self.task_fingerprints.get(task.fingerprint)
                if existing_task_id and existing_task_id in self.tasks:
                    logger.info(f"发现重复任务，返回已存在的任务ID: {existing_task_id}")
                    return existing_task_id
        
        async with self._lock:
            self.tasks[task.task_id] = task
            if self.enable_deduplication:
                self.task_fingerprints[task.fingerprint] = task.task_id
            logger.info(f"任务已提交: {task}, 元数据: {task.metadata}")
        
        # 如果工作器未运行，则启动它
        if not self._running:
            self.start()
            
        return task.task_id
    
    def start(self):
        """启动任务池工作器"""
        if not self._running:
            self._running = True
            self._worker_task = asyncio.create_task(self._worker())
            logger.info("任务池工作器已启动")
    
    async def stop(self, wait_for_completion: bool = True):
        """
        停止任务池
        
        Args:
            wait_for_completion: 是否等待所有任务完成
        """
        if not self._running:
            return
            
        self._running = False
        
        if wait_for_completion:
            # 等待所有任务完成
            async with self._lock:
                pending_tasks = [task._task for task in self.tasks.values() 
                                if task._task and not task._task.done()]
            
            if pending_tasks:
                logger.info(f"等待 {len(pending_tasks)} 个任务完成...")
                await asyncio.gather(*pending_tasks, return_exceptions=True)
        else:
            # 取消所有正在运行的任务
            tasks_to_cancel = []
            async with self._lock:
                for task_id, task in list(self.tasks.items()):
                    if task._task and not task._task.done():
                        tasks_to_cancel.append((task_id, task))
            
            for task_id, task in tasks_to_cancel:
                if task._task and not task._task.done():
                    task._task.cancel()
                    task.status = TaskStatus.CANCELLED
                    logger.info(f"任务已取消: {task}")
                
                async with self._lock:
                    # 从任务池中移除所有任务
                    self._remove_task(task_id)
        
        # 取消工作器任务
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"任务池已停止，共执行了 {self.task_execution_count} 个任务")
    
    def _remove_task(self, task_id: str):
        """
        从任务池中移除任务
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            # 如果启用了去重，也从指纹映射中移除
            if self.enable_deduplication and task.fingerprint in self.task_fingerprints:
                if self.task_fingerprints[task.fingerprint] == task_id:
                    self.task_fingerprints.pop(task.fingerprint, None)
            
            self.tasks.pop(task_id, None)
    
    async def _worker(self):
        """工作器协程，负责执行任务池中的任务"""
        while self._running:
            # 查找待处理的任务
            pending_tasks = []
            async with self._lock:
                # 按创建时间排序，先处理先提交的任务
                sorted_tasks = sorted(
                    list(self.tasks.values()),
                    key=lambda t: t.created_at
                )
                
                for task in sorted_tasks:
                    if task.status == TaskStatus.PENDING and not task._processing:
                        task._processing = True  # 标记任务正在被处理
                        pending_tasks.append(task)
                        # 限制每次处理的任务数量，避免一次处理太多任务
                        if len(pending_tasks) >= self.max_workers:
                            break
            
            if not pending_tasks:
                # 如果没有待处理的任务，等待一小段时间
                await asyncio.sleep(0.1)
                continue
            
            # 为每个待处理的任务创建执行任务
            for task in pending_tasks:
                asyncio.create_task(self._execute_task(task))
            
            # 短暂等待，避免CPU过度使用
            await asyncio.sleep(0.05)
    
    async def _execute_task(self, task: Task):
        """
        执行单个任务
        
        Args:
            task: 要执行的任务
        """
        execution_id = self.task_execution_count + 1
        self.task_execution_count = execution_id
        
        try:
            # 检查任务是否仍在任务池中
            async with self._lock:
                if task.task_id not in self.tasks:
                    logger.warning(f"任务不在池中，跳过执行: {task.task_id} (执行ID: {execution_id})")
                    return
                
                # 更新任务状态
                task.status = TaskStatus.RUNNING
                task.started_at = time.time()
            
            logger.info(f"开始执行任务: {task} (执行ID: {execution_id})")
            
            # 使用信号量控制并发数
            async with self.semaphore:
                try:
                    # 调用函数获取新的协程对象
                    coro = task.coro_func()
                    # 创建asyncio任务
                    task._task = asyncio.create_task(coro)
                    
                    # 等待任务完成
                    task.result = await task._task
                    task.completed_at = time.time()
                    
                    async with self._lock:
                        if task.task_id in self.tasks:  # 再次检查任务是否仍在池中
                            task.status = TaskStatus.COMPLETED
                            logger.info(f"任务完成: {task} (执行ID: {execution_id}), 耗时: {task.completed_at - task.started_at:.2f}秒")
                except asyncio.CancelledError:
                    # 处理任务被取消的情况
                    task.completed_at = time.time()
                    async with self._lock:
                        if task.task_id in self.tasks:
                            task.status = TaskStatus.CANCELLED
                            logger.info(f"任务被取消: {task} (执行ID: {execution_id}), 耗时: {task.completed_at - task.started_at:.2f}秒")
                except Exception as e:
                    # 处理任务执行过程中的异常
                    task.completed_at = time.time()
                    async with self._lock:
                        if task.task_id in self.tasks:
                            task.error = e
                            task.status = TaskStatus.FAILED
                            logger.error(f"任务执行失败: {task} (执行ID: {execution_id}), 错误: {str(e)}, 耗时: {task.completed_at - task.started_at:.2f}秒")
        finally:
            # 从任务池中移除已完成、失败或取消的任务
            async with self._lock:
                if task.task_id in self.tasks:
                    self._remove_task(task.task_id)
                    logger.info(f"任务已从池中移除: {task.task_id} (执行ID: {execution_id})")
                else:
                    logger.warning(f"任务已不在池中，无需移除: {task.task_id} (执行ID: {execution_id})")
                
                # 无论如何，重置处理标志
                task._processing = False
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态，如果任务不存在则返回None
        """
        task = self.tasks.get(task_id)
        return task.status if task else None
    
    def get_task_result(self, task_id: str) -> Optional[Any]:
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务结果，如果任务不存在或未完成则返回None
        """
        task = self.tasks.get(task_id)
        if task and task.status == TaskStatus.COMPLETED:
            return task.result
        return None
    
    def get_task_error(self, task_id: str) -> Optional[Exception]:
        """
        获取任务错误
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务错误，如果任务不存在或未失败则返回None
        """
        task = self.tasks.get(task_id)
        if task and task.status == TaskStatus.FAILED:
            return task.error
        return None
    
    def get_pending_count(self) -> int:
        """获取待处理任务数量"""
        return len([task for task in self.tasks.values() if task.status == TaskStatus.PENDING])
    
    def get_running_count(self) -> int:
        """获取正在运行的任务数量"""
        return len([task for task in self.tasks.values() if task.status == TaskStatus.RUNNING])
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """获取所有任务的信息"""
        return [
            {
                "task_id": task.task_id,
                "status": task.status.value,
                "has_result": task.result is not None,
                "has_error": task.error is not None,
                "created_at": task.created_at,
                "started_at": task.started_at,
                "completed_at": task.completed_at,
                "metadata": task.metadata
            }
            for task in self.tasks.values()
        ]