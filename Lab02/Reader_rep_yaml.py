# reader_rep_yaml.py
import yaml
from typing import List, Optional
from ReaderData_mapper_overloading import ReaderFull, ReaderBrief


# Репозиторий для работы с ReaderFull в формате YAML

class ReaderRepYaml:

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._data: List[dict] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            if raw is None:
                self._data = []
            elif not isinstance(raw, list):
                raise ValueError("YAML root must be a list")
            else:
                self._data = raw
        except FileNotFoundError:
            self._data = []

    def _save(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self._data, f, allow_unicode=True, sort_keys=False)

    def read_all(self) -> List[ReaderFull]:
        return [ReaderFull(**item) for item in self._data]

    def get_by_id(self, client_id: int) -> Optional[ReaderFull]:
        for item in self._data:
            if item["client_id"] == client_id:
                return ReaderFull(**item)
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[ReaderBrief]:
        if k < 0 or n < 0:
            raise ValueError("k и n должны быть неотрицательными")
        start = n * k
        end = start + k
        readers = self.read_all()
        return [ReaderRepYaml._to_brief(r) for r in readers[start:end]]

    def sort_by_last_name(self) -> None:
        self._data.sort(key=lambda x: x["last_name"])
        self._save()

    def add(self, reader: ReaderFull) -> int:
        new_id = self._next_id()
        reader_dict = ReaderRepYaml._to_dict(reader)
        reader_dict["client_id"] = new_id
        self._data.append(reader_dict)
        self._save()
        return new_id

    def replace(self, client_id: int, reader: ReaderFull) -> bool:
        for i, item in enumerate(self._data):
            if item["client_id"] == client_id:
                self._data[i] = ReaderRepYaml._to_dict(reader)
                self._data[i]["client_id"] = client_id
                self._save()
                return True
        return False

    def delete(self, client_id: int) -> bool:
        for i, item in enumerate(self._data):
            if item["client_id"] == client_id:
                del self._data[i]
                self._save()
                return True
        return False

    def get_count(self) -> int:
        return len(self._data)

    def _next_id(self) -> int:
        if not self._data:
            return 1
        return max(item["client_id"] for item in self._data) + 1

    @staticmethod
    def _to_dict(reader: ReaderFull) -> dict:
        return {
            "client_id": reader.client_id,
            "last_name": reader.last_name,
            "first_name": reader.first_name,
            "sur_name": reader.sur_name,
            "address": reader.address,
            "phone_number": reader.phone_number,
        }

    @staticmethod
    def _to_brief(reader: ReaderFull) -> ReaderBrief:
        return ReaderBrief(
            last_name=reader.last_name,
            first_name=reader.first_name,
            sur_name=reader.sur_name,
        )