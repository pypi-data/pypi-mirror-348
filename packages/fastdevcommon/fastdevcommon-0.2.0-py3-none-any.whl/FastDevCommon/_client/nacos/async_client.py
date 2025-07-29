import asyncio
from typing import Dict, List, Optional, Callable, Any

from v2.nacos import (
    NacosNamingService as V2NacosNamingService, 
    NacosConfigService as V2NacosConfigService,
    RegisterInstanceParam, DeregisterInstanceParam, BatchRegisterInstanceParam,
    GetServiceParam, ListServiceParam, ListInstanceParam, ConfigParam,
    Instance, Service, ServiceList, SubscribeServiceParam
)
from .client_config import NacosClientConfig
from .interfaces import NacosClientInterface, NacosServiceDiscovery, NacosConfigService as NacosConfigServiceInterface
from ..._logger import logger


class AsyncNacosServiceDiscovery(NacosServiceDiscovery):
    """异步Nacos服务发现实现"""
    
    def __init__(self, config: NacosClientConfig):
        self.config = config
        self._naming_service: Optional[V2NacosNamingService] = None
        self._lock = asyncio.Lock()
    
    async def _ensure_naming_service(self) -> V2NacosNamingService:
        """确保命名服务已初始化"""
        if not self._naming_service:
            async with self._lock:
                if not self._naming_service:
                    self._naming_service = await V2NacosNamingService.create_naming_service(self.config.client_config)
        return self._naming_service
    
    async def register_instance(self, 
                               service_name: str = None, 
                               ip: str = None, 
                               port: int = None,
                               weight: float = 1.0, 
                               cluster_name: str = "DEFAULT", 
                               metadata: Dict = None,
                               enabled: bool = True, 
                               healthy: bool = True, 
                               ephemeral: bool = True,
                               group_name: str = None) -> bool:
        """注册服务实例"""
        naming_service = await self._ensure_naming_service()
        
        service_name = service_name or self.config.service_name
        ip = ip or self.config.service_host
        port = port or self.config.service_port
        group_name = group_name or self.config.group_name
        
        if not service_name:
            raise ValueError("service_name must be provided")
        if not ip:
            raise ValueError("ip must be provided")
        if not port:
            raise ValueError("port must be provided")
        
        param = RegisterInstanceParam(
            service_name=service_name,
            group_name=group_name,
            ip=ip,
            port=port,
            weight=weight,
            enabled=enabled,
            healthy=healthy,
            metadata=metadata or {},
            cluster_name=cluster_name,
            ephemeral=ephemeral
        )
        
        logger.info(f"Registering instance: {param.model_dump()}")
        return await naming_service.register_instance(param)
    async def list_services(self, page_no=1, page_size=10, group_name=None, namespace_id=None, **kwargs) -> Any:
        """
        获取服务列表
        
        Args:
            page_no: 页码，默认为1
            page_size: 每页大小，默认为10
            group_name: 分组名称，默认使用配置中的group_name
            namespace_id: 命名空间ID，默认使用配置中的namespace_id
            **kwargs: 其他参数
            
        Returns:
            ServiceList: 服务列表
        """
        naming_service = await self._ensure_naming_service()
        group_name = group_name or self.config.group_name
        namespace_id = namespace_id or self.config.namespace_id
        
        param = ListServiceParam(
            page_no=page_no,
            page_size=page_size,
            group_name=group_name,
            namespace_id=namespace_id
        )
        
        return await naming_service.list_services(param)
    async def deregister_instance(self,
                                 service_name: str = None,
                                 ip: str = None,
                                 port: int = None,
                                 cluster_name: str = "DEFAULT",
                                 ephemeral: bool = True,
                                 group_name: str = None) -> bool:
        """注销服务实例"""
        naming_service = await self._ensure_naming_service()
        
        service_name = service_name or self.config.service_name
        ip = ip or self.config.service_host
        port = port or self.config.service_port
        group_name = group_name or self.config.group_name
        
        if not service_name:
            raise ValueError("service_name must be provided")
        if not ip:
            raise ValueError("ip must be provided")
        if not port:
            raise ValueError("port must be provided")
        
        param = DeregisterInstanceParam(
            service_name=service_name,
            group_name=group_name,
            ip=ip,
            port=port,
            cluster_name=cluster_name,
            ephemeral=ephemeral
        )
        
        logger.info(f"Deregistering instance: {param.model_dump()}")
        return await naming_service.deregister_instance(param)
    
    async def list_instances(self,
                            service_name: str,
                            group_name: str = None,
                            clusters: str = None,
                            healthy_only: bool = False) -> List[Instance]:
        """获取服务实例列表"""
        naming_service = await self._ensure_naming_service()
        group_name = group_name or self.config.group_name
        
        # 确保clusters是列表类型
        cluster_list = []
        if clusters:
            if isinstance(clusters, str):
                # 如果是逗号分隔的字符串，转换为列表
                cluster_list = [c.strip() for c in clusters.split(',') if c.strip()]
            elif isinstance(clusters, list):
                cluster_list = clusters
        
        # 如果列表为空，添加默认集群
        if not cluster_list:
            cluster_list = ["DEFAULT"]
        
        param = ListInstanceParam(
            service_name=service_name,
            group_name=group_name,
            clusters=cluster_list,
            healthy_only=healthy_only
        )
        
        return await naming_service.list_instances(param)
    
    async def subscribe(self,
                       service_name: str,
                       group_name: str = None,
                       clusters: str = None,
                       callback_func: Callable = None) -> None:
        """订阅服务变更"""
        naming_service = await self._ensure_naming_service()
        group_name = group_name or self.config.group_name
        
        param = SubscribeServiceParam(
            service_name=service_name,
            group_name=group_name,
            clusters=clusters
        )
        
        await naming_service.subscribe(param, callback_func)
        logger.info(f"Subscribed to service: {service_name}, group: {group_name}")
    
    async def unsubscribe(self,
                         service_name: str,
                         group_name: str = None,
                         clusters: str = None) -> None:
        """取消订阅服务变更"""
        naming_service = await self._ensure_naming_service()
        group_name = group_name or self.config.group_name
        
        param = SubscribeServiceParam(
            service_name=service_name,
            group_name=group_name,
            clusters=clusters
        )
        
        await naming_service.unsubscribe(param)
        logger.info(f"Unsubscribed from service: {service_name}, group: {group_name}")
    
    async def close(self) -> None:
        """关闭服务发现客户端"""
        if self._naming_service:
            # NacosNamingService没有close方法，检查是否有其他关闭方法
            # 如果没有，可以简单地将引用设为None
            self._naming_service = None
            logger.info("Async Nacos service discovery client closed")


