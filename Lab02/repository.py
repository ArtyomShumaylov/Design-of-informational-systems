# repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from ReaderData_mapper_overloading import ReaderFull, ReaderBrief

# Абстрактный репозиторий — общий контракт
class ReaderRepository(ABC):

    @abstractmethod
    def read_all(self) -> List[ReaderFull]: ...

    @abstractmethod
    def get_by_id(self, client_id: int) -> Optional[ReaderFull]: ...

    @abstractmethod
    def get_k_n_short_list(self, k: int, n: int) -> List[ReaderBrief]: ...

    @abstractmethod
    def sort_by_last_name(self) -> None: ...

    @abstractmethod
    def add(self, reader: ReaderFull) -> int: ...

    @abstractmethod
    def replace(self, client_id: int, reader: ReaderFull) -> bool: ...

    @abstractmethod
    def delete(self, client_id: int) -> bool: ...

    @abstractmethod
    def get_count(self) -> int: ...


# Делегирование к ReaderRepJson
class ReaderRepJsonAdapter(ReaderRepository):

    def __init__(self, file_path: str):
        from Reader_rep_json import ReaderRepJson
        self._impl = ReaderRepJson(file_path)

    def read_all(self) -> List[ReaderFull]:
        return self._impl.read_all()

    def get_by_id(self, client_id: int) -> Optional[ReaderFull]:
        return self._impl.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[ReaderBrief]:
        return self._impl.get_k_n_short_list(k, n)

    def sort_by_last_name(self) -> None:
        return self._impl.sort_by_last_name()

    def add(self, reader: ReaderFull) -> int:
        return self._impl.add(reader)

    def replace(self, client_id: int, reader: ReaderFull) -> bool:
        return self._impl.replace(client_id, reader)

    def delete(self, client_id: int) -> bool:
        return self._impl.delete(client_id)

    def get_count(self) -> int:
        return self._impl.get_count()


# Делегирование к ReaderRepYaml
class ReaderRepYamlAdapter(ReaderRepository):

    def __init__(self, file_path: str):
        from Reader_rep_yaml import ReaderRepYaml
        self._impl = ReaderRepYaml(file_path)

    def read_all(self) -> List[ReaderFull]:
        return self._impl.read_all()

    def get_by_id(self, client_id: int) -> Optional[ReaderFull]:
        return self._impl.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[ReaderBrief]:
        return self._impl.get_k_n_short_list(k, n)

    def sort_by_last_name(self) -> None:
        return self._impl.sort_by_last_name()

    def add(self, reader: ReaderFull) -> int:
        return self._impl.add(reader)

    def replace(self, client_id: int, reader: ReaderFull) -> bool:
        return self._impl.replace(client_id, reader)

    def delete(self, client_id: int) -> bool:
        return self._impl.delete(client_id)

    def get_count(self) -> int:
        return self._impl.get_count()


# Маппер: конвертация между JSON и YAML через общий интерфейс."""
class ReaderRepositoryMapper:

    @staticmethod
    def copy(src: ReaderRepository, dst: ReaderRepository) -> None:
        for reader in src.read_all():
            dst.add(reader)