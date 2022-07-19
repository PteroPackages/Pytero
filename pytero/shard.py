from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage
from json import loads
from time import time
from typing import Callable
from .errors import ShardError
from .events import Emitter
from .types import _Http, WebSocketEvent


__all__ = ('Shard')

class Shard(Emitter):
    def __init__(self, http: _Http, identifier: str) -> None:
        super().__init__()
        self._http = http
        self._conn: ClientWebSocketResponse = None
        self.origin: str = http.url
        self.identifier: str = identifier
        self.ping: float = float('nan')
        self.last_ping: float = float('nan')
    
    def __repr__(self) -> str:
        return '<Shard identifier=%s status=%s>' % (self.identifier, self.status)
    
    @property
    def closed(self) -> bool:
        return self._conn is None
    
    def event(self, func: Callable[[str], None]) -> Callable[[str], None]:
        super().add_event(func.__name__, func)
        return func
    
    async def _debug(self, msg: str) -> None:
        await super().emit_event('on_debug', 'debug %s: %s' % (self.identifier, msg))
    
    def _evt(self, name: str, args: list[str] = []) -> dict[str, list[str]]:
        return {'event': name, 'args': args}
    
    async def _heartbeat(self) -> None:
        if self.closed:
            raise ShardError('connection not available for this shard')
        
        auth: dict[str,] = await self._http.get(f'/servers/{self.identifier}/websocket')
        await self._conn.send_json(self._evt('auth', auth['data']['token']))
    
    async def launch(self) -> None:
        if not self.closed:
            return
        
        auth: dict[str,] = await self._http.get(f'/servers/{self.identifier}/websocket')
        await self._debug('attempting to connect to websocket')
        
        async with ClientSession() as session:
            async with session.ws_connect(auth['data']['socket'], origin=self.origin) as self._conn:
                await self._debug('authenticating connection')
                await self._conn.send_json(self._evt('auth', auth['data']['token']))
                await self._debug('authentication sent')
                
                async for msg in self._conn:
                    await self._on_event(msg)
    
    def destroy(self) -> None:
        if not self.closed:
            self._conn.close()
            self._conn = None
    
    async def _on_event(self, event: WSMessage) -> None:
        json = event.json()
        await self._debug('received event: %s' % data.event)
        await super().emit_event('on_raw', json)
        data = WebSocketEvent(**json)
        
        match data.event:
            case 'auth success':
                self.ping = time() - self.last_ping
                self.last_ping = time()
                await super().emit_event('on_auth_success')
            case 'token expiring':
                await self._heartbeat()
            case 'token expired':
                self.destroy()
                await self.launch()
            case 'daemon error' | 'jwt error':
                if super().has_event('on_error'):
                    await super().emit_event('on_error', ''.join(data.args))
                else:
                    self.destroy()
                    raise ShardError(''.join(data.args))
            case 'status':
                await super().emit_event('on_status_update', data.args[0])
            case 'stats':
                p = loads(''.join(data.args))
                await super().emit_event('on_stats_update', p)
            case 'console output':
                await super().emit_event('on_output', ''.join(data.args))
            case 'daemon message':
                await super().emit_event('on_daemon_log', ''.join(data.args))
            case 'install start':
                await super().emit_event('on_install_start')
            case 'install output':
                await super().emit_event('on_install_log', ''.join(data.args))
            case 'install completed':
                await super().emit_event('on_install_end')
            case 'transfer logs':
                await super().emit_event('on_transfer_log', ''.join(data.args))
            case 'transfer status':
                await super().emit_event('on_transfer_status', ''.join(data.args))
            case 'backup completed':
                p = None
                if len(data.args) > 0:
                    p = loads(''.join(data.args))
                
                await super().emit_event('on_backup_complete', p)
            case _:
                await super().emit_event('on_error', "received unknown event '%s'" % data.event)
    
    def request_logs(self) -> None:
        if not self.closed:
            self._conn.send_json(self._evt('send command'))
    
    def request_stats(self) -> None:
        if not self.closed:
            self._conn.send_json(self._evt('send stats'))
    
    def send_command(self, cmd: str) -> None:
        if not self.closed:
            self._conn.send_json(self._evt('send command', cmd))
    
    def send_state(self, state: str) -> None:
        if not self.closed:
            self._conn.send_json(self._evt('set state', state))
