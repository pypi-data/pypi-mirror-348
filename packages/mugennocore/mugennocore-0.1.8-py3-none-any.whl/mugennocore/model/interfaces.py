from abc import ABC, abstractmethod
from typing import Protocol

from mugennocore.model.search_obj import SearchObj  # type: ignore


class IManga(ABC):
    """Interface to represent a Manga General Data"""

    def __init__(self):
        pass


class IPage(ABC):
    """Interface to represent a Manga Page"""

    def __init__(self):
        pass


class IChapter(ABC):
    """Interface to represent a Manga Chapter"""

    def __init__(self):
        pass


class ISearchObj(ABC):
    """Interface to representa  search return object"""

    def __init__(self):
        pass


class ISearchPage(Protocol):
    """Interface for search results page with pagination support."""

    # Atributos obrigatórios (type hints apenas)
    search_results: list[SearchObj]
    pagination: list[int]

    @abstractmethod
    def __str__(self) -> str:
        """User-friendly string representation."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        pass
