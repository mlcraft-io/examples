# Интеграция Synmetrix с Apache Superset

[Superset](https://superset.apache.org/) — это ведущий инструмент с открытым исходным кодом для исследования данных и визуализации, который позволяет пользователям глубоко погружаться в наборы данных и извлекать значимые инсайты. Для тех, кто ищет облачное решение Superset, [Preset](https://preset.io) предоставляет широкий сервис.

## Подключение Synmetrix к Superset с использованием SQL API

Synmetrix с его надежным SQL API позволяет легко подключаться к Apache Superset, что упрощает визуализацию данных, управляемых Synmetrix.

### Настройка Соединения

Подключение Apache Superset к Synmetrix превращает Synmetrix в базу данных PostgreSQL за счет SQL API, которое предоставляет Synmetrix. Этот метод упрощает интеграцию и позволяет пользователям быстро начать визуализацию данных.

### Конфигурирование Synmetrix с Superset

Перед началом убедитесь, что следующее программное обеспечение установлено:
  - [Docker](https://docs.docker.com/install)
  - [Docker Compose](https://docs.docker.com/compose/install)

Клонируйте этот репозиторий:

```bash
git clone https://github.com/mlcraft-io/examples
```

и перейдите в папку `superset`:

```bash
cd examples/superset
```

1. Используйте Docker Compose из этого каталога для запуска Synmetrix и Superset. Для начала работы с сервисами выполните следующую команду:

```bash
./1-start-containers.sh
```

Перед продолжением убедитесь, что вы ознакомились с [Руководством по быстрому старту Synmetrix](https://docs.synmetrix.org/docs/quickstart#step-3-explore-synmetrix).

Synmetrix предоставляет начальные данные для демонстрационных целей.

2. Настройте базу данных, пользователей и роли Superset:

```bash
./2-setup-superset.sh
```

Стандартные учетные данные — это `admin` для имени пользователя и пароля. При необходимости вы можете их изменить.

Дождитесь, пока сервисы не будут запущены и работают. Вы можете проверить статус сервисов с помощью следующей команды:

```bash
./3-show-logs.sh
```

ПРИМЕЧАНИЕ: для остановки сервисов и удаления томов выполните следующую команду:

```bash
./4-stop-containers.sh
```

### Соединение с Apache Superset

1. Перейдите на: `http://localhost:9999`

2. В Apache Superset перейдите в раздел **Настройки -> Соединения с базами данных** и выберите **+ База данных** для добавления нового соединения с базой данных. Используйте учетные данные SQL API Synmetrix для конфигурации:

![Страница баз данных Apache Superset](https://ucarecdn.com/ac22a3f4-302e-4986-a116-c13cc6f5887d/-/preview/1000x574/)

Используйте следующие учетные данные для настройки соединения:

| Хост      | Порт  | База данных | Пользователь         | Пароль                |
|-----------|-------|-------------|----------------------|-----------------------|
| synmetrix | 15432 | db          | demo_pg_user         | demo_pg_pass          |

## Запрос данных из Synmetrix в Superset

После установления соединения данные Synmetrix становятся доступны как таблицы в Superset. Это позволяет пользователям создавать наборы данных и проектировать диаграммы, использу

я структурированные модели данных Synmetrix. Например, рассмотрим модель данных для "orders":

```yaml
cubes:
  - name: orders
    sql: SELECT * FROM orders

    measures:
      - name: count
        sql: COUNT(*)
        type: count

    dimensions:
      - name: status
        sql: status
        type: string

      - name: created_at
        sql: created_at
        type: time
```

Эта конфигурация позволяет использовать таблицу `orders` в Superset для создания информативных визуализаций, используя меры и измерения, определенные в Synmetrix для всестороннего анализа данных.

Подключение Synmetrix к Apache Superset дает пользователям возможность наглядно работать с их данными и улучшать процессы принятия решений на основе данных в организации.

### Видеоурок

[![](https://img.youtube.com/vi/TzLy88IAYZo/0.jpg)](https://youtu.be/TzLy88IAYZo)

## Стоит обратить внимание

* [Superset](https://superset.apache.org/)
* [Preset](https://preset.io)
* [Модели данных](https://docs.synmetrix.org/docs/core-concepts/data-models)
* [SQL API](https://docs.synmetrix.org/docs/core-concepts/sql-interface)