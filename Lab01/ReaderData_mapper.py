import json
import re


class ReaderBrief:
    def __init__(self, last_name: str, first_name: str, sur_name: str):
        self._validate_name(last_name, "Фамилия")
        self._validate_name(first_name, "Имя")
        self._validate_name(sur_name, "Отчество")

        self.__last_name = last_name
        self.__first_name = first_name
        self.__sur_name = sur_name

    @property
    def last_name(self): return self.__last_name
    @last_name.setter
    def last_name(self, value):
        self._validate_name(value, "Фамилия")
        self.__last_name = value

    @property
    def first_name(self): return self.__first_name
    @property
    def sur_name(self): return self.__sur_name

    def short_view(self) -> str:
        initials = f"{self.__first_name[0]}.{self.__sur_name[0]}." if self.__sur_name else f"{self.__first_name[0]}."
        return f"{self.__last_name} {initials}"

    def __str__(self):
        return self.short_view()

    @staticmethod
    def _validate_name(value: str, field_name: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} должна быть непустой строкой.")
        if not re.match(r"^[А-Яа-яЁёA-Za-z\s-]+$", value):
            raise ValueError(f"{field_name} содержит недопустимые символы.")


class ReaderFull:
    def __init__(self, client_id: int, last_name: str, first_name: str,
                 sur_name: str, adress: str, phone_number: str):
        self._validate_id(client_id)
        ReaderBrief._validate_name(last_name, "Фамилия")
        ReaderBrief._validate_name(first_name, "Имя")
        ReaderBrief._validate_name(sur_name, "Отчество")
        self._validate_address(adress)
        self._validate_phone(phone_number)

        self.__client_id = client_id
        self.__last_name = last_name
        self.__first_name = first_name
        self.__sur_name = sur_name
        self.__adress = adress
        self.__phone_number = phone_number

    @property
    def client_id(self): return self.__client_id
    @property
    def last_name(self): return self.__last_name
    @property
    def first_name(self): return self.__first_name
    @property
    def sur_name(self): return self.__sur_name
    @property
    def adress(self): return self.__adress
    @adress.setter
    def adress(self, value):
        self._validate_address(value)
        self.__adress = value

    @property
    def phone_number(self): return self.__phone_number
    @phone_number.setter
    def phone_number(self, value):
        self._validate_phone(value)
        self.__phone_number = value

    @staticmethod
    def _validate_id(value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID клиента должен быть целым положительным числом.")

    @staticmethod
    def _validate_address(value: str):
        if not isinstance(value, str) or len(value.strip()) < 5:
            raise ValueError("Адрес должен быть строкой длиной не менее 5 символов.")

    @staticmethod
    def _validate_phone(value: str):
        if not re.match(r"^\+?[0-9\s\-()]{10,15}$", value):
            raise ValueError("Неверный формат номера телефона.")

    @classmethod
    def from_json(cls, json_str: str) -> 'ReaderFull':
        data = json.loads(json_str)
        return cls(
            client_id=data["client_id"],
            last_name=data["last_name"],
            first_name=data["first_name"],
            sur_name=data["sur_name"],
            adress=data["adress"],
            phone_number=data["phone_number"]
        )

    @classmethod
    def from_csv_string(cls, csv_str: str) -> 'ReaderFull':
        parts = csv_str.split(',')
        if len(parts) != 6:
            raise ValueError("Неверный формат CSV строки")
        return cls(
            client_id=int(parts[0]),
            last_name=parts[1],
            first_name=parts[2],
            sur_name=parts[3],
            adress=parts[4],
            phone_number=parts[5]
        )

    def full_view(self) -> str:
        return (f"ID: {self.__client_id}, ФИО: {self.__last_name} {self.__first_name} {self.__sur_name}, "
                f"Адрес: {self.__adress}, Тел: {self.__phone_number}")

    def __repr__(self):
        return self.full_view()

    def __eq__(self, other):
        if not isinstance(other, ReaderFull):
            return False
        return self.__client_id == other.__client_id


class ReaderMapper:
    @staticmethod
    def to_brief(reader_full: ReaderFull) -> ReaderBrief:
        return ReaderBrief(
            last_name=reader_full.last_name,
            first_name=reader_full.first_name,
            sur_name=reader_full.sur_name
        )

    @staticmethod
    def to_full(reader_brief: ReaderBrief, client_id: int, adress: str, phone_number: str) -> ReaderFull:
        return ReaderFull(
            client_id=client_id,
            last_name=reader_brief.last_name,
            first_name=reader_brief.first_name,
            sur_name=reader_brief.sur_name,
            adress=adress,
            phone_number=phone_number
        )


print(ReaderFull(1, "last", "first", "sur", "kolotushkina", "1234567890").full_view())