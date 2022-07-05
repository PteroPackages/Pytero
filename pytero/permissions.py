from enum import Enum


__all__ = ('Flags', 'Permissions')

class Flags(Enum):
    WEBSOCKET_CONNECT = 'websocket.connect'

    CONTROL_CONSOLE = 'control.console'
    CONTROL_START = 'control.start'
    CONTROL_STOP = 'control.stop'
    CONTROL_RESTART = 'control.restart'

    USER_CREATE = 'user.create'
    USER_READ = 'user.read'
    USER_UPDATE = 'user.update'
    USER_DELETE = 'user.delete'

    FILE_CREATE = 'file.create'
    FILE_READ = 'file.read'
    FILE_READ_CONTENT = 'file.read-content'
    FILE_UPDATE = 'file.update'
    FILE_DELETE = 'file.delete'
    FILE_ARCHIVE = 'file.archive'
    FILE_SFTP = 'file.sftp'

    BACKUP_CREATE = 'backup.create'
    BACKUP_READ = 'backup.read'
    BACKUP_UPDATE = 'backup.update'
    BACKUP_DELETE = 'backup.delete'

    ALLOCATION_READ = 'allocation.read'
    ALLOCATION_CREATE = 'allocation.create'
    ALLOCATION_UPDATE = 'allocation.update'
    ALLOCATION_DELETE = 'allocation.delete'

    STARTUP_READ = 'startup.read'
    STARTUP_UPDATE = 'sartup.update'

    DATABASE_CREATE = 'database.create'
    DATABASE_READ = 'database.read'
    DATABASE_UPDATE = 'database.update'
    DATABASE_DELETE = 'database.delete'
    DATABASE_VIEW_PASSWORD = 'database.view_password'

    SCHEDULE_CREATE = 'schedule.create'
    SCHEDULE_READ = 'schedule.read'
    SCHEDULE_UPDATE = 'schedule.update'
    SCHEDULE_DELETE = 'schedule.delete'

    SETTINGS_RENAME = 'settings.rename'
    SETTINGS_REINSTALL = 'settings.reinstall'

    ADMIN_WEBSOCKET_ERRORS = 'admin.websocket.errors'
    ADMIN_WEBSOCKET_INSTALL = 'admin.websocket.install'
    ADMIN_WEBSOCKET_TRANSFER = 'admin.websocket.transfer'

    def __contains__(self, key: str) -> bool:
        return super().__contains__(key)

    @staticmethod
    def values(cls) -> list[str]:
        return [p.value for p in Flags.__members__.values()]


class Permissions:
    ALL_CONSOLE = (
        Flags.CONTROL_CONSOLE,
        Flags.CONTROL_START,
        Flags.CONTROL_STOP,
        Flags.CONTROL_RESTART
    )
    ALL_USER = (
        Flags.USER_CREATE,
        Flags.USER_READ,
        Flags.USER_UPDATE,
        Flags.USER_DELETE
    )
    ALL_FILE = (
        Flags.FILE_CREATE,
        Flags.FILE_READ,
        Flags.FILE_READ_CONTENT,
        Flags.FILE_UPDATE,
        Flags.FILE_ARCHIVE,
        Flags.FILE_SFTP
    )
    ALL_BACKUP = (
        Flags.BACKUP_CREATE,
        Flags.BACKUP_READ,
        Flags.BACKUP_UPDATE,
        Flags.BACKUP_DELETE
    )
    ALL_ALLOCATION = (
        Flags.ALLOCATION_CREATE,
        Flags.ALLOCATION_READ,
        Flags.ALLOCATION_UPDATE,
        Flags.ALLOCATION_DELETE
    )
    ALL_STARTUP = (Flags.STARTUP_READ, Flags.STARTUP_UPDATE)
    ALL_DATABASE = (
        Flags.DATABASE_CREATE,
        Flags.DATABASE_READ,
        Flags.DATABASE_UPDATE,
        Flags.DATABASE_DELETE,
        Flags.DATABASE_VIEW_PASSWORD
    )
    ALL_SCHEDULE = (
        Flags.SCHEDULE_CREATE,
        Flags.SCHEDULE_READ,
        Flags.SCHEDULE_UPDATE,
        Flags.SCHEDULE_DELETE
    )
    ALL_SETTINGS = (Flags.SETTINGS_RENAME, Flags.SETTINGS_REINSTALL)
    ALL_ADMIN = (
        Flags.ADMIN_WEBSOCKET_ERRORS,
        Flags.ADMIN_WEBSOCKET_INSTALL,
        Flags.ADMIN_WEBSOCKET_TRANSFER
    )
    
    def __init__(self, *perms: str | Flags) -> None:
        self.value: list[str] = self.resolve(*perms)
    
    @staticmethod
    def resolve(*perms: str | Flags) -> list[str]:
        res: list[str] = []
        
        for perm in perms:
            match type(perm).__name__:
                case 'Flags':
                    res.append(perm.value)
                case 'str':
                    if perm in Flags:
                        res.append(perm)
                    else:
                        raise KeyError('Invalid permission or flag')
                case _:
                    raise KeyError('Invalid permission or flag')
        
        return res
    
    def __repr__(self) -> str:
        return '<Permissions total=%d>' % len(self.value)
    
    def __len__(self) -> int:
        return len(self.value)
    
    def __contains__(self, perm: str):
        return perm in self.value
    
    def any(self, *perms) -> bool:
        res = self.__class__.resolve(*perms)
        for perm in self.value:
            if perm in res:
                return True
        
        return False
    
    def all(self, *perms) -> bool:
        res = self.__class__.resolve(*perms)
        for perm in self.value:
            if perm not in res:
                return False
        
        return True
    
    def is_admin(self) -> bool:
        return any(filter(lambda p: 'admin' in p, self.value))
    
    def serialize(self) -> dict[str, bool]:
        return {k: k in self.value for k in Flags.values()}
