from abc import ABC  # type: ignore


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

class ISearchPage(ABC):
    """Page results with pagination"""
    def __init__(self):
        pass