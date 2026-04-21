# 🚀 Student ETL Pipeline on Apache Airflow

![Airflow](https://img.shields.io/badge/Apache%20Airflow-3.0+-017CEE?style=flat&logo=apache-airflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.1-150458?style=flat&logo=pandas&logoColor=white)

Учебный ETL-пайплайн для демонстрации навыков оркестрации данных. Пайплайн ежедневно забирает сырые данные о продажах, очищает их, обогащает вычисляемыми полями и загружает в SQLite.

---

## 📁 Структура проекта

```
airflow_etl_project/
├── dags/
│   └── sales_etl_dag.py
├── etl_scripts/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── data/
│   ├── raw/
│   └── staging/
├── db/
│   └── sales.db
├── requirements.txt
└── README.md
```

---

## 🔧 Технологии

| Компонент | Назначение |
|-----------|------------|
| Apache Airflow 3.0+ | Оркестрация и расписание задач |
| Python 3.12 | Основной язык разработки |
| Pandas | Обработка и очистка данных |
| SQLite | Хранение финальных данных |
| Ubuntu 22.04 | Окружение для запуска |

---

## 📊 Схема DAG

```
prepare_environment → extract_from_source → transform_and_cleanse → load_to_sqlite → check_row_count
```

---

## 🛠️ Установка и запуск

### 1. Создание виртуального окружения

```bash
python3 -m venv ~/airflow_env
source ~/airflow_env/bin/activate
```

### 2. Установка зависимостей

```bash
pip install apache-airflow pandas
```

### 3. Инициализация Airflow

```bash
export AIRFLOW_HOME=~/airflow
airflow db migrate
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

### 4. Отключение примеров DAG

```bash
sed -i 's/load_examples = True/load_examples = False/g' ~/airflow/airflow.cfg
```

### 5. Копирование файлов проекта

```bash
cp -r ~/path/to/project/dags ~/airflow/
cp -r ~/path/to/project/etl_scripts ~/airflow/
mkdir -p ~/airflow/data/raw ~/airflow/data/staging ~/airflow/db
```

### 6. Правка путей в скриптах

Убедись, что в `transform.py` и `load.py` указаны корректные пути до `~/airflow/data/` и `~/airflow/db/`.

### 7. Запуск Airflow

**Терминал 1 (API-сервер):**
```bash
source ~/airflow_env/bin/activate
airflow api-server -p 8080
```

**Терминал 2 (Планировщик):**
```bash
source ~/airflow_env/bin/activate
airflow scheduler
```

### 8. Доступ к веб-интерфейсу

Открой браузер и перейди по адресу:
```
http://localhost:8080
```
Логин: `admin`
Пароль: `admin` (или тот, что был задан при создании пользователя)

---

## ▶️ Запуск DAG

В интерфейсе Airflow найди DAG `student_sales_etl_pipeline`, нажми на Play и выбери **Trigger DAG**.

---

## ✅ Проверка результата

```bash
sqlite3 ~/airflow/db/sales.db "SELECT * FROM cleaned_sales LIMIT 5;"
```

---

## 📝 Примечания

- В Airflow 3.0+ команда `airflow webserver` заменена на `airflow api-server`
- Параметр `schedule_interval` переименован в `schedule`
- Для работы `BashOperator` с `sqlite3` необходимо установить пакет:
  ```bash
  sudo apt install sqlite3 -y
  ```

---

## 👤 Автор

Evgeniy — учебный проект по оркестрации ETL-процессов.
