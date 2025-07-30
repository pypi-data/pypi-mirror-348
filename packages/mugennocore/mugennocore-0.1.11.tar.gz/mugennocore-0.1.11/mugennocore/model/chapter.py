from mugennocore.model.interfaces import IChapter


class Chapter(IChapter):
    """Represents a Manga Chapter"""

    def __init__(
        self,
        url: str,
        download_url: str,
        title: str,
        index: float,
        release_date: str = "N/A",
    ) -> None:
        self.url = url
        self.download_url = download_url
        self.title = title
        self.index = index
        self.release_date = release_date
        self.cover = (
            None  # TODO: Implement covers to chapters based on first page of chapter
        )

    def __str__(self) -> str:
        return f"""
{self.index} - {self.title}
Doanload zip: {self.download_url}
"""

    def __repr__(self):
        return (
            f"Chapter(\n"
            f"  title={repr(self.title)},\n"
            f"  index={self.index},\n"
            f"  url={repr(self.url)},\n"
            f"  download_url={repr(self.download_url)},\n"
            f"  release_date={self.release_date},\n"
            f")"
        )
