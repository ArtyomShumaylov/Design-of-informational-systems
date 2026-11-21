import csv
import json
import re
from io import StringIO

#Добавить функционал для создания из csv
#Обновить оба класса с одним функционалом
#Сделать вторую лабу

class ReaderBrief:
    def __init__(self, last_name: str, first_name: str, sur_name: str):
        self._last_name = self.validate_name(last_name, "Фамилия")
        self._first_name = self.validate_name(first_name, "Имя")
        self._sur_name = self.validate_name(sur_name, "Отчество")

    @staticmethod
    def validate_name(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} должна быть непустой строкой.")

        value = value.strip()

        if not re.fullmatch(r"[А-Яа-яЁёA-Za-z\s-]+", value):
            raise ValueError(f"{field_name} содержит недопустимые символы.")

        return value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self._last_name = self.validate_name(value, "Фамилия")

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = self.validate_name(value, "Имя")

    @property
    def sur_name(self) -> str:
        return self._sur_name

    @sur_name.setter
    def sur_name(self, value: str):
        self._sur_name = self.validate_name(value, "Отчество")

    def short_view(self) -> str:
        return f"{self.last_name} {self.first_name[0]}.{self.sur_name[0]}."

    def __str__(self) -> str:
        return self.short_view()

    def __eq__(self, other) -> bool:
        if not isinstance(other, ReaderBrief):
            return NotImplemented

        return (
            self.last_name,
            self.first_name,
            self.sur_name
        ) == (
            other.last_name,
            other.first_name,
            other.sur_name
        )


