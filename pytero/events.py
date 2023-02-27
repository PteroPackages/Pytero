from inspect import iscoroutinefunction
from typing import Callable
from .errors import EventError


__all__ = ('Emitter',)


class Emitter:
    """Events emitter manager for Pytero"""

    def __init__(self) -> None:
        self._slots: dict[str, tuple[bool, Callable[..., None]]] = {}

    def __repr__(self) -> str:
        return f'<Emitter events={len(self._slots)}>'

    def add_event(self, name: str, slot: Callable[..., None]) -> None:
        if not callable(slot):
            raise TypeError('event slot is not a function')

        self._slots[name] = (iscoroutinefunction(slot), slot)

    def remove_event(self, name: str, /) -> None:
        del self._slots[name]

    def has_event(self, name: str, /) -> bool:
        return name in self._slots

    def clear_slots(self) -> None:
        self._slots.clear()

    async def emit_event(self, name: str, *args, **kwargs) -> None:
        if slot := self._slots.get(name):
            try:
                if slot[0]:
                    await slot[1](*args, **kwargs)
                else:
                    slot[1](*args, **kwargs)
            except Exception as ex:
                raise EventError(f'failed to run event: {ex}') from ex
