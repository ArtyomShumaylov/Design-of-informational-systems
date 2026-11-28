from ReaderData_mapper_overloading import ReaderFull
from reader_rep_json import ReaderRepJson
from reader_rep_yaml import ReaderRepYaml
from repository import ReaderRepJsonAdapter, ReaderRepYamlAdapter, ReaderRepositoryMapper
from db_connection import DbConnection
from reader_db_adapter import ReaderRepDbAdapter
from decorators_db import FilterSortDbDecorator
from decorators_file import FilterSortFileDecorator


def main():
    # Файловые репозитории
    json_repo = ReaderRepJsonAdapter("readers.json")
    yaml_repo = ReaderRepYamlAdapter("readers.yaml")

    r = ReaderFull(10, "Иванов", "Иван", "Иванович", "Москва, Ленина 1", "+79990000001")
    json_repo.add(r)

    # Перенос из JSON в YAML
    ReaderRepositoryMapper.copy(json_repo, yaml_repo)

    # БД
    conn = DbConnection()
    db_repo = ReaderRepDbAdapter(conn)
    db_repo.add(r)

    # Декоратор: фильтр по фамилии, начинающейся на "И"
    filtered = FilterSortDbDecorator(
        db_repo,
        filter_fn=lambda x: x.last_name.startswith("И"),
        sort_key=lambda x: x.first_name,
    )
    print("Count:", filtered.get_count())
    print("Page 0, size 10:", [b.short_view() for b in filtered.get_k_n_short_list(10, 0)])

    # Декоратор для файлов
    filtered_file = FilterSortFileDecorator(
        json_repo,
        filter_fn=lambda x: x.last_name.startswith("И"),
    )
    print("File count:", filtered_file.get_count())


if __name__ == "__main__":
    main()