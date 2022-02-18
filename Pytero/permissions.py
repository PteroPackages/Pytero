from enum import Enum


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

    @staticmethod
    def get_string_keys() -> list[str]:
        return list(Flags.__members__.keys())
    
    @staticmethod
    def get_key_values() -> list[int]:
        return [k.value for k in Flags.__members__.values()]


def diff(perms: list) -> bool:
    base = type(perms[0])
    for p in perms:
        if not isinstance(p, base):
            return True
    
    return False

class Permissions:
    def __init__(self, data: dict[str, int] | list[str] | list[int]) -> None:
        self.raw = self.resolve(data)
    
    def __repr__(self) -> str:
        return '<Permissions total=%d>' % len(self.raw)
    
    def __len__(self) -> int:
        return len(self.raw)
    
    def __contains__(self, perm: str):
        return self.has(perm)
    
    def has(self, perm: str) -> bool:
        # TODO: resolve
        return perm in self.raw
    
    def is_admin(self) -> bool:
        for f in self.to_list():
            if 'ADMIN' in f:
                return True
        
        return False
    
    @staticmethod
    def resolve(perms: object) -> dict[str, int]:
        if isinstance(perms, dict):
            perms = [k for k in perms.keys()]
        
        if len(perms) == 0:
            return {}
        
        if diff(perms):
            raise TypeError('permissions must be all strings or all ints')
        
        keys = dict(zip(Flags.get_string_keys(), Flags.get_key_values()))
        vals = {keys[k]: k for k in keys}
        res = {}
        for p in perms:
            if keys.get(p):
                res[p] = keys[p]
            elif vals.get(p):
                res[vals[p]] = p
            else:
                raise KeyError(f"unknown permission '{p}'")
        
        return res
    
    def serialize(self) -> dict[str, bool]:
        return {k: k in self.raw for k in Flags.get_string_keys()}
    
    def to_list(self) -> list[str]:
        return [k for k in self.raw]
    
    def to_strings(self) -> list[str]:
        return [f.lower().replace('_', '.') for f in self.to_list()]
    
    @staticmethod
    def from_strings(perms: list[str]) -> dict[str, int]:
        keys = dict(zip(Flags.get_string_keys(), Flags.get_key_values()))
        res = {}
        for p in perms:
            p = p.upper().replace('.', '_')
            if keys.get(p):
                res[p] = keys[p]
            else:
                raise KeyError(f"unknown permission '{p}'")
        
        return res
