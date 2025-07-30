from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, Protocol, runtime_checkable
import numpy as np  # type: ignore
from numpy.typing import NDArray

from mugennocore.model.genre import Genre

@runtime_checkable
class IManga(Protocol):
    """Interface protocol to represent a Manga General Data"""
    title: str
    url: str
    cover: str
    synopsis: str
    language: str
    status: str
    rating: float
    last_chapter: float
    chapters: Optional[list[str]]
    release_date: date
    last_update: date
    author: str
    artists: str
    serialization: str
    genres: list[Genre]
    embedding: NDArray[np.float32]
    
    def update_info(self, **kwargs) -> None: ...
    def detailed_info(self) -> str: ...


class IPage(ABC):
    """Interface to represent a Manga Page"""

    def __init__(self):
        pass


class IChapter(ABC):
    """Interface to represent a Manga Chapter"""

    def __init__(self):
        pass


@runtime_checkable
class ISearchObj(Protocol):
    """Interface type-safe para objetos de busca com runtime checking."""

    title: str
    url: str
    cover_url: str
    score: float
    last_chapter: str

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


@runtime_checkable
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
