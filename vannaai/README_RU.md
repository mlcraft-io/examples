# Интеграция Synmetrix с Vanna+Chainlit

[Chainlit](https://github.com/Chainlit/chainlitmlc) — это универсальный асинхронный фреймворк на Python, который позволяет создавать масштабируемые приложения для конверсационного искусственного интеллекта и агентных приложений. Обеспечивая поддержку интерфейсов вроде ChatGPT, встроенных чат-ботов, настраиваемых пользовательских интерфейсов и интеграцию с другими платформами.
[Vanna](https://github.com/vanna-ai/vanna) — это open-source фреймворк для генерации SQL-запросов и связанных с этим функций. Разработанный на языке Python, Vanna использует технологию Retrieval-Augmented Generation (RAG), что позволяет значительно упростить процесс работы с данными и ускорить получение нужной информации, легко преобразовывать вопросы на естественном языке в точные SQL-запросы, что делает работу с базами данных более доступной и эффективной.

### Конфигурирование Synmetrix с Vanna+Chainlit

Перед началом убедитесь, что следующее программное обеспечение установлено:
  - [Docker](https://docs.docker.com/install)
  - [Docker Compose](https://docs.docker.com/compose/install)

Клонируйте этот репозиторий:

```bash
git clone https://github.com/mlcraft-io/examples
```

и перейдите в папку `vannaai`:

```bash
cd examples/vannaai
```

1. Установите API-ключ OpenAI в переменную OPENAI_API_KEY файла .env.

2. Используйте Docker Compose из этого каталога для запуска Synmetrix и Vanna+Chainlit. Для начала работы выполните следующую команду:

```bash
./1-start-containers.sh
```

Перед продолжением убедитесь, что вы ознакомились с [Руководством по быстрому старту Synmetrix](https://docs.synmetrix.org/docs/quickstart#step-3-explore-synmetrix).

Дождитесь, пока сервисы не будут запущены и работают. Вы можете проверить статус сервисов с помощью следующей команды:

```bash
./2-show-logs.sh
```

ПРИМЕЧАНИЕ: для остановки сервисов и удаления томов выполните следующую команду:

```bash
./3-stop-containers.sh
```

### Использование интеграции Synmetrix с Vanna+Chainlit

1. Перейдите на: `http://localhost:8000`

Интеграция Synmetrix с Vanna+Chainlit дает пользователям возможность получать данные с помощью больших языковых моделей (LLM), устраняя необходимость написания SQL-запросов. Просматривать сгенерированне SQL-запросы и графики.

## Стоит обратить внимание

* [Chainlit](https://github.com/Chainlit/chainlitmlc)
* [Vanna](https://github.com/vanna-ai/vanna)
* [SQL API](https://docs.synmetrix.org/docs/core-concepts/sql-interface)