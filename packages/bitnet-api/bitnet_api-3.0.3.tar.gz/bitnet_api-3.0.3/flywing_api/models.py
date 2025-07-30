from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseResponse:
    """所有API响应的基类"""
    success: bool
    msg: Optional[str] = None


@dataclass
class ProxyInfo:
    """代理信息模型"""
    host: Optional[str] = None
    port: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    proxyMethod: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProxyInfo':
        """从字典创建ProxyInfo对象"""
        return cls(
            host=data.get('host'),
            port=data.get('port'),
            user=data.get('user'),
            password=data.get('password'),
            proxyMethod=data.get('proxyMethod')
        )
    
    def to_dict(self) -> Dict:
        """转换为字典用于API请求"""
        result = {}
        if self.host is not None:
            result['host'] = self.host
        if self.port is not None:
            result['port'] = self.port
        if self.user is not None:
            result['user'] = self.user
        if self.password is not None:
            result['password'] = self.password
        if self.proxyMethod is not None:
            result['proxyMethod'] = self.proxyMethod
        return result


@dataclass
class ProxyConfig:
    """代理配置模型"""
    id: Optional[int] = None
    proxyName: Optional[str] = None
    proxyType: Optional[str] = None
    account: Optional[str] = None
    apiUrl: Optional[str] = None
    balance: Optional[float] = None
    validTime: Optional[int] = None
    status: Optional[bool] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProxyConfig':
        """从字典创建ProxyConfig对象"""
        return cls(
            id=data.get('id'),
            proxyName=data.get('proxyName'),
            proxyType=data.get('proxyType'),
            account=data.get('account'),
            apiUrl=data.get('apiUrl'),
            balance=data.get('balance'),
            validTime=data.get('validTime'),
            status=data.get('status')
        )