class AsyncNacosConfigService(NacosConfigServiceInterface):
    """异步Nacos配置服务实现"""
    
    def __init__(self, config: NacosClientConfig):
        self.config = config
        self._config_service: Optional[V2NacosConfigService] = None
        self._lock = asyncio.Lock()
    
    async def _ensure_config_service(self) -> V2NacosConfigService:
        """确保配置服务已初始化"""
        if not self._config_service:
            async with self._lock:
                if not self._config_service:
                    self._config_service = await V2NacosConfigService.create_config_service(self.config.client_config)
        return self._config_service
    
    async def get_config(self,
                        data_id: str,
                        group: str = None,
                        timeout: int = None) -> str:
        """获取配置"""
        config_service = await self._ensure_config_service()
        group = group or self.config.group_name
        
        param = ConfigParam(
            data_id=data_id,
            group=group
        )
        
        return await config_service.get_config(param)
    
    async def publish_config(self,
                            data_id: str,
                            content: str,
                            group: str = None,
                            content_type: str = None) -> bool:
        """发布配置"""
        config_service = await self._ensure_config_service()
        group = group or self.config.group_name
        
        param = ConfigParam(
            data_id=data_id,
            group=group,
            content=content,
            content_type=content_type
        )
        
        return await config_service.publish_config(param)
    
    async def remove_config(self,
                           data_id: str,
                           group: str = None) -> bool:
        """删除配置"""
        config_service = await self._ensure_config_service()
        group = group or self.config.group_name
        
        param = ConfigParam(
            data_id=data_id,
            group=group
        )
        
        return await config_service.remove_config(param)
    
    # 修改 listen_config 方法实现
    async def listen_config(self, data_id, group=None, callback_func=None, content_type=None, **kwargs) -> None:
        """
        监听配置变更
        
        Args:
            data_id: 配置ID
            group: 分组名称，默认使用配置中的group_name
            callback_func: 回调函数，当配置变更时调用
            content_type: 内容类型
            **kwargs: 其他参数
        """
        config_service = await self._ensure_config_service()
        group = group or self.config.group_name
        
        param = ConfigParam(
            data_id=data_id,
            group=group,
            content_type=content_type
        )
        
        # 检查 config_service 是否有 listen_config 方法
        if hasattr(config_service, 'listen_config'):
            await config_service.listen_config(param, callback_func)
        else:
            # 如果没有 listen_config 方法，使用替代方法或自己实现
            # 这里使用轮询方式实现配置监听
            
            # 只在类属性未设置时输出一次警告
            if not hasattr(self, '_warned_no_listen_config'):
                logger.warning(f"NacosConfigService does not have listen_config method, using polling instead")
                self._warned_no_listen_config = True
            
            # 创建一个任务来定期检查配置变更
            asyncio.create_task(self._poll_config_changes(data_id, group, callback_func, content_type))
            
        logger.info(f"Listening to config: {data_id}, group: {group}")
    
    # 修正 _poll_config_changes 方法实现
    async def _poll_config_changes(self, data_id, group, callback_func, content_type, interval=5):
        """
        通过轮询方式监听配置变更
        
        Args:
            data_id: 配置ID
            group: 分组名称
            callback_func: 回调函数
            content_type: 内容类型
            interval: 轮询间隔（秒）
        """
        if not callback_func:
            logger.warning(f"No callback function provided for config polling: {data_id}, group: {group}")
            return
            
        # 存储配置的键
        config_key = f"{group}#{data_id}"
        
        # 如果没有初始化轮询状态字典，则创建
        if not hasattr(self, '_polling_configs'):
            self._polling_configs = {}
            self._polling_contents = {}
            self._polling_tasks = {}
        
        # 标记为正在轮询
        self._polling_configs[config_key] = True
        
        # 获取初始配置
        try:
            # 添加重试逻辑获取初始配置
            max_retries = 3
            retry_delay = 2
            current_content = None
            
            for retry in range(max_retries):
                try:
                    current_content = await self.get_config(data_id, group)
                    break  # 成功获取配置，跳出重试循环
                except Exception as e:
                    if retry < max_retries - 1:
                        logger.warning(f"Error getting config (retry {retry+1}/{max_retries}): {e}")
                        await asyncio.sleep(retry_delay)
                    else:
                        # 最后一次重试失败，抛出异常
                        raise
                
            if current_content is None:
                logger.error(f"Failed to get initial config after {max_retries} retries")
                return
                
            self._polling_contents[config_key] = current_content
            
            # 开始轮询
            consecutive_errors = 0
            max_consecutive_errors = 5
            
            while self._polling_configs.get(config_key, False):
                await asyncio.sleep(interval)
                
                try:
                    # 获取最新配置
                    new_content = await self.get_config(data_id, group)
                    consecutive_errors = 0  # 重置连续错误计数
                    
                    # 如果配置发生变化，调用回调函数
                    if new_content != self._polling_contents.get(config_key):
                        logger.info(f"Config changed: {data_id}, group: {group}")
                        self._polling_contents[config_key] = new_content
                        
                        # 调用回调函数
                        try:
                            await callback_func(new_content)
                        except Exception as e:
                            logger.error(f"Error in config change callback: {e}")
                except Exception as e:
                    consecutive_errors += 1
                    # 使用指数退避策略增加重试间隔
                    backoff_interval = min(interval * (2 ** consecutive_errors), 60)  # 最大60秒
                    
                    if consecutive_errors >= max_consecutive_errors:
                        logger.error(f"Too many consecutive errors ({consecutive_errors}) polling config, stopping: {e}")
                        break
                        
                    logger.warning(f"Error polling config (consecutive errors: {consecutive_errors}): {e}")
                    logger.info(f"Will retry in {backoff_interval} seconds")
                    await asyncio.sleep(backoff_interval - interval)  # 减去已经等待的时间
                    
        except Exception as e:
            logger.error(f"Error starting config polling: {e}")
        
        # 轮询结束，清理状态
        if config_key in self._polling_configs:
            del self._polling_configs[config_key]
        if config_key in self._polling_contents:
            del self._polling_contents[config_key]
        
        logger.info(f"Config polling stopped for: {data_id}, group: {group}")
    
    # 修改 cancel_listen_config 方法实现
    async def cancel_listen_config(self, data_id: str, group: str = None) -> None:
        """取消监听配置变更"""
        config_service = await self._ensure_config_service()
        group = group or self.config.group_name
        
        param = ConfigParam(
            data_id=data_id,
            group=group
        )
        
        # 检查 config_service 是否有 cancel_listen_config 方法
        if hasattr(config_service, 'cancel_listen_config'):
            await config_service.cancel_listen_config(param)
        else:
            # 如果没有 cancel_listen_config 方法，使用我们自己的轮询取消逻辑
            config_key = f"{group}#{data_id}"
            if hasattr(self, '_polling_configs') and config_key in self._polling_configs:
                self._polling_configs[config_key] = False
                logger.info(f"Stopped polling config: {data_id}, group: {group}")
            else:
                logger.warning(f"No active polling for config: {data_id}, group: {group}")
                
        logger.info(f"Canceled listening to config: {data_id}, group: {group}")
    
    async def close(self) -> None:
        """关闭配置服务客户端"""
        if self._config_service:
            try:
                if hasattr(self._config_service, 'close'):
                    await self._config_service.close()
                elif hasattr(self._config_service, 'shutdown'):
                    await self._config_service.shutdown()
            except Exception as e:
                logger.warning(f"Error closing config service: {e}")
            self._config_service = None
            logger.info("Async Nacos config service client closed")


