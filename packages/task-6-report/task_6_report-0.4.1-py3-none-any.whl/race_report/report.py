from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import re

# Базова директорія для зчитування даних
base_dir = Path(__file__).resolve().parent.parent.parent
data_folder = base_dir / "Data"

@dataclass
class Record:
    """
    Stores information about a single driver:
    - abbreviation (3 letters),
    - name,
    - team,
    - start and finish times,
    - list of errors, if any.
    """
    abbr: str | None = None
    name: str | None = None
    team: str | None = None
    _start_time: datetime | None = field(default=None, repr=False)
    _end_time: datetime | None = field(default=None, repr=False)
    errors: list[str] = field(default_factory=list)

    @property
    def start_time(self) -> datetime | None:
        """"Returns the driver's race start time."""
        return self._start_time

    @start_time.setter
    def start_time(self, value: datetime | None):
        """Sets the start time and checks its validity."""
        if value is None:
            self._add_or_replace_time_error("Немає start часу")
        elif self._end_time and value >= self._end_time:
            self._add_or_replace_time_error(
                "Некоректний час: старт після фінішу або одночасно з ним")
        else:
            self._remove_time_error("start")
            self._start_time = value
        self._check_time_consistency()

    @property
    def end_time(self) -> datetime | None:
        """Returns the driver's race finish time."""
        return self._end_time

    @end_time.setter
    def end_time(self, value: datetime | None):
        """Sets the finish time and checks its validity."""
        if value is None:
            self._add_or_replace_time_error("Немає end часу")
        elif self._start_time and value <= self._start_time:
            self._add_or_replace_time_error(
                "Некоректний час: фініш раніше або одночасно зі стартом")
        else:
            self._remove_time_error("end")
            self._end_time = value
        self._check_time_consistency()

    def _add_or_replace_time_error(self, message: str):
        """Adds a time error if it's not already present."""
        if message not in self.errors:
            self.errors.append(message)

    def _remove_time_error(self, key: str):
        """Removes errors containing a specific key (e.g., 'start' or 'end')."""
        self.errors = [err for err in self.errors if key not in err]

    def _check_time_consistency(self):
        """Checks if the finish time is later than the start time."""
        self.errors = [
            err for err in self.errors
            if "фініш раніше або одночасно" not in err
        ]
        if self._start_time and self._end_time:
            if self._end_time <= self._start_time:
                self.errors.append(
                    "Некоректний час: фініш раніше або одночасно зі стартом")

    @property
    def lap_time(self) -> timedelta | None:
        """Returns the difference between finish and start times (if both are set)."""
        if self._start_time and self._end_time and self._end_time > self._start_time:
            return self._end_time - self._start_time
        return None


