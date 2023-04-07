"""Permissions definitions for the Pterodactyl API."""

from enum import Enum
from typing import TypeVar


__all__ = ('Flags', 'Permissions')

P = TypeVar('P', bound='Permissions')


class Flags(Enum):
    """An enum class containing all the permission keys for the API."""

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

    # FIX THIS IMMEDIATELY!!!
    def values(self) -> list[str]:
        return [p.value for p in Flags.__members__.values()]


class Permissions:
    """The base class for managing permissions with the API."""

    ALL_CONSOLE = (
        Flags.CONTROL_CONSOLE,
        Flags.CONTROL_START,
        Flags.CONTROL_STOP,
        Flags.CONTROL_RESTART)

    ALL_USER = (
        Flags.USER_CREATE,
        Flags.USER_READ,
        Flags.USER_UPDATE,
        Flags.USER_DELETE)

    ALL_FILE = (
        Flags.FILE_CREATE,
        Flags.FILE_READ,
        Flags.FILE_READ_CONTENT,
        Flags.FILE_UPDATE,
        Flags.FILE_ARCHIVE,
        Flags.FILE_SFTP)

    ALL_BACKUP = (
        Flags.BACKUP_CREATE,
        Flags.BACKUP_READ,
        Flags.BACKUP_UPDATE,
        Flags.BACKUP_DELETE)

    ALL_ALLOCATION = (
        Flags.ALLOCATION_CREATE,
        Flags.ALLOCATION_READ,
        Flags.ALLOCATION_UPDATE,
        Flags.ALLOCATION_DELETE)

    ALL_STARTUP = (Flags.STARTUP_READ, Flags.STARTUP_UPDATE)

    ALL_DATABASE = (
        Flags.DATABASE_CREATE,
        Flags.DATABASE_READ,
        Flags.DATABASE_UPDATE,
        Flags.DATABASE_DELETE,
        Flags.DATABASE_VIEW_PASSWORD)

    ALL_SCHEDULE = (
        Flags.SCHEDULE_CREATE,
        Flags.SCHEDULE_READ,
        Flags.SCHEDULE_UPDATE,
        Flags.SCHEDULE_DELETE)

    ALL_SETTINGS = (Flags.SETTINGS_RENAME, Flags.SETTINGS_REINSTALL)

    ALL_ADMIN = (
        Flags.ADMIN_WEBSOCKET_ERRORS,
        Flags.ADMIN_WEBSOCKET_INSTALL,
        Flags.ADMIN_WEBSOCKET_TRANSFER)

    def __init__(self, *perms: str | Flags) -> None:
        self.value: list[str] = self.resolve(*perms)

    def __repr__(self) -> str:
        return f'<Permissions total={len(self.value)}>'

    def __len__(self) -> int:
        return len(self.value)

    def __bool__(self) -> bool:
        return len(self.value) != 0

    def __contains__(self, perm: str):
        return perm in self.value

    def __eq__(self, other: P) -> bool:
        return self.value == other.value

    def __add__(self, other: P) -> P:
        return Permissions(*(self.value + other.value))

    def __sub__(self, other: P) -> P:
        perms = list(filter(lambda p: p not in other.value, self.value))
        return Permissions(*perms)

    @staticmethod
    def resolve(*perms: str | Flags) -> list[str]:
        """Resolves the given permissions into a list of valid API permissions.

        perms: tuple[:class:`str` | :class:`Flags`]
            A tuple of strings or permission flags.
        """
        res: list[str] = []
        flags = Flags.values(Flags)

        for perm in perms:
            if isinstance(perm, Flags):
                res.append(perm.value)
            elif perm in flags:
                res.append(perm)
            else:
                raise KeyError(f"invalid permission or flag '{perm}'")

        return res

    def any(self, *perms: str | Flags) -> bool:
        """Returns ``True`` if any of the specified permissions exist in the
        permission instance.

        perms: tuple[:class:`str` | :class:`Flags`]
            A tuple of strings or permission flags.
        """
        res = self.__class__.resolve(*perms)
        return any(map(lambda p: p in self.value, res))

    def all(self, *perms: str | Flags) -> bool:
        """Returns ``True`` is all of the specified permissions exist in the
        permission instance.

        perms: tuple[:class:`str` | :class:`Flags`]
            A tuple of strings or permission flags.
        """
        res = self.__class__.resolve(*perms)
        return all(map(lambda p: p in self.value, res))

    def is_admin(self) -> bool:
        """Returns ``True`` if any of the permissions in the instance are
        administrative.
        """
        return any(filter(lambda p: 'admin' in p, self.value))

    def serialize(self) -> dict[str, bool]:
        """Returns a dict of permission keys mapping to their presence in the
        permission instance.
        """
        return {k: k in self.value for k in Flags.values(Flags)}
