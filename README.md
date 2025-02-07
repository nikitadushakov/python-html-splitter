# Python HTML Splitter (MadDevs homework) 

[![CodeFactor](https://www.codefactor.io/repository/github/nikitadushakov/python-html-splitter/badge)](https://www.codefactor.io/repository/github/nikitadushakov/python-html-splitter)

## Структура проекта
```
├── README.md
├── msg_split.py
├── poetry.lock
├── pyproject.toml
├── python_html_splitter
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── splitter.py
│   └── utils.py
├── source.html
└── tests
```

## Сборка пакета:
```bash
git clone git@github.com:nikitadushakov/python-html-splitter.git
cd python-html-splitter
poetry install
```

## Запуск тестов:
```bash
poetry run pytest
```

## Запуск скрипта:
```bash
export MAX_LEN=<your_max_len>
export FILE_PATH=<your_file_path>
poetry run python msg_split.py --max-len=$MAX_LEN $FILE_PATH
```