class RaceData:
    """Class for processing race files, generating reports, and checking errors."""

    # Регулярні вирази для перевірки форматів
    ABBR_PATTERN = re.compile(r"^([A-Z]{3})_(.+?)_(.+)$")
    TIME_PATTERN = re.compile(
        r"^([A-Z]{3})(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\.\d{3})$"
    )

    def __init__(
            self,
            abbr_path: Path | None = None,
            start_path: Path | None = None,
            end_path: Path | None = None,
            folder: Path | None = None
    ) -> None:
        """
        Initializes RaceData.
        :param abbr_path: Path to the abbreviations.txt file.
        :param start_path: Path to the start.log file.
        :param end_path: Path to the end.log file.
        :param folder: Folder where the log files are located. Defaults to ./data if not provided.
        """
        self.folder = folder or Path.cwd() / "data"
        self.abbr_path = abbr_path or self.folder / "abbreviations.txt"
        self.start_path = start_path or self.folder / "start.log"
        self.end_path = end_path or self.folder / "end.log"

        self.records: list[Record] = []
        self.valid_records: list[Record] = []
        self.invalid_records: list[Record] = []

    def load_data(self):
        """Main function for loading data."""
        # Перевіряємо, чи існує папка
        if not self.folder.exists() or not self.folder.is_dir():
            print(f"Папку '{self.folder}' не знайдено.")
            return  # Завершуємо виконання, якщо папки немає

        # Якщо папка існує, продовжуємо виконання
        start_times, start_errors = self.read_times("start.log", is_start=True)
        end_times, end_errors = self.read_times("end.log", is_start=False)

        self.records.extend(start_errors)
        self.records.extend(end_errors)

        for error in start_errors + end_errors:
            for err in error.errors:
                print(err)

        valid_records, invalid_records = self.read_abbreviations()
        self.records.extend(invalid_records)

        for abbr, record in valid_records.items():
            if abbr in start_times and abbr in end_times:
                record.start_time = start_times[abbr]
                record.end_time = end_times[abbr]
            else:
                if abbr not in start_times:
                    record.errors.append(f"Немає start часу для {abbr}")
                if abbr not in end_times:
                    record.errors.append(f"Немає end часу для {abbr}")
            self.records.append(record)

    def read_abbreviations(self) -> tuple[dict[str, Record], list[Record]]:
        """
        Reads the abbreviations.txt file and returns:
        - a dictionary with abbreviations and Records
        - a list of "bad" records
        """
        abbreviations_path = self.folder / "abbreviations.txt"
        valid_records: dict[str, Record] = {}
        invalid_records: list[Record] = []

        try:
            with abbreviations_path.open(encoding="utf-8") as file:
                for line_number, line in enumerate(file, 1):
                    original_line = line
                    line = line.strip()
                    print(f"[{line_number}] LINE: {repr(line)}")

                    match = self.ABBR_PATTERN.match(line)
                    if match:
                        abbr, name, team = match.groups()
                        print(f"  ✅ MATCHED: abbr={abbr}, name={name}, team={team}")
                        valid_records[abbr] = Record(abbr, name, team)
                    else:
                        error_message = (
                            f"❌ Помилка у файлі {abbreviations_path}, рядок {line_number}: "
                            f"невідповідність формату ('{line}')"
                        )
                        print(f"  ❌ NO MATCH: {error_message}")
                        record = Record(errors=[error_message])
                        invalid_records.append(record)
        except FileNotFoundError:
            invalid_records.append(
                Record(errors=[f"Файл {abbreviations_path} не знайдено."]))
        except Exception as e:
            invalid_records.append(
                Record(errors=[f"Сталася помилка при зчитуванні: {e}"]))

        return valid_records, invalid_records

    def read_times(self, filename: str,
                   is_start: bool) -> tuple[dict[str, datetime], list[Record]]:
        """
        Reads start.log or end.log.
        :return: valid times and a list of Record objects with errors
        """
        times_path = self.folder / filename
        valid_times: dict[str, datetime] = {}
        invalid_records: list[Record] = []

        try:
            with times_path.open(encoding="utf-8") as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    match = type(self).TIME_PATTERN.match(line)
                    if match:
                        abbr, timestamp_str = match.groups()
                        try:
                            time = datetime.strptime(
                                timestamp_str, "%Y-%m-%d_%H:%M:%S.%f")
                            valid_times[abbr] = time
                        except ValueError:
                            invalid_records.append(
                                Record(
                                    abbr=abbr, errors=[
                                        f"Невірний формат дати: '{timestamp_str}' у рядку {line_number}"]))
                    else:
                        invalid_records.append(
                            Record(
                                errors=[
                                    f"Формат рядка порушено у {line_number}: '{line}'"]))
        except FileNotFoundError:
            invalid_records.append(
                Record(errors=[f"Файл {filename} не знайдено."]))
        except Exception as e:
            invalid_records.append(
                Record(errors=[f"Помилка при зчитуванні: {e}"]))

        return valid_times, invalid_records

    def build_report(self, order: str = "asc") -> dict:
        if order not in ("asc", "desc"):
            raise ValueError(f"Invalid order parameter: {order}")

        def is_valid(record: Record) -> bool:
            return (
                    record.abbr and
                    record.name and
                    record.team and
                    record.start_time and
                    record.end_time and
                    record.lap_time is not None and
                    not record.errors
            )

        valid_records = [r for r in self.records if is_valid(r)]
        invalid_records = [r for r in self.records if not is_valid(r)]

        valid_records.sort(key=lambda r: r.lap_time, reverse=(order == "desc"))

        self.valid_records = valid_records
        self.invalid_records = invalid_records

        return {
            "valid_count": len(valid_records),
            "valid": valid_records,
            "invalid": invalid_records,
        }

    def print_report(self, order: str) -> None:
        """
        Prints the report to the console.
        Outputs the first 15 valid records, others below.
        """
        valid_records = [r for r in self.records if r.lap_time is not None]
        invalid_records = [r for r in self.records if r.lap_time is None]

        # Сортуємо валідні записи в залежності від параметра order
        valid_records.sort(key=lambda r: r.lap_time, reverse=(order == 'desc'))

        print("=== Валідні записи ===")
        for i, record in enumerate(valid_records[:15], start=1):
            minutes, seconds = divmod(int(record.lap_time.total_seconds()), 60)
            seconds, milliseconds = divmod(
                int(record.lap_time.total_seconds() * 1000), 1000)
            print(
                f"{i}. {
                    record.name} | {
                    record.team} | {minutes}:{
                    seconds:02d},{
                    milliseconds:03d}")

        if len(valid_records) > 15:
            print("\n" + "-" * 79)

        for i, record in enumerate(valid_records[15:], start=16):
            minutes, seconds = divmod(int(record.lap_time.total_seconds()), 60)
            seconds, milliseconds = divmod(int(seconds * 1000), 1000)
            print(
                f"{i}. {
                    record.name} | {
                    record.team} | {minutes}:{
                    seconds:02d},{
                    milliseconds:03d}")

        print("\n=== Невалідні записи ===")
        for i, record in enumerate(invalid_records, start=1):
            print(f"{i}. {record.name} | {record.team} | {record.errors}")

    def get_driver_info(self, driver_name: str) -> Record | None:
        """Отримує інформацію про пілота за його ім’ям."""
        for record in self.records:
            if record.name == driver_name:
                return record
        return None
