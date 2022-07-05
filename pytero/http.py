from aiohttp import ClientSession, ClientResponse
from json import dumps
from sys import getsizeof
from time import time
from typing import Callable
from .errors import PteroAPIError, RequestError
from .events import Emitter


__all__ = ('RequestManager')

class RequestManager(Emitter):
    def __init__(self, api: str, url: str, key: str) -> None:
        super().__init__()
        self._api = api
        self.url = url
        self.key = key
        self.ping: float = float('nan')
    
    def __repr__(self) -> str:
        return '<RequestManager(Emitter)>'
    
    def event(self, func: Callable[[str], None]) -> Callable[[str], None]:
        super().add_event(func.__name__, func)
        return func
    
    async def _emit(self, name: str, *args):
        for arg in args:
            await super().emit_event(name, arg)
    
    def headers(self, ctype: str) -> dict[str, str]:
        return {
            'User-Agent': '%s Pytero v0.1.0' % self._api.title(),
            'Content-Type': ctype,
            'Accept': 'application/json,text/plain',
            'Authorization': 'Bearer %s' % self.key
        }
    
    def _validate_query(self, args: dict[str,]) -> str:
        query: list[str] = []
        if filter := args.get('filter'):
            query.append('filter[%s]=%s' % filter)
        
        if include := args.get('include'):
            query.append('include=' + ','.join(include))
        
        if sort := args.get('sort'):
            query.append(f'sort={sort}')
        
        if page := args.get('page'):
            query.append(f'page={page}')
        
        if per_page := args.get('per_page'):
            query.append(f'per_page={per_page}')
        
        if extra := args.get('extra'):
            (query.append(f'{k}={extra[k]}') for k in extra)
        
        if len(query) == 0:
            return ''
        
        return '?' + query[0] + '&'.join(query[1:])
    
    async def _make(self, method: str, path: str, **kwargs):
        if method not in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'):
            raise KeyError("invalid http method '%s'" % method)
        
        payload = None
        body = kwargs.get('body') or None
        ctype = kwargs.get('ctype') or 'application/json'
        
        if body is not None:
            if ctype == 'application/json':
                payload = dumps(body)
            else:
                payload = body
        
        query = self._validate_query(kwargs)
        url = '%s/api/%s%s%s' % (self.url, self._api, path, query)
        await self._emit(
            'debug',
            'request: %s /api/%s%s' % (method, self._api, path),
            'payload: %d bytes' % getsizeof(payload)
        )
        
        async with ClientSession() as session:
            start = time()
            async with getattr(session, method.lower())(
                url,
                data=payload,
                headers=self.headers(ctype)
            ) as response:
                self.ping = time() - start
                response: ClientResponse
                
                await self._emit(
                    'debug',
                    'response: %d' % response.status,
                    'content-type: %s' % response.content_type,
                    'content-length: %d' % (response.content_length or 0)
                )
                
                if response.status == 204:
                    return None
                
                if response.status in (200, 201, 202):
                    if response.headers.get('content-type') == 'application/json':
                        data = await response.json()
                        return data
                    else:
                        data = await response.text()
                        return data
                
                if 400 <= response.status < 500:
                    err: dict[str,] = await response.json()
                    raise PteroAPIError(err['errors'][0]['code'], err)
                
                raise RequestError(
                    'pterodactyl api returned an invalid or unacceptable'
                    ' response (status: %d)' % response.status)
    
    def get(
        self,
        path: str,
        *,
        body = None,
        ctype: str = None,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None,
        page: int = None,
        per_page: int = None
    ):
        return self._make(
            'GET',
            path,
            body=body,
            ctype=ctype,
            filter=filter,
            include=include,
            sort=sort,
            page=page,
            per_page=per_page
        )
    
    def post(
        self,
        path: str,
        body,
        *,
        ctype: str = None,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None,
        page: int = None,
        per_page: int = None
    ):
        return self._make(
            'POST',
            path,
            body=body,
            ctype=ctype,
            filter=filter,
            include=include,
            sort=sort,
            page=page,
            per_page=per_page
        )
    
    def patch(
        self,
        path: str,
        body,
        *,
        ctype: str = None,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None,
        page: int = None,
        per_page: int = None
    ):
        return self._make(
            'PATCH',
            path,
            body=body,
            ctype=ctype,
            filter=filter,
            include=include,
            sort=sort,
            page=page,
            per_page=per_page
        )
    
    def put(
        self,
        path: str,
        body,
        *,
        ctype: str = None,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None,
        page: int = None,
        per_page: int = None
    ):
        return self._make(
            'PUT',
            path,
            body=body,
            ctype=ctype,
            filter=filter,
            include=include,
            sort=sort,
            page=page,
            per_page=per_page
        )
    
    def delete(
        self,
        path: str,
        *,
        body = None,
        ctype: str = None,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None,
        page: int = None,
        per_page: int = None
    ):
        return self._make(
            'DELETE',
            path,
            body=body,
            ctype=ctype,
            filter=filter,
            include=include,
            sort=sort,
            page=page,
            per_page=per_page
        )
