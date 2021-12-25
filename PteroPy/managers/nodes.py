from ..app.endpoints import NODES_MAIN, NODES_GET
from ..structures import Node
from typing import Any, Dict, Optional, Union


class NodeManager:
    def __init__(self, client) -> None:
        self.client = client
        self.cache: Dict[str, Node] = {}
    
    def __repr__(self) -> str:
        return '<NodeManager cache=%d>' % len(self.cache)
    
    def __patch(self, data: Dict[str, Any]) -> Union[Node, Dict[int, Node]]:
        if data.get('data'):
            res = {}
            for o in data['data']:
                n = Node(self.client, o['attributes'])
                res[n.id] = n
            
            self.cache.update(res)
            return res
    
    def resolve(self, obj: Any) -> Optional[Node]:
        if isinstance(obj, Node): return obj
        if type(obj) == int: return self.cache.get(obj)
        if type(obj) == str:
            r = filter(lambda n: n.name == obj, self.cache.values())
            return list(r)[0]
        
        return None
    
    async def fetch(self, _id: int = None, force: bool = False):
        if _id is not None:
            if not force:
                n = self.cache.get(_id)
                if n: return n
        
        data = await self.client.requests.get(
            NODES_GET(_id) if _id is not None else NODES_MAIN
        )
        return self.__patch(data)
    
    def query(self, entity, filter: str = None, sort: str = None):
        return NotImplemented
    
    def create(self, **options):
        return NotImplemented
    
    def update(self, node: Union[int, Node], **options):
        return NotImplemented
    
    def delete(self, id: int):
        return NotImplemented
