import hashlib
import json
from typing import Dict, List, Optional, Any, Callable
import asyncio

from .client_config import NacosClientConfig
from ..._logger import logger
from ..http_client import HttpClient, Response

class NacosClient:
    """
    Nacos 统一客户端，支持 V1 和 V2 API，提供配置管理和服务发现功能
    """

    def __init__(self, server_addresses: str = None, namespace: str = "", username: str = None,
                 password: str = None, version: str = "v1", config: NacosClientConfig = None):
        """
        初始化 Nacos 客户端

        Args:
            server_addresses: Nacos服务器地址，多个地址用逗号分隔，如：'http://127.0.0.1:8848,http://127.0.0.1:8849'
            namespace: 命名空间ID，默认为空字符串，等同于public
            username: 用户名，如果Nacos开启了认证
            password: 密码，如果Nacos开启了认证
            version: Nacos API 版本，可选值为 "v1" 或 "v2"，默认为 "v1"
            config: NacosClientConfig 配置对象，如果提供则优先使用该配置
        """
        # 如果提供了配置对象，则优先使用配置对象中的值
        if config:
            self.server_addresses = [config.server_address] if config.server_address else []
            self.namespace = config.namespace_id
            self.username = config.access_key
            self.password = config.secret_key
            # 默认使用 v1 版本，除非配置中明确指定
            self.version = getattr(config, 'version', 'v1').lower()
        else:
            # 使用传入的参数初始化
            self.server_addresses = server_addresses.split(',') if server_addresses else []
            self.namespace = namespace
            self.username = username
            self.password = password
            self.version = version.lower()

        self.current_server_index = 0
        self._listening_configs = {}
        self._listening_tasks = {}

        if self.version not in ["v1", "v2"]:
            raise ValueError("Version must be 'v1' or 'v2'")

        # 如果提供了用户名和密码，则进行登录
        self.access_token = None
        if self.username and self.password:
            asyncio.create_task(self._login())

    @classmethod
    def from_config(cls, config: NacosClientConfig):
        """
        从配置对象创建客户端实例

        Args:
            config: NacosClientConfig 配置对象

        Returns:
            NacosClient: 客户端实例
        """
        return cls(config=config)
    
    async def _login(self):
        """登录Nacos获取访问令牌"""
        # Nacos 认证接口，v1和v2版本都使用相同的路径
        path = "/nacos/v1/auth/login"
        
        # 使用表单数据方式提交
        data = {
            'username': self.username,
            'password': self.password
        }
        
        # 尝试POST方式登录
        response = await self._request('POST', path, data=data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.access_token = data.get('accessToken')
                logger.info("Successfully logged in to Nacos")
            except json.JSONDecodeError:
                # 尝试解析文本响应
                if "accessToken" in response.text:
                    import re
                    match = re.search(r'"accessToken":"([^"]+)"', response.text)
                    if match:
                        self.access_token = match.group(1)
                        logger.info("Successfully logged in to Nacos (parsed from text)")
                else:
                    logger.error(f"Failed to parse login response: {response.text}")
        else:
            # 如果POST失败，尝试GET方式（某些旧版本可能支持）
            params = {
                'username': self.username,
                'password': self.password
            }
            response = await self._request('GET', path, params=params)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.access_token = data.get('accessToken')
                    logger.info("Successfully logged in to Nacos using GET method")
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse login response: {response.text}")
            else:
                error_msg = response.text if response else 'No response'
                logger.error(f"Failed to login to Nacos: {error_msg}")
    
    def _get_server_url(self):
        """获取当前使用的服务器URL"""
        return self.server_addresses[self.current_server_index]
    
    def _switch_server(self):
        """切换到下一个服务器"""
        self.current_server_index = (self.current_server_index + 1) % len(self.server_addresses)
        logger.info(f"Switched to Nacos server: {self._get_server_url()}")
    
    async def _request(self, method: str, path: str, params: Dict = None, data: Dict = None, headers: Dict = None, 
                 max_retries: int = 3) -> Optional[Response]:
        """
        发送HTTP请求到Nacos服务器
        
        Args:
            method: HTTP方法，如GET、POST、PUT、DELETE
            path: 请求路径
            params: URL参数
            data: 请求体数据
            headers: 请求头
            max_retries: 最大重试次数
            
        Returns:
            Response: HTTP响应对象
        """
        if params is None:
            params = {}
        else:
            # 转换布尔值为字符串，避免URL参数类型错误
            for key, value in list(params.items()):
                if isinstance(value, bool):
                    params[key] = str(value).lower()
        
        # 添加命名空间参数
        if self.namespace:
            if 'namespaceId' not in params and 'tenant' not in params:
                if self.version == "v1" and 'cs' in path:  # V1 配置管理API使用tenant
                    params['tenant'] = self.namespace
                else:  # V2 API 和 V1 服务发现API使用namespaceId
                    params['namespaceId'] = self.namespace
        
        # 添加访问令牌
        if self.access_token:
            if params is None:
                params = {}
            params['accessToken'] = self.access_token
        
        # 默认请求头
        if headers is None:
            headers = {}
        
        # 处理请求体中的布尔值
        if data:
            for key, value in list(data.items()):
                if isinstance(value, bool):
                    data[key] = str(value).lower()
        
        retries = 0
        last_error = None
        
        while retries < max_retries:
            try:
                url = f"{self._get_server_url()}{path}"
                
                client = HttpClient()
                if method == 'GET':
                    response = await client.get(url, params=params, headers=headers)
                elif method == 'POST':
                    response = await client.post(url, params=params, data=data, headers=headers)
                elif method == 'PUT':
                    response = await client.put(url, params=params, data=data, headers=headers)
                elif method == 'DELETE':
                    response = await client.delete(url, params=params, data=data, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # 检查响应状态码
                if 200 <= response.status_code < 300:
                    return response
                
                # 处理错误响应
                if response.status_code == 403:
                    # 可能是认证失败，尝试重新登录
                    if self.username and self.password:
                        await self._login()
                
                logger.warning(f"Request failed with status code {response.status_code}: {response.text}")
                
                # 切换到下一个服务器
                self._switch_server()
                
            except Exception as e:
                logger.error(f"Request error: {str(e)}")
                last_error = e
                # 切换到下一个服务器
                self._switch_server()
            
            retries += 1
            # 等待一段时间后重试
            await asyncio.sleep(1)
        
        if last_error:
            logger.error(f"Max retries reached. Last error: {str(last_error)}")
        else:
            logger.error("Max retries reached. All servers failed.")
        
        return None
    
    # ================ 配置管理 API ================
    
    async def get_config(self, data_id: str, group: str = "DEFAULT_GROUP") -> Optional[str]:
        """
        获取配置
        
        Args:
            data_id: 配置ID
            group: 配置分组，默认为DEFAULT_GROUP
            
        Returns:
            str: 配置内容
        """
        if self.version == "v1":
            path = "/nacos/v1/cs/configs"
            params = {
                'dataId': data_id,
                'group': group
            }
        else:  # v2
            path = "/nacos/v2/cs/config"
            params = {
                'dataId': data_id,
                'group': group
            }
        
        response = await self._request('GET', path, params=params)
        if response:
            if self.version == "v1":
                return response.text
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data')
                except json.JSONDecodeError:
                    return None
        return None
    
    async def publish_config(self, data_id: str, group: str, content: str, 
                      content_type: str = None) -> bool:
        """
        发布配置
        
        Args:
            data_id: 配置ID
            group: 配置分组
            content: 配置内容
            content_type: 配置类型，如text, json, xml, yaml, html, properties
            
        Returns:
            bool: 是否发布成功
        """
        if self.version == "v1":
            path = "/nacos/v1/cs/configs"
        else:  # v2
            path = "/nacos/v2/cs/config"
        
        data = {
            'dataId': data_id,
            'group': group,
            'content': content
        }
        
        if content_type:
            data['type'] = content_type
        
        response = await self._request('POST', path, data=data)
        if response:
            if self.version == "v1":
                return response.text == "true"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    async def remove_config(self, data_id: str, group: str = "DEFAULT_GROUP") -> bool:
        """
        删除配置
        
        Args:
            data_id: 配置ID
            group: 配置分组，默认为DEFAULT_GROUP
            
        Returns:
            bool: 是否删除成功
        """
        if self.version == "v1":
            path = "/nacos/v1/cs/configs"
        else:  # v2
            path = "/nacos/v2/cs/config"
        
        params = {
            'dataId': data_id,
            'group': group
        }
        
        response = await self._request('DELETE', path, params=params)
        if response:
            if self.version == "v1":
                return response.text == "true"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    async def listen_config(self, data_id: str, group: str, callback: Callable[[str], Any]) -> None:
        """
        监听配置变更
        
        Args:
            data_id: 配置ID
            group: 配置分组
            callback: 配置变更回调函数，接收新的配置内容作为参数
        """
        config_key = f"{data_id}^{group}"
        if config_key in self._listening_configs:
            logger.warning(f"Already listening to config: {config_key}")
            return
        
        self._listening_configs[config_key] = callback
        
        # 创建监听任务
        task = asyncio.create_task(self._listen_config_task(data_id, group, callback))
        self._listening_tasks[config_key] = task
    
    async def _listen_config_task(self, data_id: str, group: str, callback: Callable[[str], Any]) -> None:
        """
        配置监听任务
        
        Args:
            data_id: 配置ID
            group: 配置分组
            callback: 配置变更回调函数
        """
        # 获取初始配置
        content = await self.get_config(data_id, group)
        if content is not None:
            # 计算MD5
            content_md5 = hashlib.md5(content.encode('utf-8')).hexdigest()
        else:
            content_md5 = ""
        
        config_key = f"{data_id}^{group}"
        
        while config_key in self._listening_configs:
            try:
                # 构建监听参数
                if self.version == "v1":
                    path = "/nacos/v1/cs/configs/listener"
                    headers = {
                        'Long-Pulling-Timeout': '30000'
                    }
                    
                    # 构建监听数据
                    listening_configs = f"{data_id}%02{group}%02{content_md5}"
                    if self.namespace:
                        listening_configs += f"%02{self.namespace}"
                    listening_configs += "%01"
                    
                    data = {
                        'Listening-Configs': listening_configs
                    }
                else:  # v2
                    path = "/nacos/v2/cs/config/listener"
                    headers = {
                        'Long-Pulling-Timeout': '30000'
                    }
                    
                    # 构建监听数据
                    listening_configs = f"{data_id}%02{group}%02{content_md5}"
                    if self.namespace:
                        listening_configs += f"%02{self.namespace}"
                    listening_configs += "%01"
                    
                    data = {
                        'Listening-Configs': listening_configs
                    }
                
                # 发送长轮询请求
                response = await self._request('POST', path, data=data, headers=headers)
                
                if response and response.text:
                    # 配置已变更，获取最新配置
                    new_content = await self.get_config(data_id, group)
                    if new_content is not None:
                        # 更新MD5
                        content_md5 = hashlib.md5(new_content.encode('utf-8')).hexdigest()
                        # 调用回调函数
                        await callback(new_content)
                
            except Exception as e:
                logger.error(f"Error in config listening task: {str(e)}")
                # 出错后等待一段时间再重试
                await asyncio.sleep(5)
    
    async def cancel_listen_config(self, data_id: str, group: str) -> None:
        """
        取消配置监听
        
        Args:
            data_id: 配置ID
            group: 配置分组
        """
        config_key = f"{data_id}^{group}"
        if config_key in self._listening_configs:
            del self._listening_configs[config_key]
            
            # 取消监听任务
            if config_key in self._listening_tasks:
                task = self._listening_tasks[config_key]
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                del self._listening_tasks[config_key]
    
    # ================ 服务发现 API ================
    
    async def register_instance(self, service_name: str, ip: str, port: int, 
                         weight: float = 1.0, enabled: bool = True, healthy: bool = True,
                         ephemeral: bool = True, cluster_name: str = "DEFAULT", 
                         group_name: str = "DEFAULT_GROUP", metadata: Dict = None) -> str:
        """
        注册服务实例
        
        Args:
            service_name: 服务名
            ip: 实例IP
            port: 实例端口
            weight: 实例权重，默认为1.0
            enabled: 是否启用，默认为True
            healthy: 是否健康，默认为True
            ephemeral: 是否临时实例，默认为True
            cluster_name: 集群名称，默认为DEFAULT
            group_name: 分组名称，默认为DEFAULT_GROUP
            metadata: 元数据，默认为None
            
        Returns:
            str: 注册结果
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/instance"
        else:  # v2
            path = "/nacos/v2/ns/instance"
        
        data = {
            'serviceName': service_name,
            'ip': ip,
            'port': port,
            'weight': weight,
            'enabled': str(enabled).lower(),  # 转换为字符串
            'healthy': str(healthy).lower(),  # 转换为字符串
            'ephemeral': str(ephemeral).lower(),  # 转换为字符串
            'clusterName': cluster_name,
            'groupName': group_name
        }
        
        if metadata:
            # 将字典转换为JSON字符串
            data['metadata'] = json.dumps(metadata)
        
        response = await self._request('POST', path, data=data)
        if response:
            if self.version == "v1":
                return response.text
            else:  # v2
                try:
                    result = response.json()
                    return "ok" if result.get('code') == 0 else result.get('message', "error")
                except json.JSONDecodeError:
                    return response.text
        return "error"
    
    async def deregister_instance(self, service_name: str, ip: str, port: int,
                           cluster_name: str = "DEFAULT", ephemeral: bool = True,
                           group_name: str = "DEFAULT_GROUP") -> bool:
        """
        注销服务实例
        
        Args:
            service_name: 服务名
            ip: 实例IP
            port: 实例端口
            cluster_name: 集群名称，默认为DEFAULT
            ephemeral: 是否为临时实例，默认为True
            group_name: 分组名称，默认为DEFAULT_GROUP
            
        Returns:
            bool: 是否注销成功
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/instance"
        else:  # v2
            path = "/nacos/v2/ns/instance"
        
        data = {
            'serviceName': service_name,
            'ip': ip,
            'port': port,
            'clusterName': cluster_name,
            'ephemeral': ephemeral,
            'groupName': group_name
        }
        
        response = await self._request('DELETE', path, data=data)
        if response:
            if self.version == "v1":
                return response.text == "ok"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    async def get_instance(self, service_name: str, ip: str, port: int,
                    cluster_name: str = "DEFAULT", 
                    group_name: str = "DEFAULT_GROUP") -> Optional[Dict]:
        """
        查询服务实例详情
        
        Args:
            service_name: 服务名
            ip: 实例IP
            port: 实例端口
            cluster_name: 集群名称，默认为DEFAULT
            group_name: 分组名称，默认为DEFAULT_GROUP
            
        Returns:
            Dict: 实例详情
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/instance"
        else:  # v2
            path = "/nacos/v2/ns/instance"
        
        params = {
            'serviceName': service_name,
            'ip': ip,
            'port': port,
            'clusterName': cluster_name,
            'groupName': group_name
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            if self.version == "v1":
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return None
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data')
                except json.JSONDecodeError:
                    return None
        return None
    
    async def list_instances(self, service_name: str, cluster_name: str = None, 
                      group_name: str = "DEFAULT_GROUP", healthy_only: bool = False) -> Optional[Dict]:
        """
        查询服务实例列表
        
        Args:
            service_name: 服务名
            cluster_name: 集群名称，默认为None
            group_name: 分组名称，默认为DEFAULT_GROUP
            healthy_only: 是否只返回健康实例，默认为False
            
        Returns:
            Dict: 实例列表
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/instance/list"
        else:  # v2
            path = "/nacos/v2/ns/instance/list"
        
        params = {
            'serviceName': service_name,
            'groupName': group_name,
            'healthyOnly': str(healthy_only).lower()  # 转换为字符串
        }
        
        if cluster_name:
            params['clusters'] = cluster_name
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                if self.version == "v1":
                    return response.json()
                else:  # v2
                    result = response.json()
                    return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def update_instance_metadata_batch(self, service_name: str, metadata: Dict, 
                                     instances: List[Dict] = None, 
                                     consistency_type: str = None,
                                     group_name: str = "DEFAULT_GROUP") -> bool:
        """
        批量更新实例元数据
        
        Args:
            service_name: 服务名
            metadata: 元数据
            instances: 实例列表，默认为None，表示更新所有实例
            consistency_type: 一致性类型，'persist'表示持久化实例，默认为None表示临时实例
            group_name: 分组名称，默认为DEFAULT_GROUP
            
        Returns:
            bool: 是否更新成功
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Batch update instance metadata is only supported in Nacos V2 API")
            return False
        
        path = "/nacos/v2/ns/instance/metadata/batch"
        
        data = {
            'serviceName': service_name,
            'groupName': group_name,
            'metadata': json.dumps(metadata)
        }
        
        if consistency_type:
            data['consistencyType'] = consistency_type
        
        if instances:
            data['instances'] = json.dumps(instances)
        
        response = await self._request('PUT', path, data=data)
        if response:
            try:
                result = response.json()
                return result.get('data', False)
            except json.JSONDecodeError:
                return False
        return False
    
    async def delete_instance_metadata_batch(self, service_name: str, metadata: Dict, 
                                     instances: List[Dict] = None, 
                                     consistency_type: str = None,
                                     group_name: str = "DEFAULT_GROUP") -> bool:
        """
        批量删除实例元数据
        
        Args:
            service_name: 服务名
            metadata: 元数据
            instances: 实例列表，默认为None，表示更新所有实例
            consistency_type: 一致性类型，'persist'表示持久化实例，默认为None表示临时实例
            group_name: 分组名称，默认为DEFAULT_GROUP
            
        Returns:
            bool: 是否删除成功
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Batch delete instance metadata is only supported in Nacos V2 API")
            return False
        
        path = "/nacos/v2/ns/instance/metadata/batch"
        
        data = {
            'serviceName': service_name,
            'groupName': group_name,
            'metadata': json.dumps(metadata)
        }
        
        if consistency_type:
            data['consistencyType'] = consistency_type
        
        if instances:
            data['instances'] = json.dumps(instances)
        
        response = await self._request('DELETE', path, data=data)
        if response:
            try:
                result = response.json()
                return result.get('data', False)
            except json.JSONDecodeError:
                return False
        return False
    
    async def create_service(self, service_name: str, group_name: str = "DEFAULT_GROUP", 
                      protect_threshold: float = 0.0, metadata: Dict = None, 
                      selector: Dict = None) -> bool:
        """
        创建服务
        
        Args:
            service_name: 服务名
            group_name: 分组名称，默认为DEFAULT_GROUP
            protect_threshold: 保护阈值，默认为0.0
            metadata: 元数据，默认为None
            selector: 访问策略，默认为None
            
        Returns:
            bool: 是否创建成功
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/service"
        else:  # v2
            path = "/nacos/v2/ns/service"
        
        data = {
            'serviceName': service_name,
            'groupName': group_name,
            'protectThreshold': protect_threshold
        }
        
        if metadata:
            # 将字典转换为JSON字符串
            data['metadata'] = json.dumps(metadata)
        
        if selector:
            # 将字典转换为JSON字符串
            data['selector'] = json.dumps(selector)
        
        response = await self._request('POST', path, data=data)
        if response:
            if self.version == "v1":
                return response.text == "ok"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    async def delete_service(self, service_name: str, group_name: str = "DEFAULT_GROUP") -> bool:
        """
        删除服务
        
        Args:
            service_name: 服务名
            group_name: 分组名称，默认为DEFAULT_GROUP
            
        Returns:
            bool: 是否删除成功
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/service"
        else:  # v2
            path = "/nacos/v2/ns/service"
        
        params = {
            'serviceName': service_name,
            'groupName': group_name
        }
        
        response = await self._request('DELETE', path, params=params)
        if response:
            if self.version == "v1":
                return response.text == "ok"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    async def update_service(self, service_name: str, group_name: str = "DEFAULT_GROUP",
                      protect_threshold: float = None, metadata: Dict = None,
                      selector: Dict = None) -> bool:
        """
        更新服务
        
        Args:
            service_name: 服务名
            group_name: 分组名称，默认为DEFAULT_GROUP
            protect_threshold: 保护阈值
            metadata: 元数据
            selector: 访问策略
            
        Returns:
            bool: 是否更新成功
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/service"
            method = 'POST'  # V1 API 使用 POST 更新服务
        else:  # v2
            path = "/nacos/v2/ns/service"
            method = 'PUT'  # V2 API 使用 PUT 更新服务
        
        data = {
            'serviceName': service_name,
            'groupName': group_name
        }
        
        if protect_threshold is not None:
            data['protectThreshold'] = protect_threshold
        
        if metadata:
            data['metadata'] = json.dumps(metadata)
        
        if selector:
            data['selector'] = json.dumps(selector)
        
        response = await self._request(method, path, data=data)
        if response:
            if self.version == "v1":
                return response.text == "ok"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    async def get_service(self, service_name: str, group_name: str = "DEFAULT_GROUP") -> Optional[Dict]:
        """
        查询服务详情
        
        Args:
            service_name: 服务名
            group_name: 分组名称，默认为DEFAULT_GROUP
            
        Returns:
            Dict: 服务详情
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/service"
        else:  # v2
            path = "/nacos/v2/ns/service"
        
        params = {
            'serviceName': service_name,
            'groupName': group_name
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                if self.version == "v1":
                    return response.json()
                else:  # v2
                    result = response.json()
                    return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def list_services(self, group_name: str = None, page_no: int = 1, page_size: int = 20) -> Optional[Dict]:
        """
        查询服务列表
        
        Args:
            group_name: 分组名称，默认为None
            page_no: 当前页，默认为1
            page_size: 页条目数，默认为20，最大为500
            
        Returns:
            Dict: 服务列表
        """
        if self.version == "v1":
            path = "/nacos/v1/ns/service/list"
        else:  # v2
            path = "/nacos/v2/ns/service/list"
        
        params = {
            'pageNo': page_no,
            'pageSize': page_size
        }
        
        if group_name:
            params['groupName'] = group_name
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                if self.version == "v1":
                    return response.json()
                else:  # v2
                    result = response.json()
                    return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def update_instance_health(self, service_name: str, ip: str, port: int, 
                            healthy: bool, cluster_name: str = "DEFAULT", 
                            group_name: str = "DEFAULT_GROUP") -> bool:
        """
                更新实例健康状态

                Args:
                    service_name: 服务名
                    ip: 实例IP
                    port: 实例端口
                    healthy: 是否健康
                    cluster_name: 集群名称，默认为DEFAULT
                    group_name: 分组名称，默认为DEFAULT_GROUP

                Returns:
                    bool: 是否更新成功
                """
        if self.version == "v1":
            path = "/nacos/v1/ns/instance/beat"
        else:  # v2
            path = "/nacos/v2/ns/instance/health"

        data = {
            'serviceName': service_name,
            'ip': ip,
            'port': port,
            'healthy': healthy,
            'clusterName': cluster_name,
            'groupName': group_name
        }

        response = await self._request('PUT', path, data=data)
        if response:
            if self.version == "v1":
                return response.text == "ok"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    # ================ 命名空间管理 API ================
    
    async def list_namespaces(self) -> Optional[List[Dict]]:
        """
        查询命名空间列表
        
        Returns:
            List[Dict]: 命名空间列表
        """
        if self.version == "v1":
            path = "/nacos/v1/console/namespaces"
        else:  # v2
            path = "/nacos/v2/console/namespace/list"
        
        response = await self._request('GET', path)
        if response:
            try:
                if self.version == "v1":
                    result = response.json()
                    return result.get('data')
                else:  # v2
                    result = response.json()
                    return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_namespace(self, namespace_id: str) -> Optional[Dict]:
        """
        查询具体命名空间
        
        Args:
            namespace_id: 命名空间ID
            
        Returns:
            Dict: 命名空间信息
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Get namespace detail is only supported in Nacos V2 API")
            # 尝试从列表中获取
            namespaces = await self.list_namespaces()
            if namespaces:
                for ns in namespaces:
                    if ns.get('namespace') == namespace_id:
                        return ns
            return None
        
        path = "/nacos/v2/console/namespace"
        params = {
            'namespaceId': namespace_id
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def create_namespace(self, namespace_id: str, namespace_name: str, 
                        namespace_desc: str = None) -> bool:
        """
        创建命名空间
        
        Args:
            namespace_id: 命名空间ID
            namespace_name: 命名空间名称
            namespace_desc: 命名空间描述，默认为None
            
        Returns:
            bool: 是否创建成功
        """
        if self.version == "v1":
            path = "/nacos/v1/console/namespaces"
        else:  # v2
            path = "/nacos/v2/console/namespace"
        
        data = {
            'customNamespaceId': namespace_id if self.version == "v1" else 'namespaceId',
            'namespaceName': namespace_name,
        }
        
        if namespace_desc:
            data['namespaceDesc'] = namespace_desc
        
        response = await self._request('POST', path, data=data)
        if response:
            if self.version == "v1":
                return response.text == "true"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    async def edit_namespace(self, namespace_id: str, namespace_name: str, 
                      namespace_desc: str = None) -> bool:
        """
        编辑命名空间
        
        Args:
            namespace_id: 命名空间ID
            namespace_name: 命名空间名称
            namespace_desc: 命名空间描述，默认为None
            
        Returns:
            bool: 是否编辑成功
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Edit namespace is only supported in Nacos V2 API")
            return False
        
        path = "/nacos/v2/console/namespace"
        
        data = {
            'namespaceId': namespace_id,
            'namespaceName': namespace_name
        }
        
        if namespace_desc:
            data['namespaceDesc'] = namespace_desc
        
        response = await self._request('PUT', path, data=data)
        if response:
            try:
                result = response.json()
                return result.get('data', False)
            except json.JSONDecodeError:
                return False
        return False
    
    async def delete_namespace(self, namespace_id: str) -> bool:
        """
        删除命名空间
        
        Args:
            namespace_id: 命名空间ID
            
        Returns:
            bool: 是否删除成功
        """
        if self.version == "v1":
            path = "/nacos/v1/console/namespaces"
        else:  # v2
            path = "/nacos/v2/console/namespace"
        
        if self.version == "v1":
            params = {
                'namespaceId': namespace_id
            }
            response = await self._request('DELETE', path, params=params)
        else:  # v2
            data = {
                'namespaceId': namespace_id
            }
            response = await self._request('DELETE', path, data=data)
        
        if response:
            if self.version == "v1":
                return response.text == "true"
            else:  # v2
                try:
                    result = response.json()
                    return result.get('data', False)
                except json.JSONDecodeError:
                    return False
        return False
    
    # ================ 配置历史 API ================
    
    async def get_config_history_list(self, data_id: str, group: str, 
                               page_no: int = 1, page_size: int = 100) -> Optional[Dict]:
        """
        查询配置历史列表
        
        Args:
            data_id: 配置ID
            group: 配置分组
            page_no: 当前页，默认为1
            page_size: 页条目数，默认为100，最大为500
            
        Returns:
            Dict: 配置历史列表
        """
        if self.version == "v1":
            path = "/nacos/v1/cs/history"
        else:  # v2
            path = "/nacos/v2/cs/history/list"
        
        params = {
            'dataId': data_id,
            'group': group,
            'pageNo': page_no,
            'pageSize': page_size
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                if self.version == "v1":
                    return response.json()
                else:  # v2
                    result = response.json()
                    return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_config_history_detail(self, data_id: str, group: str, nid: str) -> Optional[Dict]:
        """
        查询具体版本的历史配置
        
        Args:
            data_id: 配置ID
            group: 配置分组
            nid: 历史配置ID
            
        Returns:
            Dict: 历史配置详情
        """
        if self.version == "v1":
            path = "/nacos/v1/cs/history"
        else:  # v2
            path = "/nacos/v2/cs/history"
        
        params = {
            'dataId': data_id,
            'group': group,
            'nid': nid
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                if self.version == "v1":
                    return response.json()
                else:  # v2
                    result = response.json()
                    return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_previous_config_history(self, data_id: str, group: str, id: str) -> Optional[Dict]:
        """
        查询配置上一版本信息
        
        Args:
            data_id: 配置ID
            group: 配置分组
            id: 配置ID
            
        Returns:
            Dict: 上一版本配置详情
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Get previous config history is only supported in Nacos V2 API")
            return None
        
        path = "/nacos/v2/cs/history/previous"
        
        params = {
            'dataId': data_id,
            'group': group,
            'id': id
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    # ================ 客户端管理 API (仅 V2) ================
    
    async def list_clients(self) -> Optional[List[str]]:
        """
        查询客户端列表
        
        Returns:
            List[str]: 客户端ID列表
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("List clients is only supported in Nacos V2 API")
            return None
        
        path = "/nacos/v2/ns/client/list"
        
        response = await self._request('GET', path)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_client(self, client_id: str) -> Optional[Dict]:
        """
        查询客户端信息
        
        Args:
            client_id: 客户端ID
            
        Returns:
            Dict: 客户端信息
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Get client is only supported in Nacos V2 API")
            return None
        
        path = "/nacos/v2/ns/client"
        
        params = {
            'clientId': client_id
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_client_publish_list(self, client_id: str) -> Optional[List[Dict]]:
        """
        查询客户端的注册信息
        
        Args:
            client_id: 客户端ID
            
        Returns:
            List[Dict]: 客户端注册的服务列表
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Get client publish list is only supported in Nacos V2 API")
            return None
        
        path = "/nacos/v2/ns/client/publish/list"
        
        params = {
            'clientId': client_id
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_client_subscribe_list(self, client_id: str) -> Optional[List[Dict]]:
        """
        查询客户端的订阅信息
        
        Args:
            client_id: 客户端ID
            
        Returns:
            List[Dict]: 客户端订阅的服务列表
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Get client subscribe list is only supported in Nacos V2 API")
            return None
        
        path = "/nacos/v2/ns/client/subscribe/list"
        
        params = {
            'clientId': client_id
        }
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_service_publisher_list(self, service_name: str, group_name: str = "DEFAULT_GROUP",
                                  ip: str = None, port: int = None) -> Optional[List[Dict]]:
        """
        查询注册指定服务的客户端信息
        
        Args:
            service_name: 服务名
            group_name: 分组名称，默认为DEFAULT_GROUP
            ip: IP地址，默认为None，表示不限制IP地址
            port: 端口号，默认为None，表示不限制端口号
            
        Returns:
            List[Dict]: 客户端列表
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Get service publisher list is only supported in Nacos V2 API")
            return None
        
        path = "/nacos/v2/ns/client/service/publisher/list"
        
        params = {
            'serviceName': service_name,
            'groupName': group_name
        }
        
        if ip:
            params['ip'] = ip
        
        if port:
            params['port'] = port
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None
    
    async def get_service_subscriber_list(self, service_name: str, group_name: str = "DEFAULT_GROUP",
                                   ip: str = None, port: int = None) -> Optional[List[Dict]]:
        """
        查询订阅指定服务的客户端信息
        
        Args:
            service_name: 服务名
            group_name: 分组名称，默认为DEFAULT_GROUP
            ip: IP地址，默认为None，表示不限制IP地址
            port: 端口号，默认为None，表示不限制端口号
            
        Returns:
            List[Dict]: 客户端列表
        """
        # 仅 V2 API 支持此功能
        if self.version == "v1":
            logger.warning("Get service subscriber list is only supported in Nacos V2 API")
            return None
        
        path = "/nacos/v2/ns/client/service/subscriber/list"
        
        params = {
            'serviceName': service_name,
            'groupName': group_name
        }
        
        if ip:
            params['ip'] = ip
        
        if port:
            params['port'] = port
        
        response = await self._request('GET', path, params=params)
        if response:
            try:
                result = response.json()
                return result.get('data')
            except json.JSONDecodeError:
                return None
        return None

    async def _get_service_instance(self, service_name: str, group_name: str = "DEFAULT_GROUP",
                                    healthy_only: bool = True) -> Optional[Dict]:
        """
        获取服务实例，根据权重进行选择

        Args:
            service_name: 服务名称
            group_name: 服务分组
            healthy_only: 是否只返回健康实例

        Returns:
            Dict: 服务实例信息，包含 ip 和 port
        """
        instances = await self.list_instances(service_name, group_name=group_name)
        if not instances or not instances.get('hosts') or len(instances.get('hosts')) == 0:
            logger.warning(f"No instances found for service: {service_name}")
            return None

        # 筛选健康实例
        available_instances = []
        for instance in instances.get('hosts', []):
            if not healthy_only or instance.get('healthy', False):
                available_instances.append(instance)

        if not available_instances:
            logger.warning(f"No healthy instances found for service: {service_name}")
            return None
        # 基于权重选择实例
        return self._select_instance_by_weight(available_instances)

    @staticmethod
    def _select_instance_by_weight(instances: List[Dict]) -> Dict:
        """
        根据权重选择服务实例

        Args:
            instances: 可用的服务实例列表

        Returns:
            Dict: 选中的服务实例
        """
        if not instances:
            return None

        if len(instances) == 1:
            return instances[0]

        # 计算总权重
        total_weight = 0
        for instance in instances:
            # 获取权重，默认为1
            weight = instance.get('weight', 1)
            if weight <= 0:
                weight = 1
            total_weight += weight

        # 如果所有实例权重都相同，使用随机选择
        if all(instance.get('weight', 1) == instances[0].get('weight', 1) for instance in instances):
            import random
            return random.choice(instances)

        # 基于权重随机选择
        import random
        random_weight = random.uniform(0, total_weight)
        current_weight = 0

        for instance in instances:
            weight = instance.get('weight', 1)
            if weight <= 0:
                weight = 1
            current_weight += weight
            if current_weight >= random_weight:
                return instance

        # 如果由于浮点数精度问题没有选中，则返回最后一个实例
        return instances[-1]

    async def _call_service(self, service_name: str, path: str, method: str,
                            group_name: str = "DEFAULT_GROUP",
                            params: Dict = None, data: Dict = None,
                            headers: Dict = None, timeout: int = 30,
                            healthy_only: bool = True,**kwargs) -> Optional[Response]:
        """
        调用微服务

        Args:
            service_name: 服务名称
            path: 接口路径
            method: HTTP方法
            group_name: 服务分组
            params: 查询参数
            data: 请求体数据
            headers: 请求头
            timeout: 超时时间（秒）
            healthy_only: 是否只调用健康实例

        Returns:
            Response: HTTP响应对象
        """
        instance = await self._get_service_instance(service_name, group_name, healthy_only)
        if not instance:
            logger.error(f"Failed to get instance for service: {service_name}")
            return None

        ip = instance.get('ip')
        port = instance.get('port')

        # 构建完整URL
        url = f"http://{ip}:{port}{path}"
        logger.info(f"Calling service {service_name} at {url}")

        client = HttpClient()
        try:
            if method.upper() == "GET":
                return await client.get(url, timeout=timeout, headers=headers, params=params,**kwargs)
            elif method.upper() == "POST":
                return await client.post(url, timeout=timeout, headers=headers, params=params, data=data,**kwargs)
            elif method.upper() == "PUT":
                return await client.put(url, timeout=timeout, headers=headers, params=params, data=data,**kwargs)
            elif method.upper() == "DELETE":
                return await client.delete(url, timeout=timeout, headers=headers, params=params, data=data,**kwargs)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None
        except Exception as e:
            logger.error(f"Error calling service {service_name}: {str(e)}")
            return None

    async def get(self, service_name: str, path: str, group_name: str = "DEFAULT_GROUP",
                  params: Dict = None, headers: Dict = None,
                  timeout: int = 30,**kwargs) -> Optional[Response]:
        """
        向微服务发送GET请求

        Args:
            service_name: 服务名称
            path: 接口路径
            group_name: 服务分组
            params: 查询参数
            headers: 请求头
            timeout: 超时时间（秒）

        Returns:
            Response: HTTP响应对象
        """
        return await self._call_service(
            service_name=service_name,
            path=path,
            method="GET",
            group_name=group_name,
            params=params,
            headers=headers,
            timeout=timeout,**kwargs
        )

    async def post(self, service_name: str, path: str, data: Dict = None,
                   group_name: str = "DEFAULT_GROUP", params: Dict = None,
                   headers: Dict = None, timeout: int = 30,**kwargs) -> Optional[Response]:
        """
        向微服务发送POST请求

        Args:
            service_name: 服务名称
            path: 接口路径
            data: 请求体数据
            group_name: 服务分组
            params: 查询参数
            headers: 请求头
            timeout: 超时时间（秒）

        Returns:
            Response: HTTP响应对象
        """
        return await self._call_service(
            service_name=service_name,
            path=path,
            method="POST",
            group_name=group_name,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout,
            **kwargs
        )

    async def put(self, service_name: str, path: str, data: Dict = None,
                  group_name: str = "DEFAULT_GROUP", params: Dict = None,
                  headers: Dict = None, timeout: int = 30,**kwargs) -> Optional[Response]:
        """
        向微服务发送PUT请求

        Args:
            service_name: 服务名称
            path: 接口路径
            data: 请求体数据
            group_name: 服务分组
            params: 查询参数
            headers: 请求头
            timeout: 超时时间（秒）

        Returns:
            Response: HTTP响应对象
        """
        return await self._call_service(
            service_name=service_name,
            path=path,
            method="PUT",
            group_name=group_name,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout,**kwargs
        )

    async def delete(self, service_name: str, path: str, data: Dict = None,
                     group_name: str = "DEFAULT_GROUP", params: Dict = None,
                     headers: Dict = None, timeout: int = 30,**kwargs) -> Optional[Response]:
        """
        向微服务发送DELETE请求

        Args:
            service_name: 服务名称
            path: 接口路径
            data: 请求体数据
            group_name: 服务分组
            params: 查询参数
            headers: 请求头
            timeout: 超时时间（秒）

        Returns:
            Response: HTTP响应对象
        """
        return await self._call_service(
            service_name=service_name,
            path=path,
            method="DELETE",
            group_name=group_name,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout,**kwargs
        )

    async def request(self, service_name: str, path: str, method: str,
                      data: Dict = None, group_name: str = "DEFAULT_GROUP",
                      params: Dict = None, headers: Dict = None,
                      timeout: int = 30,**kwargs) -> Optional[Response]:
        """
        向微服务发送自定义HTTP请求

        Args:
            service_name: 服务名称
            path: 接口路径
            method: HTTP方法
            data: 请求体数据
            group_name: 服务分组
            params: 查询参数
            headers: 请求头
            timeout: 超时时间（秒）

        Returns:
            Response: HTTP响应对象
        """
        return await self._call_service(
            service_name=service_name,
            path=path,
            method=method,
            group_name=group_name,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout,**kwargs
        )