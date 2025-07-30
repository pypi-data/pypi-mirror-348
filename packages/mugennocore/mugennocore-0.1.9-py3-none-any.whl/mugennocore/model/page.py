from mugennocore.model.interfaces import IPage


class Page(IPage):
    """Object to represent a Manga Page"""

    def __init__(self, img_url: str, page_index: float) -> None:
        self.img_url = img_url
        self.pade_index = page_index
        self.img_binary = None  # TODO: Implement a binary from url method

    def __str__(self) -> str:
        return f"""
{self.img_url}
Page: {self.pade_index}           
"""

    def __repr__(self):
        return (
            f"Page(\n"
            f"  img_utl={repr(self.img_url)},\n"
            f"  page_index={repr(self.pade_index)},\n"
            f"  img_binary={repr(self.img_binary)},\n"
            f")"
        )
