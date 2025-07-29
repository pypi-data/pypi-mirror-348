import os
from v2.nacos import ClientConfigBuilder, GRPCConfig


class NacosClientConfig:
    """Nacos客户端配置类，用于同步和异步客户端共享配置"""
    
    def __init__(
            self,
            service_name: str = "",
            service_host: str = "",
            service_port: int = 0,
            group_name: str = "DEFAULT_GROUP",
            namespace_id: str = "",
            server_address: str = "",
            access_key: str = "",
            secret_key: str = "",
            log_level: str = "INFO",
            grpc_timeout: int = 5000,
            **kwargs
    ):
        # 服务相关配置
        self.service_name = service_name or os.getenv("NACOS_SERVICE_NAME", "")
        self.service_host = service_host or os.getenv("NACOS_SERVICE_HOST", "localhost")
        self.service_port = service_port or int(os.getenv("NACOS_SERVICE_PORT", "8848"))
        self.group_name = group_name or os.getenv("NACOS_GROUP_NAME", "DEFAULT_GROUP")
        self.namespace_id = namespace_id or os.getenv("NACOS_NAMESPACE", "")
        
        # 服务器地址
        self.server_address = server_address or os.getenv('NACOS_SERVER_ADDR', '')
        if not self.server_address:
            self.server_address = f"{self.service_host}:{self.service_port}"
        if not self.server_address.startswith("http"):
            self.server_address = "http://" + self.server_address
            
        # 认证信息
        self.access_key = access_key or os.getenv("NACOS_ACCESS_KEY", "")
        self.secret_key = secret_key or os.getenv("NACOS_SECRET_KEY", "")
        
        # 其他配置
        self.log_level = log_level
        self.grpc_timeout = grpc_timeout
        
        # 构建客户端配置
        self.client_config = (ClientConfigBuilder()
                             .access_key(self.access_key)
                             .secret_key(self.secret_key)
                             .server_address(self.server_address)
                             .namespace_id(self.namespace_id)
                             .log_level(self.log_level)
                             .grpc_config(GRPCConfig(grpc_timeout=self.grpc_timeout))
                             .build())