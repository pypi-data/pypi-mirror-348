import asyncio
import concurrent
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Callable, Any

from v2.nacos import Instance, Service, ServiceList

from .client_config import NacosClientConfig
from .async_client import AsyncNacosClient
from .interfaces import NacosClientInterface
from ..._logger import logger


class SyncNacosClient(NacosClientInterface):
    """同步Nacos客户端，支持服务发现和配置管理"""

    def list_services(self, **kwargs) -> Any:
        pass

    def __init__(self, config: Optional[NacosClientConfig] = None, **kwargs):
        """
        初始化同步Nacos客户端
        
        Args:
            config: Nacos客户端配置，如果为None则使用kwargs创建
            **kwargs: 如果config为None，则使用这些参数创建配置
        """
        self.config = config or NacosClientConfig(**kwargs)
        self._async_client = AsyncNacosClient(self.config)
        self._executor = ThreadPoolExecutor(max_workers=10)
        self._loop = None
        self._lock = threading.Lock()
        self._closed = False
    
    def _get_event_loop(self):
        """获取事件循环"""
        if self._loop is None:
            with self._lock:
                if self._loop is None:
                    try:
                        self._loop = asyncio.get_event_loop()
                    except RuntimeError:
                        self._loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(self._loop)
        return self._loop
    
    def _run_coroutine(self, coro):
        """运行协程并返回结果"""
        if self._closed:
            raise RuntimeError("Client is closed")
            
        loop = self._get_event_loop()
        if loop.is_running():
            # 如果事件循环正在运行，使用线程池执行
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            try:
                # 添加超时处理
                return future.result(timeout=self.config.grpc_timeout / 1000 + 1)
            except concurrent.futures.TimeoutError:
                future.cancel()
                raise TimeoutError(f"Operation timed out after {self.config.grpc_timeout / 1000} seconds")
        else:
            # 否则直接运行
            return loop.run_until_complete(coro)
    
    # =============== 服务发现相关方法 ===============
    
    def register_instance(self, **kwargs) -> bool:
        """注册服务实例"""
        return self._run_coroutine(self._async_client.register_instance(**kwargs))
    
    def deregister_instance(self, **kwargs) -> bool:
        """注销服务实例"""
        return self._run_coroutine(self._async_client.deregister_instance(**kwargs))
    def list_services(self, **kwargs) -> Any:
        """
        获取服务列表
        
        Args:
            **kwargs: 参数，如 page_no, page_size, group_name, namespace_id 等
            
        Returns:
            ServiceList: 服务列表
        """
        return self._run_coroutine(self._async_client.list_services(**kwargs))
    def list_instances(self, service_name, **kwargs) -> List[Instance]:
        """
        获取服务实例列表
        
        Args:
            service_name: 服务名称
            **kwargs: 其他参数，如 group_name, clusters, healthy_only 等
        """
        return self._run_coroutine(self._async_client.list_instances(service_name, **kwargs))
    
    def subscribe(self, service_name, **kwargs) -> None:
        """
        订阅服务变更
        
        Args:
            service_name: 服务名称
            **kwargs: 其他参数，如 group_name, clusters, callback_func 等
        """
        # 对于回调函数，需要包装一下，确保在正确的线程中执行
        callback_func = kwargs.get('callback_func')
        if callback_func:
            async def async_callback(service):
                loop = self._get_event_loop()
                await loop.run_in_executor(self._executor, callback_func, service)
            
            kwargs['callback_func'] = async_callback
            
        self._run_coroutine(self._async_client.subscribe(service_name, **kwargs))
    
    def unsubscribe(self, service_name, **kwargs) -> None:
        """
        取消订阅服务变更
        
        Args:
            service_name: 服务名称
            **kwargs: 其他参数，如 group_name, clusters 等
        """
        self._run_coroutine(self._async_client.unsubscribe(service_name, **kwargs))
    
    # =============== 配置管理相关方法 ===============
    
    def get_config(self, data_id, group=None, **kwargs) -> str:
        """
        获取配置
        
        Args:
            data_id: 配置ID
            group: 分组名称，默认使用配置中的group_name
            **kwargs: 其他参数，如 timeout 等
        """
        return self._run_coroutine(self._async_client.get_config(data_id, group, **kwargs))
    
    def publish_config(self, data_id, content, **kwargs) -> bool:
        """
        发布配置
        
        Args:
            data_id: 配置ID
            content: 配置内容
            **kwargs: 其他参数，如 group, content_type 等
        """
        return self._run_coroutine(self._async_client.publish_config(data_id, content, **kwargs))
    
    def remove_config(self, data_id, group=None) -> bool:
        """
        删除配置
        
        Args:
            data_id: 配置ID
            group: 分组名称，默认使用配置中的group_name
        """
        return self._run_coroutine(self._async_client.remove_config(data_id, group))
    
    def listen_config(self, data_id, **kwargs) -> None:
        """
        监听配置变更
        
        Args:
            data_id: 配置ID
            **kwargs: 其他参数，如 group, callback_func, content_type 等
        """
        # 对于回调函数，需要包装一下，确保在正确的线程中执行
        callback_func = kwargs.get('callback_func')
        if callback_func:
            async def async_callback(content):
                loop = self._get_event_loop()
                await loop.run_in_executor(self._executor, callback_func, content)
            
            kwargs['callback_func'] = async_callback
            
        self._run_coroutine(self._async_client.listen_config(data_id, **kwargs))
    
    def cancel_listen_config(self, data_id, group=None) -> None:
        """
        取消监听配置变更
        
        Args:
            data_id: 配置ID
            group: 分组名称，默认使用配置中的group_name
        """
        self._run_coroutine(self._async_client.cancel_listen_config(data_id, group))
    
    # =============== 客户端管理方法 ===============
    
    def close(self) -> None:
        """关闭客户端连接"""
        if self._closed:
            return
            
        self._closed = True
        try:
            self._run_coroutine(self._async_client.close())
        except Exception as e:
            logger.warning(f"Error closing async client: {e}")
            
        if self._executor:
            self._executor.shutdown(wait=False)
            self._executor = None
        logger.info("Sync Nacos client closed")
    
    def server_health(self) -> bool:
        """检查服务器健康状态"""
        return self._run_coroutine(self._async_client.server_health())
    
    def __enter__(self):
        """支持上下文管理器"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器，退出时关闭客户端"""
        self.close()


def create_sync_client(**kwargs) -> SyncNacosClient:
    """
    创建同步Nacos客户端
    
    Args:
        **kwargs: 客户端配置参数
        
    Returns:
        SyncNacosClient: 同步Nacos客户端实例
    """
    config = NacosClientConfig(**kwargs)
    return SyncNacosClient(config)


def list_services(self, **kwargs) -> Any:
    """
    获取服务列表
    
    Args:
        **kwargs: 参数，如 page_no, page_size, group_name, namespace_id 等
        
    Returns:
        ServiceList: 服务列表
    """
    return self._run_coroutine(self._async_client.list_services(**kwargs))


