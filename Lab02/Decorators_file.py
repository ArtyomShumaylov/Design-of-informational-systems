from typing import List, Optional, Callable, Any
from repository import ReaderRepository
from ReaderData_mapper_overloading import ReaderFull, ReaderBrief, ReaderMapper


class FilterSortFileDecorator(ReaderRepository):

    def __init__(
        self,
        repo: ReaderRepository,
        filter_fn: Optional[Callable[[ReaderFull], bool]] = None,
        sort_key: Optional[Callable[[ReaderFull], Any]] = None,
    ):
        self._repo = repo
        self._filter_fn = filter_fn
        self._sort_key = sort_key

    def _apply(self, readers: List[ReaderFull]) -> List[ReaderFull]:
        if self._filter_fn:
            readers = [r for r in readers if self._filter_fn(r)]
        if self._sort_key:
            readers = sorted(readers, key=self._sort_key)
        return readers

    def read_all(self) -> List[ReaderFull]:
        return self._apply(self._repo.read_all())

    def get_by_id(self, client_id: int) -> Optional[ReaderFull]:
        r = self._repo.get_by_id(client_id)
        if r and self._filter_fn and not self._filter_fn(r):
            return None
        return r

    def get_k_n_short_list(self, k: int, n: int) -> List[ReaderBrief]:
        readers = self._apply(self._repo.read_all())
        start, end = n * k, n * k + k
        return [ReaderMapper.to_brief(r) for r in readers[start:end]]

    def sort_by_last_name(self) -> None:
        self._repo.sort_by_last_name()

    def add(self, reader: ReaderFull) -> int:
        return self._repo.add(reader)

    def replace(self, client_id: int, reader: ReaderFull) -> bool:
        return self._repo.replace(client_id, reader)

    def delete(self, client_id: int) -> bool:
        return self._repo.delete(client_id)

    def get_count(self) -> int:
        if self._filter_fn:
            return len(self._apply(self._repo.read_all()))
        return self._repo.get_count()