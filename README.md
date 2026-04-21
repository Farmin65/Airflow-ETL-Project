# ETL-пайплайн на Apache Airflow

![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=apache-airflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)

## О проекте

Проект представляет собой учебный ETL-пайплайн, построенный на Apache Airflow. Основная цель — автоматизировать ежедневную обработку данных и подготовить их для аналитической отчётности.

### Что делается с данными

Пайплайн выполняет полный цикл обработки:

1. **Извлечение (Extract)** — чтение сырого CSV-файла с данными о заказах. Если файл отсутствует, система автоматически генерирует тестовый набор данных для демонстрации работы.

2. **Трансформация (Transform)** — очистка и подготовка данных:
   - Приведение колонки `price` к числовому типу с удалением лишних символов
   - Парсинг дат с обработкой некорректных значений и заполнение пропусков текущей датой
   - Расчёт вычисляемого поля `total_amount` (цена × количество)
   - Фильтрация записей с отрицательным или нулевым количеством товара

3. **Загрузка (Load)** — сохранение очищенных данных в базу SQLite для последующего анализа.

4. **Проверка (Verify)** — контрольная задача, выводящая количество загруженных записей.

### Состав исходных данных

| Поле | Тип | Описание |
|------|-----|----------|
| `order_id` | int | Уникальный идентификатор заказа |
| `product` | str | Наименование товара |
| `price` | float | Цена за единицу товара |
| `quantity` | int | Количество единиц в заказе |
| `order_date` | date | Дата оформления заказа |

### Выходные данные

После обработки в таблице `cleaned_sales` появляются все исходные поля плюс вычисляемое поле `total_amount`, готовое для построения отчётов по выручке.

### Особенности реализации

- Код разделён на независимые модули (`extract`, `transform`, `load`) для удобства тестирования и поддержки
- DAG спроектирован с учётом зависимостей: каждая следующая задача выполняется только после успешного завершения предыдущей
- Настроен автоматический перезапуск задач при сбоях (1 повтор через 5 минут)

## Пример данных до и после обработки

### До обработки (сырые данные)

Файл `sales_data_2026.csv`:

| order_id | product | price | quantity | order_date |
|----------|---------|-------|----------|------------|
| 101 | Laptop | 1200.50 | 1 | 2026-04-15 |
| 102 | Mouse | 25 | 5 | 2026-04-16 |
| 103 | Keyboard | 45.00 | 3 | 2026-04-16 |
| 104 | Monitor | 300 | 2 | bad_date |
| 105 | Laptop | 1250.00 | 1 | 2026-04-17 |

**Проблемы исходных данных:**
- Колонка `price` имеет неконсистентный формат (где-то с нулями, где-то без)
- В колонке `order_date` присутствует некорректное значение `bad_date`
- Отсутствует поле с итоговой суммой заказа

---

### После обработки (очищенные данные)

Файл `sales_clean.csv` и таблица `cleaned_sales` в `sales.db`:

| order_id | product | price | quantity | order_date | total_amount |
|----------|---------|-------|----------|------------|--------------|
| 101 | Laptop | 1200.5 | 1 | 2026-04-15 | 1200.5 |
| 102 | Mouse | 25.0 | 5 | 2026-04-16 | 125.0 |
| 103 | Keyboard | 45.0 | 3 | 2026-04-16 | 135.0 |
| 104 | Monitor | 300.0 | 2 | 2026-04-21 | 600.0 |
| 105 | Laptop | 1250.0 | 1 | 2026-04-17 | 1250.0 |

**Что изменилось:**
- Колонка `price` приведена к единому числовому формату `float`
- Некорректная дата `bad_date` заменена на текущую дату запуска пайплайна
- Добавлено вычисляемое поле `total_amount = price × quantity`
- Все данные сохранены в SQLite базу для дальнейшего анализа

---

### Структура базы данных

Файл `sales.db` содержит таблицу `cleaned_sales` со следующей схемой:

```sql
CREATE TABLE cleaned_sales (
    order_id INTEGER,
    product TEXT,
    price REAL,
    quantity INTEGER,
    order_date TEXT,
    total_amount REAL
);
```

Пример SQL-запроса для проверки общей выручки по товарам:

```sql
SELECT 
    product, 
    SUM(total_amount) as revenue 
FROM cleaned_sales 
GROUP BY product 
ORDER BY revenue DESC;
```

Результат выполнения:

| product | revenue |
|---------|---------|
| Laptop | 2450.5 |
| Monitor | 600.0 |
| Keyboard | 135.0 |
| Mouse | 125.0 |


## Выполнение пайплайна

![Успешный запуск DAG в Airflow](airflow_dag_success.jpg)

*Все 5 задач выполненены успешно.*

---

## Структура проекта

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

## Технологии

| Компонент | Назначение |
|-----------|------------|
| Apache Airflow 3.0+ | Оркестрация и расписание задач |
| Python 3.12 | Основной язык разработки |
| Pandas | Обработка и очистка данных |
| SQLite | Хранение финальных данных |
| Ubuntu 22.04 | Окружение для запуска |

---

## Схема DAG

```
prepare_environment → extract_from_source → transform_and_cleanse → load_to_sqlite → check_row_count
```

---

## Установка и запуск

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

Убедитесь, что в `transform.py` и `load.py` указаны корректные пути до `~/airflow/data/` и `~/airflow/db/`.

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

Перейти по адресу:
```
http://localhost:8080
```
Логин: `admin`
Пароль: `admin` (или тот, что был задан при создании пользователя)

---

## Запуск DAG

В интерфейсе Airflow найдите DAG `student_sales_etl_pipeline`, нажмите на Play и выберите **Trigger DAG**.

---

## Проверка результата

```bash
sqlite3 ~/airflow/db/sales.db "SELECT * FROM cleaned_sales LIMIT 5;"
```

---

