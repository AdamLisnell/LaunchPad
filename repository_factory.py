from typing import Dict, Type, TypeVar, Optional, Callable

from core.ports.repositories.base_repository import BaseRepository
from core.ports.repositories.candidate_repository import CandidateRepository
from core.ports.repositories.job_repository import JobRepository
from core.ports.repositories.requirement_repository import RequirementRepository

# Type variables
T = TypeVar("T")
R = TypeVar("R", bound=BaseRepository)


class RepositoryFactory:
    """Factory for creating repository instances based on configuration."""

    def __init__(self):
        self._repositories: Dict[Type[R], Dict[str, Type[R]]] = {
            CandidateRepository: {},
            JobRepository: {},
            RequirementRepository: {},
        }
        self._instances: Dict[Type[R], Dict[str, R]] = {
            CandidateRepository: {},
            JobRepository: {},
            RequirementRepository: {},
        }
        self._factories: Dict[Type[R], Dict[str, Callable[..., R]]] = {
            CandidateRepository: {},
            JobRepository: {},
            RequirementRepository: {},
        }

    def register(
        self,
        interface_type: Type[R],
        implementation_type_or_factory: Type[R] | Callable[..., R],
        name: str = "default",
    ) -> None:
        """Register an implementation for a repository interface."""
        if interface_type not in self._repositories:
            self._repositories[interface_type] = {}
            self._factories[interface_type] = {}

        if callable(implementation_type_or_factory) and not isinstance(
            implementation_type_or_factory, type
        ):
            # It's a factory function
            self._factories[interface_type][name] = implementation_type_or_factory
        else:
            # It's a class type
            self._repositories[interface_type][name] = implementation_type_or_factory

    def get(self, interface_type: Type[R], name: str = "default", **kwargs) -> R:
        """Get an instance of a repository."""
        # Check if we already have an instance
        if (
            interface_type in self._instances
            and name in self._instances[interface_type]
        ):
            return self._instances[interface_type][name]

        # Check if we have a registered factory
        if (
            interface_type in self._factories
            and name in self._factories[interface_type]
        ):
            factory = self._factories[interface_type][name]
            instance = factory(**kwargs)

            # Save the instance for reuse
            if interface_type not in self._instances:
                self._instances[interface_type] = {}
            self._instances[interface_type][name] = instance

            return instance

        # Check if we have a registered implementation
        if (
            interface_type not in self._repositories
            or name not in self._repositories[interface_type]
        ):
            raise ValueError(
                f"No implementation registered for {interface_type.__name__} with name '{name}'"
            )

        # Create a new instance
        implementation = self._repositories[interface_type][name]
        instance = implementation(**kwargs)

        # Save the instance for reuse
        if interface_type not in self._instances:
            self._instances[interface_type] = {}
        self._instances[interface_type][name] = instance

        return instance

    def get_factory(
        self, interface_type: Type[R], name: str = "default"
    ) -> Callable[..., R]:
        """Get a factory function for a repository interface interface."""
        if (
            interface_type in self._factories
            and name in self._factories[interface_type]
        ):
            return self._factories[interface_type][name]
        raise ValueError(
            f"No factory registered for {interface_type.__name__} with name '{name}'"
        )

    def clear_instances(self) -> None:
        """Clear all instances (useful for testing)."""
        self._instances = {
            CandidateRepository: {},
            JobRepository: {},
            RequirementRepository: {},
        }


# Create a global instance for easy import
repository_factory = RepositoryFactory()