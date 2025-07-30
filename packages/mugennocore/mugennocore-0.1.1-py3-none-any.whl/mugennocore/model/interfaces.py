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
