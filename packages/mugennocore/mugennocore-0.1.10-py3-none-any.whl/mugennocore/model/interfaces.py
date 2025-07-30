from abc import ABC, abstractmethod
from typing import Protocol


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


class ISearchObj(Protocol):
    """Interface type-safe para objetos de busca com runtime checking."""

    title: str
    url: str
    cover_url: str
    score: float
    last_chapter: str

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class ISearchPage(Protocol):
    """Interface for search results page with pagination support."""

    # Atributos obrigatórios (type hints apenas)
    search_results: list[ISearchObj]
    pagination: list[int]

    @abstractmethod
    def __str__(self) -> str:
        """User-friendly string representation."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        pass