class ReaderFull:
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str) and not kwargs:
            self._init_from_json(args[0])
        elif len(args) == 6 and not kwargs:
            self._init_standard(*args)
        elif 'client_id' in kwargs and len(kwargs) == 6:
            self._init_standard(
                kwargs['client_id'],
                kwargs['last_name'],
                kwargs['first_name'],
                kwargs['sur_name'],
                kwargs['address'],
                kwargs['phone_number']
            )
        else:
            raise TypeError("Неверные аргументы для конструктора ReaderFull.")

    def _init_standard(
        self,
        client_id: int,
        last_name: str,
        first_name: str,
        sur_name: str,
        address: str,
        phone_number: str
    ):
        self._client_id = self.validate_id(client_id)
        self._last_name = self.validate_name(last_name, "Фамилия")
        self._first_name = self.validate_name(first_name, "Имя")
        self._sur_name = self.validate_name(sur_name, "Отчество")
        self._address = self.validate_address(address)
        self._phone_number = self.validate_phone(phone_number)

    def _init_from_json(self, json_str: str):
        if not isinstance(json_str, str):
            raise ValueError("Данные должны быть строкой.")

        try:
            data = json.loads(json_str)
        except (json.JSONDecodeError, TypeError) as error:
            raise ValueError("Некорректная JSON-строка.") from error

        if not isinstance(data, dict):
            raise ValueError("JSON должен содержать объект с данными читателя.")

        required_fields = {
            "client_id",
            "last_name",
            "first_name",
            "sur_name",
            "address",
            "phone_number"
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            raise ValueError(
                f"Отсутствуют поля: {', '.join(sorted(missing_fields))}."
            )

        self._init_standard(
            client_id=data["client_id"],
            last_name=data["last_name"],
            first_name=data["first_name"],
            sur_name=data["sur_name"],
            address=data["address"],
            phone_number=data["phone_number"]
        )

    def _init_from_csv(self, csv_str: str):
        if not isinstance(csv_str, str):
            raise ValueError("CSV-данные должны быть строкой.")

        try:
            rows = list(csv.reader(StringIO(csv_str), strict=True))
        except csv.Error as error:
            raise ValueError("Некорректная CSV-строка.") from error

        if len(rows) != 1 or len(rows[0]) != 6:
            raise ValueError("CSV должен содержать ровно 6 полей в одной строке.")

        client_id, last_name, first_name, sur_name, address, phone_number = rows[0]

        try:
            client_id = int(client_id)
        except ValueError as error:
            raise ValueError("ID читателя в CSV должен быть целым числом.") from error

        self._init_standard(
            client_id=client_id,
            last_name=last_name,
            first_name=first_name,
            sur_name=sur_name,
            address=address,
            phone_number=phone_number
        )
    
    @staticmethod
    def validate_id(value: int) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("ID читателя должен быть положительным целым числом")
        return value

    @staticmethod
    def validate_name(value: str, field_name: str) -> str:
        return ReaderBrief.validate_name(value, field_name)

    @staticmethod
    def validate_address(value: str) -> str:
        if not isinstance(value, str) or len(value.strip()) < 5:
            raise ValueError("Адрес - не менее 5 символов")
        return value.strip()

    @staticmethod
    def validate_phone(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Телефон должен быть str")

        value = value.strip()

        if not re.fullmatch(r"\+?[0-9\s()\-]+", value):
            raise ValueError("Телефон содержит недопустимые символы")

        digit_count = len(re.sub(r"\D", "", value))

        if not 10 <= digit_count <= 15:
            raise ValueError("Количество цифр в телефоне должно быть от 10 до 15")

        return value

    @property
    def client_id(self) -> int:
        return self._client_id

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self._last_name = self.validate_name(value, "Фамилия")

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = self.validate_name(value, "Имя")

    @property
    def sur_name(self) -> str:
        return self._sur_name

    @sur_name.setter
    def sur_name(self, value: str):
        self._sur_name = self.validate_name(value, "Отчество")

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = self.validate_address(value)

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        self._phone_number = self.validate_phone(value)

    def short_view(self) -> str:
        return ReaderMapper.to_brief(self).short_view()

    def full_view(self) -> str:
        return (
            f"ID: {self.client_id}, "
            f"ФИО: {self.last_name} {self.first_name} {self.sur_name}, "
            f"Адрес: {self.address}, "
            f"Телефон: {self.phone_number}"
        )

    def __str__(self) -> str:
        return self.full_view()

    def __eq__(self, other) -> bool:
        if not isinstance(other, ReaderFull):
            return NotImplemented
        return self.client_id == other.client_id


class ReaderMapper:
    @staticmethod
    def to_brief(reader: ReaderFull) -> ReaderBrief:
        if not isinstance(reader, ReaderFull):
            raise TypeError("Ожидается ReaderFull")

        return ReaderBrief(
            last_name=reader.last_name,
            first_name=reader.first_name,
            sur_name=reader.sur_name
        )

    @staticmethod
    def to_full(
        reader: ReaderBrief,
        client_id: int,
        address: str,
        phone_number: str
    ) -> ReaderFull:
        if not isinstance(reader, ReaderBrief):
            raise TypeError("Ожидается ReaderBrief")

        return ReaderFull(
            client_id=client_id,
            last_name=reader.last_name,
            first_name=reader.first_name,
            sur_name=reader.sur_name,
            address=address,
            phone_number=phone_number
        )

if __name__ == "__main__":
    reader = ReaderFull(
        1,
        "Иванов",
        "Иван",
        "Иванович",
        "Москва, улица Ленина, 10",
        "+79991234567"
    )

    brief_reader = ReaderMapper.to_brief(reader)

    print("Полная версия:", reader.full_view())
    print("Краткая версия:", brief_reader.short_view())

    json_data = json.dumps({
        "client_id": 2,
        "last_name": "Петрова",
        "first_name": "Анна",
        "sur_name": "Сергеевна",
        "address": "Москва, улица Мира, 5",
        "phone_number": "+79991234568"
    }, ensure_ascii=False)

    reader_from_json = ReaderFull(json_data)
    print("Из JSON:", reader_from_json.full_view())

    reader_from_csv = ReaderFull('3,Сидоров,Павел,Игоревич,"Москва, улица Мира, 15",79991234569')
    print("Из CSV:", reader_from_csv.full_view())

    reconstructed_reader = ReaderMapper.to_full(
        brief_reader,
        4,
        "Казань, улица Мира, 15",
        "+79991234570"
    )

    print("Восстановленный:", reconstructed_reader.full_view())
    print("Одинаковый ID:", reader == reconstructed_reader)