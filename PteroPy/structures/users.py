from typing import List


class BaseUser:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        self.username: str
        self.email: str
        self.firstname: str
        self.lastname: str
        self.language: str
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.username = data.get('username', self.username)
        self.email = data.get('email'. self.email)
        self.firstname = data.get('firstname', self.firstname)
        self.lastname = data.get('lastname', self.lastname)
        self.language = data.get('language', self.language)
    
    def __str__(self) -> str:
        return self.firstname +' '+ self.lastname
    
    def __repr__(self) -> str:
        return '<%s %d>' % (self.__class__.__name__, self.id)


class PteroUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        
        self.uuid: str = data['uuid']
        self.created_at: str = data['created_at']
        self.external_id: str
        self.is_admin: bool
        self.tfa: bool
        self.updated_at: str
        self.relationships = NotImplemented
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        
        self.external_id = data.get('external_id', self.external_id)
        self.is_admin = data.get('is_admin', self.is_admin)
        self.tfa = data.get('2fa', self.tfa)
        self.updated_at = data.get('updated_at', self.updated_at)
    
    def update(self):
        return NotImplemented
    
    def delete(self):
        return NotImplemented


class PteroSubUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        
        self.uuid: str = data['uuid']
        self.image: str
        self.enabled: bool
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        
        self.image = data.get('image', self.image)
        self.enabled = data.get('2fa_enabled', self.enabled)
    
    def set_permissions(data: object):
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
