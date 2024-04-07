## Руководство по подключению Synmetrix к DBeaver с использованием SQL API

Подключение SQL API Synmetrix через клиент PostgreSQL, например, DBeaver, предоставляет продвинутый интерфейс для выполнения SQL-запросов к вашим моделям данных. В этом руководстве описывается процесс установления связи с DBeaver и предлагаются альтернативные клиенты PostgreSQL для гибкости вашего рабочего процесса.

### Начало работы

Прежде чем продолжить, убедитесь, что вы выполнили [Быстрый старт Synmetrix](https://docs.synmetrix.org/docs/quickstart#prerequisite-software).

### Настройка DBeaver для Synmetrix

1. **Установите DBeaver**: Скачайте и установите DBeaver с [https://dbeaver.io/](https://dbeaver.io/).

2. **Новое подключение к PostgreSQL**: В DBeaver кликните правой кнопкой мыши в панели Database Navigator и выберите `New > Database Connection`. Выберите PostgreSQL в качестве типа базы данных.

3. **Введите детали подключения**: Введите учетные данные SQL интерфейса Synmetrix:
   - **Хост**: localhost
   - **Порт**: 15432
   - **База данных**: db (Используйте реальное имя базы данных, предоставленное Synmetrix.)
   - **Имя пользователя**: demo_pg_user
   - **Пароль**: demo_pg_pass

4. **Проверьте соединение**: Нажмите "Test Connection" для проверки настроек, затем "Finish", чтобы сохранить соединение.

5. **SQL Консоль**: Перейдите к вашему соединению в DBeaver, откройте его и используйте SQL-редактор/консоль для начала работы с вашими моделями данных.

### Примеры SQL-запросов

Выполните следующие примеры запросов для взаимодействия с вашими моделями данных Synmetrix:

#### Запрос заказов

```sql
SELECT * FROM orders ORDER BY createdAt LIMIT 3;
```

Результат:
```
count|number|status    |createdAt              |completedAt            |__user|__cubeJoinField|
-----+------+----------+-----------------------+-----------------------+------+---------------+
    1|  78.0|processing|2019-01-02 00:00:00.000|2019-01-29 00:00:00.000|      |               |
    2|  48.0|completed |2019-01-02 00:00:00.000|2019-01-27 00:00:00.000|      |               |
    1|  38.0|shipped   |2019-01-02 00:00:00.000|2019-01-17 00:00:00.000|      |               |
```

#### Агрегация заказов и продуктов

```sql
SELECT p.name, SUM(o.count) FROM orders o CROSS JOIN products p GROUP BY p.name LIMIT 5;
```

Результат:

```
name                    |SUM(o.count)|
------------------------+------------+
Tasty Plastic Mouse     |         121|
Intelligent Cotton Ball |         119|
Ergonomic Steel Tuna    |         116|
Intelligent Rubber Pants|         116|
Generic Wooden Gloves   |         116|
```

#### Группировка заказов по дате и статусу

```sql
SELECT status, DATE_TRUNC('month', createdAt) AS date, COUNT(*) 
FROM orders 
GROUP BY date, status 
ORDER BY date ASC;
```

Результат:

```
status    |date                   |COUNT(UInt8(1))|
----------+-----------------------+---------------+
processing|2019-01-01 00:00:00.000|             50|
completed |2019-01-01 00:00:00.000|             48|
shipped   |2019-01-01 00:00:00.000|             57|
shipped   |2019-02-

01 00:00:00.000|             34|
processing|2019-02-01 00:00:00.000|             39|
...
```

#### Продвинутый запрос с условной логикой

```sql
SELECT
  city,
  CASE WHEN status = 'shipped' THEN 'done' ELSE 'in-progress' END AS real_status,
  SUM(number) AS total
FROM (
  SELECT users.city, orders.number, orders.status
  FROM orders CROSS JOIN users
) AS inner_query
GROUP BY city, real_status
ORDER BY city;
```

Результат:

```
city         |real_status|total  |
-------------+-----------+-------+
Austin       |done       |20870.0|
Austin       |in-progress|40354.0|
Chicago      |done       |18307.0|
Chicago      |in-progress|40370.0|
Los Angeles  |done       |23692.0|
...
```

### Видеоурок

[![](https://img.youtube.com/vi/8l_Ud3IM0OQ/0.jpg)](https://youtu.be/8l_Ud3IM0OQ)

### Изучение других клиентов PostgreSQL

Хотя DBeaver является надежным вариантом для подключения к Synmetrix, существуют и другие клиенты, предлагающие обширные возможности для управления базами данных и выполнения SQL-запросов. Вот некоторые альтернативы:

- **psql CLI**: Официальный командный интерфейс для PostgreSQL. [Узнать больше](https://www.postgresql.org/docs/current/app-psql.html).
- **Apache Superset**: Инструмент с открытым исходным кодом для исследования данных и визуализации. [Узнать больше](https://superset.apache.org/).
- **Tableau Cloud/Desktop**: Лидирующий инструмент визуализации с облачной и настольной версиями. [Облако](https://www.tableau.com/cloud) | [Настольный](https://www.tableau.com/).
- **Power BI**: Сервис бизнес-аналитики от Microsoft. [Узнать больше](https://powerbi.microsoft.com/).
- **Metabase**: Инструмент бизнес-аналитики с открытым исходным кодом. [Узнать больше](https://www.metabase.com/).
- **Google Data Studio**: Бесплатный инструмент от Google для создания дашбордов и отчетов. [Узнать больше](https://datastudio.google.com/).
- **Excel через плагин Devart**: Подключите Excel к различным базам данных, включая PostgreSQL. [Узнать больше](https://www.devart.com/excel-addins/).
- **Deepnote**: Совместная тетрадь для данных. [Узнать больше](https://deepnote.com/).
- **Hex**: Проектная тетрадь для команд. [Узнать больше](https://hex.pm/).
- **Observable**: Создавайте, сотрудничайте и делитесь визуализациями данных. [Узнать больше](https://observablehq.com/).
- **Streamlit**: Превращайте данные скрипты в общедоступные веб-приложения. [Узнать больше](https://streamlit.io/).
- **Jupyter notebook**: Открытое веб-приложение для создания и обмена документами с живым кодом. [Узнать больше](https://jupyter.org/).
- **Hightouch**: Синхронизируйте данные между вашим озером данных и бизнес-приложениями. [Узнать больше](https://hightouch.io/).

Каждый из этих клиентов предлагает уникальные функции и возможности, делая их подходящими для различных потребностей в управлении данными и анализе. 

Рассмотрите ваши конкретные требования и предпочтения при выборе правильного инструмента для подключения к Synmetrix.