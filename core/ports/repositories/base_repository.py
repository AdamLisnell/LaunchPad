from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    """Base repository interface defining common operations."""

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get an entity by id."""
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        """List entities with pagination."""
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        pass

    @abstractmethod
    async def update(self, id: str, entity: T) -> Optional[T]:
        """Update an entity."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete an entity."""
        pass
