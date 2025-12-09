from typing import Dict, Generic, List, Optional, Type, TypeVar
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.ports.repositories.base_repository import BaseRepository
from infrastructure.db.models import Base

T = TypeVar("T")
M = TypeVar("M", bound=Base)


class MySQLRepository(BaseRepository[T], Generic[T, M]):
    """Base MySQL repository implementation."""

    def __init__(
        self, session: AsyncSession, model_class: Type[M], domain_class: Type[T]
    ):
        self.session = session
        self.model_class = model_class
        self.domain_class = domain_class

    async def get(self, id: str) -> Optional[T]:
        """Get an entity by id."""
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        model = result.scalars().first()

        if model is None:
            return None

        return model.to_domain()

    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        """List entities with pagination."""
        result = await self.session.execute(
            select(self.model_class).offset(skip).limit(limit)
        )
        models = result.scalars().all()

        return [model.to_domain() for model in models]

    async def create(self, entity: T) -> T:
        """Create a new entity."""
        if not getattr(entity, "id", None):
            setattr(entity, "id", str(uuid.uuid4()))

        model = self.model_class.from_domain(entity)
        self.session.add(model)
        await self.session.commit()

        return entity

    async def update(self, id: str, entity: T) -> Optional[T]:
        """Update an entity."""
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        model = result.scalars().first()

        if model is None:
            return None

        # Ensure entity has id
        if not getattr(entity, "id", None):
            setattr(entity, "id", id)

        # Update model
        updated_model = self.model_class.from_domain(entity)
        for key, value in updated_model.__dict__.items():
            if key != "_sa_instance_state":
                setattr(model, key, value)

        await self.session.commit()

        return entity

    async def delete(self, id: str) -> bool:
        """Delete an entity."""
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        model = result.scalars().first()

        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()

        return True
