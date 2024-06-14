# Integrating Synmetrix with Vanna+Chainlit

[Chainlit](https://github.com/Chainlit/chainlit) — is a versatile asynchronous Python framework that enables the creation of scalable applications for conversational artificial intelligence and agent applications. Providing support for interfaces like ChatGPT, embedded chatbots, customizable user interfaces, and integration with other platforms.
[Vanna](https://github.com/vanna-ai/vanna) — is an open-source framework for generating SQL queries and related functions. Developed in Python, Vanna utilizes Retrieval-Augmented Generation (RAG) technology, which significantly simplifies the process of working with data and speeds up the retrieval of necessary information, easily converting natural language questions into precise SQL queries, making working with databases more accessible and efficient.

### Configuring Synmetrix with Vanna+Chainlit

Before getting started, ensure the following software is installed:
  - [Docker](https://docs.docker.com/install)
  - [Docker Compose](https://docs.docker.com/compose/install)

Clone this repository:

```bash
git clone https://github.com/mlcraft-io/examples
```

and navigate to the `vannaai` folder:

```bash
cd examples/vannaai
```

1. Set your OpenAI API key in the OPENAI_API_KEY variable in the .env file.

2. Use Docker Compose from this directory to start Synmetrix and Vanna+Chainlit. To get started, execute the following command:

```bash
./1-start-containers.sh
```

Before proceeding, ensure you have reviewed the [Synmetrix Quick Start Guide](https://docs.synmetrix.org/docs/quickstart#step-3-explore-synmetrix).

Wait until the services are up and running. You can check the status of services using the following command:

```bash
./2-show-logs.sh
```

NOTE: To stop the services and remove volumes, execute the following command:

```bash
./3-stop-containers.sh
```

### Using Synmetrix Integration with Vanna+Chainlit

1. Go to: `http://localhost:8000`

The integration of Synmetrix with Vanna+Chainlit allows users to retrieve data using large language models (LLMs), eliminating the need to write SQL queries. Browse generated SQL queries and charts.

## Key References

* [Chainlit](https://github.com/Chainlit/chainlit)
* [Vanna](https://github.com/vanna-ai/vanna)
* [SQL API](https://docs.synmetrix.org/docs/core-concepts/sql-interface)