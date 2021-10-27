from enum import Enum
from typing import Dict, List


class Flags(Enum):
    WEBSOCKET_CONNECT = 0

    CONTROL_CONSOLE = 1
    CONTROL_START = 2
    CONTROL_STOP = 3
    CONTROL_RESTART = 4

    USER_CREATE = 5
    USER_READ = 6
    USER_UPDATE = 7
    USER_DELETE = 8

    FILE_CREATE = 9
    FILE_READ = 10
    FILE_UPDATE = 11
    FILE_DELETE = 12
    FILE_ARCHIVE = 13
    FILE_SFTP = 14

    BACKUP_CREATE = 15
    BACKUP_READ = 16
    BACKUP_UPDATE = 17
    BACKUP_DELETE = 18

    ALLOCATION_READ = 19
    ALLOCATION_CREATE = 20
    ALLOCATION_UPDATE = 21
    ALLOCATION_DELETE = 22

    STARTUP_READ = 23
    STARTUP_UPDATE = 24

    DATABASE_CREATE = 25
    DATABASE_READ = 26
    DATABASE_UPDATE = 27
    DATABASE_DELETE = 28
    DATABASE_VIEW_PASSWORD = 29

    SCHEDULE_CREATE = 30
    SCHEDULE_READ = 31
    SCHEDULE_UPDATE = 32
    SCHEDULE_DELETE = 33

    SETTINGS_RENAME = 34
    SETTINGS_REINSTALL = 35

    ADMIN_WEBSOCKET_ERRORS = 41
    ADMIN_WEBSOCKET_INSTALL = 42
    ADMIN_WEBSOCKET_TRANSFER = 43

    def __dict__(cls) -> Dict[str, int]:
        return { k: getattr(cls, k) for k in dir(cls) if k.isupper() }


def diff(perms: list) -> bool:
    base = type(perms[0])
    for p in perms:
        if not isinstance(p, base):
            return True
    
    return False

class Permissions:
    def __init__(self, data) -> None:
        self.raw = self.resolve(self, data)
    
    def has(self, perm: object) -> bool:
        return perm in self.raw
    
    def is_admin(self) -> bool:
        for f in self.to_list():
            if 'ADMIN' in f:
                return True
        
        return False
    
    @staticmethod
    def resolve(cls, perms: object) -> Dict[str, int]:
        if isinstance(perms, dict):
            perms = [k for k in perms.keys()]
        
        if len(perms) == 0:
            return {}
        
        if diff(perms):
            raise TypeError('permissions must be all strings or all ints')
        
        keys = dict(Flags)
        vals = { keys[k]: k for k in keys.keys() }
        res = {}
        for p in perms:
            if keys.get(p):
                res[p] = keys[p]
            elif vals.get(p):
                res[vals[p]] = p
            else:
                raise KeyError(f"unknown permission '{p}'")
        
        return res
    
    def serialize(self) -> Dict[str, bool]:
        return { k: bool(self.raw.get(k)) for k in dict(Flags) }
    
    def to_list(self) -> List[str]:
        return [k for k in self.raw]
    
    def to_strings(self) -> List[str]:
        return [f.lower().replace('_', '.') for f in self.to_list()]
    
    @staticmethod
    def from_strings(cls, perms: List[str]) -> Dict[str, int]:
        keys = dict(Flags)
        res = {}
        for p in perms:
            p = p.lower().replace('.', '_')
            if keys.get(p):
                res[p] = keys[p]
            else:
                raise KeyError(f"unknown permission '{p}'")
        
        return res
