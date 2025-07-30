import json
import requests
from typing import Dict, List, Optional, Union, Any

from .models import (
    BaseResponse, ProxyInfo, ProxyConfig, Task, TaskCheckReq,
    TaskCreateReq, TaskReceiveReq, TaskReceiveResp, TaskReceiveListReq,
    TaskReceiveListResp, TaskUpdateWindowInfoReq, UserLoginResp,
    ClientUser, WorkingTime
)


class FlyWingClient:
    """FlyWing广告系统API客户端"""
    
    def __init__(self, host: str = "localhost", port: int = 8080, token: Optional[str] = None):
        """
        初始化FlyWing API客户端
        
        Args:
            host: API主机地址
            port: API端口号
            token: 认证令牌（如果需要）
        """
        self.base_url = f"http://{host}:{port}"
        self.token = token
        self.headers = {
            "Content-Type": "application/json"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    def _post(self, endpoint: str, data: Dict = None) -> Dict:
        """
        发送POST请求到API
        
        Args:
            endpoint: API端点（不带前导斜杠）
            data: 请求数据（将转换为JSON）
            
        Returns:
            响应数据字典
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data or {})
        response.raise_for_status()
        return response.json()
    
    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        """
        发送GET请求到API
        
        Args:
            endpoint: API端点（不带前导斜杠）
            params: 请求参数
            
        Returns:
            响应数据字典
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json()
    
    # 用户管理API
    def login(self, username: str, password: str) -> UserLoginResp:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            UserLoginResp对象
        """
        params = {
            "username": username,
            "password": password
        }
        response_data = self._post("api/user/login", params)
        return UserLoginResp.from_dict(response_data)
    
    def register(self, username: str, password: str, mac_id: Optional[str] = None, device_info: Optional[str] = None) -> UserLoginResp:
        """
        用户注册
        
        Args:
            username: 用户名
            password: 密码
            mac_id: MAC地址ID
            device_info: 设备信息
            
        Returns:
            UserLoginResp对象
        """
        data = {
            "username": username,
            "password": password
        }
        if mac_id:
            data["macId"] = mac_id
        if device_info:
            data["deviceInfo"] = device_info
            
        response_data = self._post("api/user/register", data)
        return UserLoginResp.from_dict(response_data)
    
    def get_user_info(self) -> ClientUser:
        """
        获取用户信息
        
        Returns:
            ClientUser对象
        """
        response_data = self._get("api/user/userinfo")
        return ClientUser.from_dict(response_data)
    
    # 代理管理API
    def get_proxy_config_list(self) -> List[ProxyConfig]:
        """
        获取代理配置列表
        
        Returns:
            ProxyConfig对象列表
        """
        response_data = self._get("api/proxy/list")
        return [ProxyConfig.from_dict(item) for item in response_data]
    
    def get_proxy_config_by_id(self, proxy_id: int) -> ProxyConfig:
        """
        根据ID获取代理配置
        
        Args:
            proxy_id: 代理配置ID
            
        Returns:
            ProxyConfig对象
        """
        response_data = self._get(f"api/proxy/{proxy_id}")
        return ProxyConfig.from_dict(response_data)
    
    def gen_proxy(self, proxy_id: int, count: int) -> List[ProxyInfo]:
        """
        生成代理
        
        Args:
            proxy_id: 代理配置ID
            count: 生成数量
            
        Returns:
            ProxyInfo对象列表
        """
        response_data = self._get(f"api/proxy/genProxy/{proxy_id}/{count}")
        return [ProxyInfo.from_dict(item) for item in response_data]
    
    # 任务管理API
    def create_task(self, task_req: TaskCreateReq) -> Task:
        """
        创建任务
        
        Args:
            task_req: 任务创建请求对象
            
        Returns:
            Task对象
        """
        response_data = self._post("api/task/create", task_req.to_dict())
        return Task.from_dict(response_data)
    
    def check_task(self, task_check_req: TaskCheckReq) -> Task:
        """
        检查任务
        
        Args:
            task_check_req: 任务检查请求对象
            
        Returns:
            Task对象
        """
        response_data = self._post("api/task/check", task_check_req.to_dict())
        return Task.from_dict(response_data)
    
    def receive_task(self, task_receive_req: TaskReceiveReq) -> TaskReceiveResp:
        """
        接收任务
        
        Args:
            task_receive_req: 任务接收请求对象
            
        Returns:
            TaskReceiveResp对象
        """
        response_data = self._post("api/task/receive", task_receive_req.to_dict())
        return TaskReceiveResp.from_dict(response_data)
    
    def get_task_list(self, task_receive_list_reqs: List[TaskReceiveListReq]) -> List[TaskReceiveListResp]:
        """
        获取任务列表
        
        Args:
            task_receive_list_reqs: 任务接收列表请求对象列表
            
        Returns:
            TaskReceiveListResp对象列表
        """
        data = [req.to_dict() for req in task_receive_list_reqs]
        response_data = self._post("api/task/receive/list", data)
        return [TaskReceiveListResp.from_dict(item) for item in response_data]
    
    def update_window_info(self, task_update_window_info_req: TaskUpdateWindowInfoReq) -> int:
        """
        更新窗口信息
        
        Args:
            task_update_window_info_req: 任务窗口信息更新请求对象
            
        Returns:
            更新结果（整数）
        """
        response_data = self._post("api/task/receive/update_window", task_update_window_info_req.to_dict())
        return response_data
    
    def update_complete_info(self, task_id: int) -> BaseResponse:
        """
        更新完成信息
        
        Args:
            task_id: 任务ID
            
        Returns:
            BaseResponse对象
        """
        response_data = self._post(f"api/task/receive/update/complete/{task_id}")
        return BaseResponse(success=True if response_data == 200 else False)
    
    # 工作时间管理API
    def get_all_working_times(self) -> List[WorkingTime]:
        """
        获取所有工作时间
        
        Returns:
            WorkingTime对象列表
        """
        response_data = self._get("api/working-time/all")
        return [WorkingTime.from_dict(item) for item in response_data]