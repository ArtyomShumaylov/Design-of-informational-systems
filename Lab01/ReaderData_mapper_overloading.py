import csv
import json
import re
from io import StringIO

class ReaderBrief:
    def __init__(self, *args, **kwargs):

        if len(args) == 1 and isinstance(args[0], str) and not kwargs:
            data_str = args[0]
            if self._is_json(data_str):
                self._init_from_dict(self._parse_json(data_str))
            elif self._is_csv(data_str):
                self._init_from_dict(self._parse_csv(data_str))
            else:
                raise ValueError("String argument must be valid JSON or CSV format.")
                
        elif len(args) == 3 and not kwargs:
            self._init_standard(args[0], args[1], args[2])
            
        elif 'last_name' in kwargs and 'first_name' in kwargs and 'sur_name' in kwargs and len(kwargs) == 3:
            self._init_standard(kwargs['last_name'], kwargs['first_name'], kwargs['sur_name'])
            
        else:
            raise TypeError(
                "Invalid arguments for ReaderBrief. Use:\n"
                "1. ReaderBrief('Last', 'First', 'Sur')\n"
                "2. ReaderBrief(json_string)\n"
                "3. ReaderBrief(csv_string)\n"
                "4. ReaderBrief(last_name='...', first_name='...', sur_name='...')"
            )

    def _init_standard(self, last_name: str, first_name: str, sur_name: str):
        self._last_name = self.validate_name(last_name, "Фамилия")
        self._first_name = self.validate_name(first_name, "Имя")
        self._sur_name = self.validate_name(sur_name, "Отчество")

    def _init_from_dict(self, data: dict):
        required = {'last_name', 'first_name', 'sur_name'}
        missing = required - data.keys()
        if missing:
            raise ValueError(f"Missing fields in data: {missing}")
        
        self._init_standard(
            last_name=data['last_name'],
            first_name=data['first_name'],
            sur_name=data['sur_name']
        )

    @staticmethod
    def _is_json(s: str) -> bool:
        try:
            json.loads(s)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def _is_csv(s: str) -> bool:
        return ',' in s

    @staticmethod
    def _parse_json(json_str: str) -> dict:
        try:
            data = json.loads(json_str)
            if not isinstance(data, dict):
                raise ValueError("JSON root must be an object.")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    @staticmethod
    def _parse_csv(csv_str: str) -> dict:
        try:
            rows = list(csv.reader(StringIO(csv_str), strict=True))
            if len(rows) != 1:
                raise ValueError("CSV обязан содержать только одну колонку")
            
            row = rows[0]
            if len(row) < 3:
                raise ValueError("CSV обязан содержать минимум 3 поля")
            
            return {
                "last_name": row[0],
                "first_name": row[1],
                "sur_name": row[2]
            }
        except csv.Error as e:
            raise ValueError(f"Invalid CSV: {e}")

    @staticmethod
    def validate_name(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} должна быть непустой строкой")

        value = value.strip()

        if not re.fullmatch(r"[А-Яа-яЁёA-Za-z\s-]+", value):
            raise ValueError(f"{field_name} содержит недопустимые символы")

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
            data_str = args[0]
            if self._is_json(data_str):
                self._init_from_dict(self._parse_json(data_str))
            elif self._is_csv(data_str):
                self._init_from_dict(self._parse_csv(data_str))
            else:
                raise ValueError("String argument must be valid JSON or CSV format.")

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
            raise TypeError(
                "Invalid arguments for ReaderFull. Use:\n"
                "1. ReaderFull(id, last, first, sur, addr, phone)\n"
                "2. ReaderFull(json_string)\n"
                "3. ReaderFull(csv_string)\n"
                "4. ReaderFull(client_id=..., ...)"
            )

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

    def _init_from_dict(self, data: dict):
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
            raise ValueError(f"Отсутствуют поля: {', '.join(sorted(missing_fields))}.")

        self._init_standard(
            client_id=data["client_id"],
            last_name=data["last_name"],
            first_name=data["first_name"],
            sur_name=data["sur_name"],
            address=data["address"],
            phone_number=data["phone_number"]
        )

    @staticmethod
    def _is_json(s: str) -> bool:
        try:
            json.loads(s)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def _is_csv(s: str) -> bool:
        return ',' in s

    @staticmethod
    def _parse_json(json_str: str) -> dict:
        try:
            data = json.loads(json_str)
            if not isinstance(data, dict):
                raise ValueError("JSON root must be an object.")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    @staticmethod
    def _parse_csv(csv_str: str) -> dict:
        try:
            rows = list(csv.reader(StringIO(csv_str), strict=True))
            if len(rows) != 1:
                raise ValueError("CSV must contain exactly one row.")
            
            row = rows[0]
            if len(row) != 6:
                raise ValueError("CSV for ReaderFull must contain exactly 6 fields.")

            client_id_str, last_name, first_name, sur_name, address, phone_number = row
            
            try:
                client_id = int(client_id_str)
            except ValueError:
                raise ValueError("Client ID in CSV must be an integer.")

            return {
                "client_id": client_id,
                "last_name": last_name,
                "first_name": first_name,
                "sur_name": sur_name,
                "address": address,
                "phone_number": phone_number
            }
        except csv.Error as e:
            raise ValueError(f"Invalid CSV: {e}")

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
    print("--- Тест 1: Стандартный ---")
    reader = ReaderFull(
        1,
        "Иванов",
        "Иван",
        "Иванович",
        "Москва, улица Ленина, 10",
        "+79991234567"
    )
    print(reader.full_view())

    print("\n--- Тест 2: JSON (ReaderFull) ---")
    json_data = json.dumps({
        "client_id": 2,
        "last_name": "Петрова",
        "first_name": "Анна",
        "sur_name": "Сергеевна",
        "address": "Москва, улица Мира, 5",
        "phone_number": "+79991234568"
    }, ensure_ascii=False)
    
    reader_from_json = ReaderFull(json_data)
    print(reader_from_json.full_view())

    print("\n--- Тест 3: CSV (ReaderFull) ---")
    
    csv_data = '3,Сидоров,Павел,Игоревич,"Москва, улица Мира, 15",79991234569'
    reader_from_csv = ReaderFull(csv_data)
    print(reader_from_csv.full_view())

    print("\n--- Тест 4: ReaderBrief из JSON ---")
    brief_json = '{"last_name": "Смирнов", "first_name": "Дмитрий", "sur_name": "Алексеевич"}'
    brief_reader_json = ReaderBrief(brief_json)
    print(f"Brief из JSON: {brief_reader_json.short_view()}")

    print("\n--- Тест 5: ReaderBrief из CSV ---")
    brief_csv = "Кузнецов,Елена,Владимировна"
    brief_reader_csv = ReaderBrief(brief_csv)
    print(f"Brief из CSV: {brief_reader_csv.short_view()}")

    print("\n--- Тест 6: Mapper и Equality ---")
    brief_reader_std = ReaderMapper.to_brief(reader)
    print(f"Map Brief: {brief_reader_std.short_view()}")
    
    reconstructed_reader = ReaderMapper.to_full(
        brief_reader_std,
        4,
        "Казань, улица Мира, 15",
        "+79991234570"
    )
    print(f"Воссозданный: {reconstructed_reader.full_view()}")
    
    print(f"Тот же ID? {reader == reconstructed_reader}")
    
    reader_copy = ReaderFull(1, "Иванов", "Иван", "Иванович", "Другой адрес", "+70000000000")
    print(f"Тот же ID? {reader == reader_copy}")