# Python HTML Splitter (MadDevs homework) 


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

## Запуск скрипта:
```bash
export MAX_LEN=<your_max_len>
export FILE_PATH=<your_file_path>

git clone git@github.com:nikitadushakov/python-html-splitter.git
cd python-html-splitter
poetry install
python3 msg_split.py --max-len=$MAX_LEN $FILE_PATH
```