class AsyncNacosClient(NacosClientInterface):
    """异步Nacos客户端，支持服务发现和配置管理"""

    def __init__(self, config: Optional[NacosClientConfig] = None, **kwargs):
        """
        初始化异步Nacos客户端
        
        Args:
            config: Nacos客户端配置，如果为None则使用kwargs创建
            **kwargs: 如果config为None，则使用这些参数创建配置
        """
        self.config = config or NacosClientConfig(**kwargs)
        self._service_discovery = AsyncNacosServiceDiscovery(self.config)
        self._config_service = AsyncNacosConfigService(self.config)
    
    # =============== 服务发现相关方法 ===============
    
    async def register_instance(self, **kwargs) -> bool:
        """注册服务实例"""
        return await self._service_discovery.register_instance(**kwargs)
    
    async def deregister_instance(self, **kwargs) -> bool:
        """注销服务实例"""
        return await self._service_discovery.deregister_instance(**kwargs)
    
    async def list_instances(self, service_name, **kwargs) -> List[Instance]:
        """
        获取服务实例列表
        
        Args:
            service_name: 服务名称
            **kwargs: 其他参数，如 group_name, clusters, healthy_only 等
        """
        return await self._service_discovery.list_instances(service_name, **kwargs)
    
    async def list_services(self, **kwargs) -> Any:
        """
        获取服务列表
        
        Args:
            **kwargs: 参数，如 page_no, page_size, group_name, namespace_id 等
            
        Returns:
            ServiceList: 服务列表
        """
        return await self._service_discovery.list_services(**kwargs)
    
    async def subscribe(self, service_name, **kwargs) -> None:
        """
        订阅服务变更
        
        Args:
            service_name: 服务名称
            **kwargs: 其他参数，如 group_name, clusters, callback_func 等
        """
        await self._service_discovery.subscribe(service_name, **kwargs)
    
    async def unsubscribe(self, service_name, **kwargs) -> None:
        """
        取消订阅服务变更
        
        Args:
            service_name: 服务名称
            **kwargs: 其他参数，如 group_name, clusters 等
        """
        await self._service_discovery.unsubscribe(service_name, **kwargs)
    
    # =============== 配置管理相关方法 ===============
    
    async def get_config(self, data_id, group=None, **kwargs) -> str:
        """
        获取配置
        
        Args:
            data_id: 配置ID
            group: 分组名称，默认使用配置中的group_name
            **kwargs: 其他参数，如 timeout 等
        """
        return await self._config_service.get_config(data_id, group, **kwargs)
    
    async def publish_config(self, data_id, content, **kwargs) -> bool:
        """
        发布配置
        
        Args:
            data_id: 配置ID
            content: 配置内容
            **kwargs: 其他参数，如 group, content_type 等
        """
        return await self._config_service.publish_config(data_id, content, **kwargs)
    
    async def remove_config(self, data_id, group=None) -> bool:
        """
        删除配置
        
        Args:
            data_id: 配置ID
            group: 分组名称，默认使用配置中的group_name
        """
        return await self._config_service.remove_config(data_id, group)
    
    async def listen_config(self, data_id, **kwargs) -> None:
        """
        监听配置变更
        
        Args:
            data_id: 配置ID
            **kwargs: 其他参数，如 group, callback_func, content_type 等
        """
        await self._config_service.listen_config(data_id, **kwargs)
    
    async def cancel_listen_config(self, data_id, group=None) -> None:
        """
        取消监听配置变更
        
        Args:
            data_id: 配置ID
            group: 分组名称，默认使用配置中的group_name
        """
        await self._config_service.cancel_listen_config(data_id, group)
    
    # =============== 客户端管理方法 ===============
    
    async def close(self) -> None:
        """关闭客户端连接"""
        await self._service_discovery.close()
        await self._config_service.close()
        logger.info("Async Nacos client closed")
    
    async def server_health(self) -> bool:
        """检查服务器健康状态"""
        try:
            # 尝试获取一个不存在的配置，如果服务器正常，应该返回空字符串而不是抛出异常
            await self.get_config(data_id="health_check", group="DEFAULT_GROUP")
            return True
        except Exception as e:
            logger.warning(f"Server health check failed: {e}")
            return False


def create_async_client(**kwargs) -> AsyncNacosClient:
    """
    创建异步Nacos客户端
    
    Args:
        **kwargs: 客户端配置参数
        
    Returns:
        AsyncNacosClient: 异步Nacos客户端实例
    """
    config = NacosClientConfig(**kwargs)
    return AsyncNacosClient(config)


async def list_services(self, page_no=1, page_size=10, group_name=None, namespace_id=None, **kwargs) -> Any:
    """
    获取服务列表
    
    Args:
        page_no: 页码，默认为1
        page_size: 每页大小，默认为10
        group_name: 分组名称，默认使用配置中的group_name
        namespace_id: 命名空间ID，默认使用配置中的namespace_id
        **kwargs: 其他参数
        
    Returns:
        ServiceList: 服务列表
    """
    naming_service = await self._ensure_naming_service()
    group_name = group_name or self.config.group_name
    namespace_id = namespace_id or self.config.namespace_id
    
    param = ListServiceParam(
        page_no=page_no,
        page_size=page_size,
        group_name=group_name,
        namespace_id=namespace_id
    )
    
    return await naming_service.list_services(param)

