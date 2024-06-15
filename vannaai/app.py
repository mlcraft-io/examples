import os
from urllib.parse import urlparse
from typing import Optional
import pandas as pd

import chainlit as cl
import chainlit.data as cl_data
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")
CHAINLIT_PG_CONNECTION_STRING = os.getenv(
    "CHAINLIT_PG_CONNECTION_STRING",
    "postgresql+asyncpg://chainlit:pg_pass@chainlit-postgres:5432/chainlit",
)
QDRANT_URL = os.getenv("QDRANT_URL")

cl_data._data_layer = SQLAlchemyDataLayer(conninfo=CHAINLIT_PG_CONNECTION_STRING)


class Vanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


vn = Vanna(
    {
        "url": QDRANT_URL,
        "api_key": OPENAI_API_KEY,
        "model": "gpt-4o",
    }
)

url = urlparse(PG_CONNECTION_STRING)
vn.connect_to_postgres(
    host=url.hostname,
    port=url.port,
    user=url.username,
    password=url.password,
    dbname=url.path[1:],  # Strip the leading '/' from the path to get the database name
)

df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

plan = vn.get_training_plan_generic(df_information_schema)

vn.train(plan=plan)


ASSISTANT_NAME = "Synmetrix"


def gen_query_recursive(human_query: str, trials: int = 3):
    sql_query = vn.generate_sql(human_query)

    if trials == 0:
        raise ValueError("Query is not a valid SQL query")

    if not vn.is_sql_valid(sql_query):
        sql_query = gen_query_recursive(human_query, trials - 1)

    return sql_query


@cl.step(name="Generate SQL", type="tool", language="sql", show_input=False)
async def gen_query(human_query: str):
    sql_query = gen_query_recursive(human_query)
    return sql_query


@cl.step(name="Preview dataframe", type="tool", show_input=False)
async def preview_df(df: pd.DataFrame):
    return df.to_markdown(index=False)


@cl.step(name="Generate plotly code", type="tool", language="python", show_input=False)
async def generate_plotly_code(human_query, sql, df):
    return vn.generate_plotly_code(question=human_query, sql=sql, df=df)


@cl.step(name="Plot", show_input=False)
async def plot(human_query, sql, df):
    current_step = cl.context.current_step
    plotly_code = await generate_plotly_code(human_query, sql, df)
    fig = vn.get_plotly_figure(plotly_code=plotly_code, df=df)

    current_step.output = plotly_code
    return fig


@cl.step(type="run", name=ASSISTANT_NAME)
async def chain(human_query: str):
    if vn.is_sql_valid(human_query):
        sql_query = human_query
    else:
        sql_query = await gen_query(human_query)

    try:
        df = vn.run_sql(sql_query)
        await preview_df(df)

        fig = await plot(human_query, sql_query, df)
        elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

        await cl.Message(
            content=human_query, elements=elements, author=ASSISTANT_NAME
        ).send()
    except ValueError as e:
        await cl.Message(content=f"Query failed: {e}", author=ASSISTANT_NAME).send()


@cl.on_message
async def main(message: cl.Message):
    await chain(message.content)


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    if (username, password) == ("admin", "admin"):
        return cl.User(identifier="admin")
    else:
        return None


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name=" ",
            icon="/public/avatars/default.png",
            markdown_description="The underlying LLM model is **GPT-4o**",
            starters=[
                cl.Starter(
                    label="Show all available cubes",
                    message="Show all available tables in the database",
                    icon="/public/starter-icon.png",
                ),
            ],
        )
    ]