@dataclass
class Task:
    """任务模型"""
    id: Optional[int] = None
    taskName: Optional[str] = None
    description: Optional[str] = None
    groupId: Optional[str] = None
    groupName: Optional[str] = None
    proxyConfigId: Optional[int] = None
    proxyConfigName: Optional[str] = None
    openUrl: Optional[str] = None
    autoCookie: Optional[bool] = None
    startTime: Optional[datetime] = None
    status: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """从字典创建Task对象"""
        start_time = None
        if data.get('startTime'):
            try:
                start_time = datetime.fromisoformat(data.get('startTime').replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return cls(
            id=data.get('id'),
            taskName=data.get('taskName'),
            description=data.get('description'),
            groupId=data.get('groupId'),
            groupName=data.get('groupName'),
            proxyConfigId=data.get('proxyConfigId'),
            proxyConfigName=data.get('proxyConfigName'),
            openUrl=data.get('openUrl'),
            autoCookie=data.get('autoCookie'),
            startTime=start_time,
            status=data.get('status')
        )


@dataclass
class TaskCheckReq:
    """任务检查请求"""
    taskId: int
    
    def to_dict(self) -> Dict:
        """转换为字典用于API请求"""
        return {
            'taskId': self.taskId
        }


@dataclass
class TaskCreateReq:
    """任务创建请求"""
    taskName: str
    description: Optional[str] = None
    groupId: Optional[str] = None
    proxyConfigId: Optional[int] = None
    openUrl: Optional[str] = None
    autoCookie: Optional[bool] = None
    
    def to_dict(self) -> Dict:
        """转换为字典用于API请求"""
        result = {
            'taskName': self.taskName
        }
        if self.description is not None:
            result['description'] = self.description
        if self.groupId is not None:
            result['groupId'] = self.groupId
        if self.proxyConfigId is not None:
            result['proxyConfigId'] = self.proxyConfigId
        if self.openUrl is not None:
            result['openUrl'] = self.openUrl
        if self.autoCookie is not None:
            result['autoCookie'] = self.autoCookie
        return result


@dataclass
class TaskReceiveReq:
    """任务接收请求"""
    taskId: int
    
    def to_dict(self) -> Dict:
        """转换为字典用于API请求"""
        return {
            'taskId': self.taskId
        }


@dataclass
class TaskReceiveResp:
    """任务接收响应"""
    id: Optional[int] = None
    taskId: Optional[int] = None
    taskName: Optional[str] = None
    openUrl: Optional[str] = None
    proxyInfo: Optional[ProxyInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TaskReceiveResp':
        """从字典创建TaskReceiveResp对象"""
        proxy_info = None
        if data.get('proxyInfo'):
            proxy_info = ProxyInfo.from_dict(data.get('proxyInfo'))
            
        return cls(
            id=data.get('id'),
            taskId=data.get('taskId'),
            taskName=data.get('taskName'),
            openUrl=data.get('openUrl'),
            proxyInfo=proxy_info
        )


@dataclass
class TaskReceiveListReq:
    """任务接收列表请求"""
    taskId: int
    
    def to_dict(self) -> Dict:
        """转换为字典用于API请求"""
        return {
            'taskId': self.taskId
        }


@dataclass
class TaskReceiveListResp:
    """任务接收列表响应"""
    id: Optional[int] = None
    taskId: Optional[int] = None
    taskName: Optional[str] = None
    openUrl: Optional[str] = None
    proxyInfo: Optional[ProxyInfo] = None
    windowInfo: Optional[str] = None
    completeTime: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TaskReceiveListResp':
        """从字典创建TaskReceiveListResp对象"""
        proxy_info = None
        if data.get('proxyInfo'):
            proxy_info = ProxyInfo.from_dict(data.get('proxyInfo'))
            
        complete_time = None
        if data.get('completeTime'):
            try:
                complete_time = datetime.fromisoformat(data.get('completeTime').replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return cls(
            id=data.get('id'),
            taskId=data.get('taskId'),
            taskName=data.get('taskName'),
            openUrl=data.get('openUrl'),
            proxyInfo=proxy_info,
            windowInfo=data.get('windowInfo'),
            completeTime=complete_time
        )


@dataclass
class TaskUpdateWindowInfoReq:
    """任务窗口信息更新请求"""
    id: int
    windowInfo: str
    
    def to_dict(self) -> Dict:
        """转换为字典用于API请求"""
        return {
            'id': self.id,
            'windowInfo': self.windowInfo
        }


@dataclass
class UserLoginResp:
    """用户登录响应"""
    token: Optional[str] = None
    user: Optional['ClientUser'] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserLoginResp':
        """从字典创建UserLoginResp对象"""
        user = None
        if data.get('user'):
            user = ClientUser.from_dict(data.get('user'))
            
        return cls(
            token=data.get('token'),
            user=user
        )


@dataclass
class ClientUser:
    """客户端用户模型"""
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    macId: Optional[str] = None
    deviceInfo: Optional[str] = None
    changeMacIdCount: Optional[int] = None
    isAdmin: Optional[bool] = None
    status: Optional[bool] = None
    createDate: Optional[datetime] = None
    updateDate: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ClientUser':
        """从字典创建ClientUser对象"""
        create_date = None
        if data.get('createDate'):
            try:
                create_date = datetime.fromisoformat(data.get('createDate').replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        update_date = None
        if data.get('updateDate'):
            try:
                update_date = datetime.fromisoformat(data.get('updateDate').replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            password=data.get('password'),
            macId=data.get('macId'),
            deviceInfo=data.get('deviceInfo'),
            changeMacIdCount=data.get('changeMacIdCount'),
            isAdmin=data.get('isAdmin'),
            status=data.get('status'),
            createDate=create_date,
            updateDate=update_date
        )


@dataclass
class WorkingTime:
    """工作时间模型"""
    id: Optional[int] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'WorkingTime':
        """从字典创建WorkingTime对象"""
        return cls(
            id=data.get('id'),
            startTime=data.get('startTime'),
            endTime=data.get('endTime')
        )