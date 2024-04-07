# Synmetrix with Large Language Model (LLM) example

This guide demonstrates how to use the Synmetrix API with the Large Language Model (LLM) to generate SQL queries from natural language questions.

## Why Semantic Layer for LLM-powered apps?
When building text-to-SQL applications, it is crucial to provide LLM with rich context about underlying data model. Without enough context it’s hard for humans to comprehend data, LLM will simply compound on that confusion to produce wrong answers.

In many cases it is not enough to feed LLM with database schema and expect it to generate the correct SQL. To operate correctly and execute trustworthy actions, it needs to have enough context and semantics about the data it consumes; it must understand the metrics, dimensions, entities, and relational aspects of the data by which it's powered. Basically—LLM needs a semantic layer.

## Getting started

Before proceeding, ensure you have completed Synmetrix's [Quick Start guide](https://docs.synmetrix.org/docs/quickstart#prerequisite-software).

### Required Software

- Python 3.9 or later
- PIP (Python package manager)

## Setting Up Synmetrix with LLM

1. Setup python environment and install the required packages:

```bash
source create-venv.sh
```

2. Copy the Synmetrix Access Token

   - Access Synmetrix: Go to the [Synmetrix Stack](https://localhost/) website and sign into your account. For demonstration, utilize the provided default seed data.
   - Retrieve the API Key: Move to the [Explore -> REST API](https://docs.synmetrix.org/docs/user-guide/explore#example-api-utilization) section and copy the API key provided there.
   - Insert the copied API key as `SYNMETRIX_ACCESS_KEY` into the `.env` file.


3. Insert OpenAI API Key

   - Access OpenAI: Go to the [OpenAI](https://platform.openai.com/) website and sign into your account.
   - Retrieve the API Key: Move to the [API Keys](https://platform.openai.com/account/api-keys) section and copy the API key provided there.
   - Insert the copied API key as `OPENAI_API_KEY` into the `.env` file.

4. Run the LLM-powered app:

```bash
streamlit run streamlit_app.py 
```

4. Visit <http://localhost:8501> to preview the project.

### Video Tutorial

[![](https://img.youtube.com/vi/TtH-pFGDK84/0.jpg)](https://youtu.be/TtH-pFGDK84)