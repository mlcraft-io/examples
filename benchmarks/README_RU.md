# Бенчмарки

Этот каталог содержит бенчмарки для бэкенда Synmetrix. Бенчмарки включают в себя:

- Бенчмарк кэширования OLAP-куба
- Бенчмарк предварительных агрегаций OLAP-куба (материализованные представления)
- Бенчмарк Synmetrix с высокой нагрузкой на OLAP-кубы: 1000 источников данных с 1000 метрик каждый (всего 1М метрик)

## Требования к программному обеспечению

- [Docker](https://docs.docker.com/install)
- [Node.js (версия 20.8.1 или выше)](https://nodejs.org/en/download/)
- [Node.js (Version 20.8.1 or above)](https://nodejs.org/en/download/)
- [Yarn](https://yarnpkg.com/getting-started/install)
- [Python 3.9](https://www.python.org/downloads/)

# Начало работы

Чтобы запустить бенчмарки, вам необходимо иметь запущенную специфическую тестовую среду Synmetrix. 
Тестовая среда представляет собой сервисы docker swarm с репликами cube и hasura для имитации реальной среды. [Тестовые данные](https://github.com/mlcraft-io/mlcraft/blob/main/tests/data/orders.sql) генерируются и хранятся в базе данных PostgreSQL.
Тестовая среда описана в файле `docker-compose.test.yml` в корне [репозитория Synmetrix](https://github.com/mlcraft-io/mlcraft/blob/main/docker-compose.test.yml).

1. Клонируйте репозиторий Synmetrix:

```bash
git clone https://github.com/mlcraft-io/mlcraft
cd mlcraft
```

2. Запустите стек Docker Swarm:

```bash
./cli.sh swarm up --init --env test synmetrix-test
```

3. Запустите миграции:

```bash
./migrate.sh
```

ПРИМЕЧАНИЕ: Для выполнения тестов бенчмарков используются начальные данные Synmetrix от пользователя `demo@synmetrix.org`.

4. Запустите бенчмарки:

```bash
./run-benchmarks.sh
```

5. Остановите стек Docker Swarm:

```bash
./cli.sh swarm destroy synmetrix-test
```

# Результаты

Результаты бенчмарков хранятся в папке `results`. Результаты хранятся в формате `csv`, представляющие результаты бенчмарков в табличном виде.
Данные из файлов `csv` могут быть визуализированы любым инструментом для визуализации данных, например Excel, Google Sheets или любой другой инструмент для визуализации данных.

