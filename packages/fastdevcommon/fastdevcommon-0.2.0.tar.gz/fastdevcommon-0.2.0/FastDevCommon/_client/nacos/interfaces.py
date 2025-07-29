from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Callable, Any

class NacosClientInterface(ABC):
    """Nacos客户端接口，定义服务发现和配置管理的核心功能"""
    
    @abstractmethod
    def register_instance(self, **kwargs) -> bool:
        """注册服务实例"""
        pass
    
    @abstractmethod
    def deregister_instance(self, **kwargs) -> bool:
        """注销服务实例"""
        pass
    
    @abstractmethod
    def list_instances(self, service_name, **kwargs) -> List[Any]:
        """获取服务实例列表"""
        pass
    
    @abstractmethod
    def list_services(self, **kwargs) -> Any:
        """获取服务列表"""
        pass
    
    @abstractmethod
    def get_config(self, data_id, group=None, **kwargs) -> str:
        """获取配置"""
        pass
    
    @abstractmethod
    def publish_config(self, data_id, content, **kwargs) -> bool:
        """发布配置"""
        pass
    
    @abstractmethod
    def listen_config(self, data_id, **kwargs) -> None:
        """监听配置变更"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """关闭客户端连接"""
        pass


class NacosServiceDiscovery(ABC):
    """Nacos服务发现接口"""
    
    @abstractmethod
    def register_instance(self, **kwargs) -> bool:
        """注册服务实例"""
        pass
    
    @abstractmethod
    def deregister_instance(self, **kwargs) -> bool:
        """注销服务实例"""
        pass
    
    @abstractmethod
    def list_instances(self, service_name, **kwargs) -> List[Any]:
        """获取服务实例列表"""
        pass
    
    @abstractmethod
    def list_services(self, **kwargs) -> Any:
        """获取服务列表"""
        pass
    
    @abstractmethod
    def subscribe(self, service_name, **kwargs) -> None:
        """订阅服务变更"""
        pass
    
    @abstractmethod
    def unsubscribe(self, service_name, **kwargs) -> None:
        """取消订阅服务变更"""
        pass


class NacosConfigService(ABC):
    """Nacos配置服务接口"""
    
    @abstractmethod
    def get_config(self, data_id, group=None, **kwargs) -> str:
        """获取配置"""
        pass
    
    @abstractmethod
    def publish_config(self, data_id, content, **kwargs) -> bool:
        """发布配置"""
        pass
    
    @abstractmethod
    def remove_config(self, data_id, group=None) -> bool:
        """删除配置"""
        pass
    
    @abstractmethod
    def listen_config(self, data_id, **kwargs) -> None:
        """监听配置变更"""
        pass
    
    @abstractmethod
    def cancel_listen_config(self, data_id, group=None) -> None:
        """取消监听配置变更"""
        pass