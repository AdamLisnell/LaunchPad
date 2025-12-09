from datetime import date
from typing import Dict, Generic, List, Optional, TypeVar
import uuid

from core.ports.repositories.base_repository import BaseRepository

T = TypeVar("T")


class MemoryRepository(BaseRepository[T], Generic[T]):
    """Base memory repository implementation."""

    def __init__(self):
        self._storage: Dict[str, T] = {}

    async def get(self, id: str) -> Optional[T]:
        """Get an entity by id."""
        return self._storage.get(id)

    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        """List entities with pagination."""
        return list(self._storage.values())[skip : skip + limit]

    async def create(self, entity: T) -> T:
        """Create a new entity."""
        if not getattr(entity, "id", None):
            setattr(entity, "id", str(uuid.uuid4()))
        self._storage[entity.id] = entity
        return entity

    async def update(self, id: str, entity: T) -> Optional[T]:
        """Update an entity."""
        if id not in self._storage:
            return None
        if not getattr(entity, "id", None):
            setattr(entity, "id", id)
        self._storage[id] = entity
        return entity

    async def delete(self, id: str) -> bool:
        """Delete an entity."""
        if id not in self._storage:
            return False
        del self._storage[id]
        return True
