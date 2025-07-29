# Пакет task_6_report

`task_6_report` — Python package for analyzing Formula 1 race results: loading logs, building reports, output via CLI.

---

## Installation

```bash
pip install task_6_report
```

---

## Using

```python
from race_report.report import RaceData
from pathlib import Path

# Specify the path to your data folder
folder = Path(r"your path to the folder/data")
data = RaceData(folder)
data.load_data()
report = data.build_report(order='asc')  # 'asc' або 'desc'
data.print_report(report)
```

### Required data files:
abbreviations.txt:
```
DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
SVF_Sebastian Vettel_FERRARI
LHM_Lewis Hamilton_MERCEDES
```

start.log:
```
DRR2018-05-24_12:14:12.054
SVF2018-05-24_12:14:15.145
LHM2018-05-24_12:14:18.035
```

end.log:
```
DRR2018-05-24_12:15:26.399
SVF2018-05-24_12:15:29.750
LHM2018-05-24_12:15:33.082
```

### An example of a report:

```
1. DRR_Daniel Ricciardo | RED BULL RACING TAG HEUER | 1:14.345
2. SVF_Sebastian Vettel | FERRARI | 1:14.788
...
```

---

## Call in GitBash GitBash (CLI)

To run your report.py file with the --order option, use the following command:

```bash
race-report -p PATH_TO_DATA_FOLDER [-o asc|desc] [-d DRIVER_NAME]
```

Parameters:

 - -p, --path (required): path to the folder with the data files
 - -o, --order (optional): sort order (asc for ascending, desc for descending), default asc
 - -d, --driver (optional): pilot name to display information only for him/her

Examples:

- Build the full report in ascending order:

```bash
race-report -p data/ -o asc
```

- Build the full report in descending order:
```bash
race-report -p data/ -o desc
```

- Get information only about a specific pilot:
```bash
race-report -p data/ -d "Sebastian Vettel"
```
---

## The structure of the project

```
task_6_report/

├── src/
│   └── race_report/
│       ├── __init__.py
│       ├── report.py
│       └── cli.py
│
├── tests/
│   ├── __init__.py
│   ├── tests_load_data/
│   ├── tests_build_report/
│   ├── tests_print_report/
│   ├── tests_read_abbreviations/
│   └── tests_cli/
│
├── LICENSE
├── pyproject.toml
├── README.md
└── .gitignore
```

## License

This project is licensed under the MIT License.