import argparse
import os
from pathlib import Path

from race_report.report import RaceData  # Імпортуємо твою логіку

def get_cli_arguments():
    """
    Парсинг аргументів командного рядка для запуску скрипта.
    """
    parser = argparse.ArgumentParser(description="Аналізатор гонки F1")

    parser.add_argument(
        "-p", "--path",
        required=True,
        help="Шлях до папки з файлами start.log, end.log, abbreviations.txt"
    )

    parser.add_argument(
        "-o", "--order",
        choices=["asc", "desc"],
        default="asc",
        help="Порядок сортування: asc (за зростанням) або desc (за спаданням)"
    )

    parser.add_argument(
        "-d", "--driver",
        metavar="NAME",
        help="Ім'я пілота для детальної інформації"
    )

    args = parser.parse_args()

    return {"path": args.path, "order": args.order, "driver": args.driver}


def main():
    args = get_cli_arguments()
    folder = Path(args["path"])

    race = RaceData(
        abbr_path=folder / "abbreviations.txt",
        start_path=folder / "start.log",
        end_path=folder / "end.log",
        folder=folder
    )

    race.load_data()

    if args["driver"]:
        record = race.get_driver_info(args["driver"])
        if record:
            print("Інформація про пілота:")
            print(f"Абревіатура: {record.abbr}")
            print(f"Ім’я: {record.name}")
            print(f"Команда: {record.team}")
            if record.lap_time:
                total_ms = int(record.lap_time.total_seconds() * 1000)
                minutes, remainder_ms = divmod(total_ms, 60_000)
                seconds, milliseconds = divmod(remainder_ms, 1000)
                print(f"Час кола: {minutes}:{seconds:02d},{milliseconds:03d}")
            else:
                print("Час кола: недоступний")
            if record.errors:
                print("Помилки:")
                for err in record.errors:
                    print(f"- {err}")
        else:
            print(f"Пілот з ім’ям '{args['driver']}' не знайдений.")
    else:
        race.print_report(order=args["order"])


if __name__ == "__main__":
    main()
