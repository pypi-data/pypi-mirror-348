from datetime import datetime
import numpy as np  # type: ignore
from numpy.typing import NDArray
from mugennocore.model.genre import Genre
from mugennocore.model.interfaces import IManga


class Manga(IManga):
    def __init__(
        self,
        title: str,
        url: str,
        synopsis: str,
        cover: str,
        language: str,
        status: str,
        rating: float,
        last_chapter: float,
        release_date: str,  # "YYYY-MM-DD"
        last_update: str,  # "YYYY-MM-DD"
        author: str,
        artists: str,
        serialization: str,
        genres: list[Genre],
        embedding: NDArray[np.float32],
    ):
        self.title = title
        self.url = url
        self.synopsis = synopsis
        self.cover = cover
        self.language = language
        self.status = status
        self.rating = rating
        self.last_chapter = last_chapter
        self.release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        self.last_update = datetime.strptime(last_update, "%Y-%m-%d").date()
        self.author = author
        self.artists = artists
        self.serialization = serialization
        self.genres = genres
        self.embedding = embedding

    def __str__(self) -> str:
        return (
            f"{self.title}"
            f"{self.cover}"
            f"★ - {self.rating} | Caps - {self.last_chapter} | Updated on - {self.last_update}\n"
            f"Genres: {', '.join(genre.value for genre in self.genres)}"
        )

    def __repr__(self) -> str:
        return (
            f"Manga(\n"
            f"  title={repr(self.title)},\n"
            f"  url={repr(self.url)},\n"
            f"  status={repr(self.status)},\n"
            f"  rating={self.rating},\n"
            f"  last_chapter={self.last_chapter},\n"
            f"  genres={[g.value for g in self.genres]},\n"
            f"  author={repr(self.author)},\n"
            f"  release_date={self.release_date.isoformat()},\n"
            f"  embedding_shape={self.embedding.shape}\n"
            f")"
        )

    def detailed_info(self) -> str:
        """Método adicional para exibição formatada completa."""
        return f"""
📖 {self.title.upper()}
{'=' * (len(self.title) + 2)}

🔗 URL: {self.url}
✍️ Autor(es): {self.author}
🎨 Artista(s): {self.artists}
📰 Serialização: {self.serialization}
📌 Status: {self.status}
⭐ Nota: {self.rating}
📜 Último Capítulo: {self.last_chapter}
🏷️ Gêneros: {', '.join(genre.value for genre in self.genres)}
🌐 Idioma: {self.language}

📝 Sinopse:
{self.synopsis}

🗓️ Data de Lançamento: {self.release_date}
🔄 Última Atualização: {self.last_update}
"""
