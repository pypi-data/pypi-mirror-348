from typing import Optional, Union

from .client_config import NacosClientConfig
from .async_client import AsyncNacosClient
from .sync_client import SyncNacosClient
from .interfaces import NacosClientInterface


class NacosClientFactory:
    """Nacos客户端工厂类，用于创建同步或异步客户端"""
    
    @staticmethod
    def create_client(
        async_mode: bool = False,
        config: Optional[NacosClientConfig] = None,
        **kwargs
    ) -> Union[AsyncNacosClient, SyncNacosClient]:
        """
        创建Nacos客户端
        
        Args:
            async_mode: 是否创建异步客户端，默认为False
            config: Nacos客户端配置，如果为None则使用kwargs创建
            **kwargs: 如果config为None，则使用这些参数创建配置
            
        Returns:
            Union[AsyncNacosClient, SyncNacosClient]: Nacos客户端实例
        """
        config = config or NacosClientConfig(**kwargs)
        
        if async_mode:
            return AsyncNacosClient(config)
        else:
            return SyncNacosClient(config)


# 便捷函数
def create_client(async_mode: bool = False, **kwargs) -> NacosClientInterface:
    """
    创建Nacos客户端
    
    Args:
        async_mode: 是否创建异步客户端，默认为False
        **kwargs: 客户端配置参数
        
    Returns:
        NacosClientInterface: Nacos客户端实例
    """
    return NacosClientFactory.create_client(async_mode=async_mode, **kwargs)