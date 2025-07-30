from mugennocore.model.interfaces import ISearchObj


class SearchObj(ISearchObj):
    """ "Reoresents a Search return Obj"""

    def __init__(
        self, title: str, url: str, cover_url: str, score: float, last_chapter: str
    ) -> None:
        self.title = title
        self.url = url
        self.cover_url = cover_url
        self.score = score
        self.last_chapter = last_chapter

    def __str__(self) -> str:
        return f"""
{self.title}
{self.cover_url}
★ - {self.score} | 🕮 - {self.last_chapter}
"""

    def __repr__(self) -> str:
        return f"""
SearchObj(
    title={self.title}
    url={self.url}
    cover_url={self.cover_url}
    score={self.score}
    last_chapter={self.last_chapter}
)
"""
