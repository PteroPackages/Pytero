"""A basic event emitter implementation for Pytero, specfically for the HTTP
and websocket interactions/events.
"""

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
        """Adds a callback function for a specified event. Note that the
        function can be synchronous or asynchronous as both will be handled
        when emitted.

        Parameters
        ----------
        name: :class:`str`
            The name of the event.
        slot: Callable[..., None]
            The callback function.
        """
        if not callable(slot):
            raise TypeError('event slot is not a function')

        self._slots[name] = (iscoroutinefunction(slot), slot)

    def remove_event(self, name: str, /) -> None:
        """Removes a callback function for a specified event.

        Parameters
        ----------
        name: :class:`str`
            The name of the event.
        """
        del self._slots[name]

    def has_event(self, name: str, /) -> bool:
        """Returns ``True`` if the specified event has a callback function.

        Parameters
        ----------
        name: :class:`str`
            The name of the event.
        """
        return name in self._slots

    def clear_slots(self) -> None:
        """Clears all the events and callback functions."""
        self._slots.clear()

    async def emit_event(self, name: str, *args, **kwargs) -> None:
        """Emits an event callback with the given arguments.

        Parameters
        ----------
        name: :class:`str`
            The name of the event.
        *args:
            A tuple of arguments to be passed on to the event callback.
        **kwargs:
            A dict of arguments to be passed on to the event callback.
        """
        if slot := self._slots.get(name):
            try:
                if slot[0]:
                    await slot[1](*args, **kwargs)
                else:
                    slot[1](*args, **kwargs)
            except Exception as ex:
                raise EventError(f'failed to run event: {ex}') from ex
