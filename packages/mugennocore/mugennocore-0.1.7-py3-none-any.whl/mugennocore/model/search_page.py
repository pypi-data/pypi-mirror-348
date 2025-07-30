from mugennocore.model.interfaces import ISearchPage
from mugennocore.model.search_obj import SearchObj


class SearchPage(ISearchPage):
    def __init__(self, search_results: list[SearchObj], pagination: list[int])-> None:
        self.search_results = search_results
        self.pagination = pagination

    def __str__(self) -> str:
        results_str = "\n".join(str(result) for result in self.search_results)
        return f"""
{results_str}
{'==='* len(self.pagination)}
{self.pagination}
"""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  search_results={repr(self.search_results)},\n"
            f"  pagination={repr(self.pagination)}\n"
            f")"
        )