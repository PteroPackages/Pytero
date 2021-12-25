from .permissions import PermissionResolvable
from typing import Optional, List


class BaseUser:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.username: str = data.get('username')
        self.email: str = data.get('email')
        self.firstname: str = data.get('firstname')
        self.lastname: str = data.get('lastname')
        self.language: str = data.get('language')
    
    def __str__(self) -> str:
        return self.firstname +' '+ self.lastname
    
    def __repr__(self) -> str:
        return '<%s id=%d firstname=%s lastname=%s>' % (
            self.__class__.__name__, self.id, self.firstname, self.lastname
        )


class PteroUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        
        self.uuid: str = data['uuid']
        self.created_at: str = data['created_at']
        self.relationships = NotImplemented
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        
        self.external_id: Optional[str] = data.get('external_id', None)
        self.is_admin: bool = data.get('is_admin', False)
        self.two_factor: bool = data.get('2fa', False)
        self.updated_at: float = data.get('updated_at', 0.0)
    
    def update(self):
        return NotImplemented
    
    def delete(self):
        return NotImplemented


class PteroSubUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        
        self.uuid: str = data['uuid']
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        
        self.image: Optional[str] = data.get('image', None)
        self.enabled: bool = data.get('2fa_enabled', False)
    
    def set_permissions(data: PermissionResolvable):
        return NotImplemented


class ClientUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        super().__patch(data)
        
        self.is_admin: bool = data['is_admin']
        self.tokens: List[str] = []
        self.apikeys: List[str] = []
    
    def get_2fa_code(self):
        return NotImplemented
    
    def enable_2fa(self, code: str):
        return NotImplemented
    
    def disable_2fa(self, password: str):
        return NotImplemented
    
    def update_email(self, email: str, password: str):
        return NotImplemented
    
    def update_password(self, old_pass: str, new_pass: str):
        return NotImplemented
    
    def fetch_keys(self):
        return NotImplemented
    
    def create_key(self):
        return NotImplemented
    
    def delete_key(self, key: str):
        return NotImplemented
