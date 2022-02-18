from inspect import iscoroutinefunction
from typing import Callable
from .errors import EventError


class EventManager:
    '''Events emitter manager for Pytero'''
    def __init__(self, max_slots: int = 10) -> None:
        self._slots: dict[str, list[Callable[..., None]]] = {}
        self.max_slots = max_slots
        self.locked = False
    
    def add_event_slot(self, name: str, slot: Callable[..., None]) -> None:
        if self.locked:
            raise EventError('cannot add any more event slots')
        
        if not callable(slot):
            raise TypeError('event slot is not a function')
        
        if not iscoroutinefunction(slot):
            raise TypeError('event slot must be an async function')
        
        if slots := self._slots.get(name):
            slots.append(slot)
            self._slots[name] = slots
        else:
            self._slots[name] = [slot]
        
        if not self.locked and len(self._slots) == self.max_slots:
            self.locked = True
    
    def remove_event_slot(self, name: str) -> None:
        del self._slots[name]
        if self.locked and len(self._slots) < self.max_slots:
            self.locked = False
    
    def remove_all_events(self) -> None:
        self._slots.clear()
    
    async def emit_event(self, name: str, *args, **kwargs) -> None:
        if not self._slots.get(name):
            raise EventError("no events by the name of '%s'" % name)
        
        for slot in self._slots[name]:
            try:
                await slot(*args, **kwargs)
            except Exception as e:
                raise EventError(
                    "function failed at event '%s': %s"
                    % (name, str(e)))
