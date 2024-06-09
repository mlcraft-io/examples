import os
from urllib.parse import urlparse

from vanna.flask import VannaFlaskApp
from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
import chainlit as cl
from chainlit.input_widget import Select
import os


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")
QDRANT_URL = os.getenv("QDRANT_URL")

class Vanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


vn = Vanna(
    {
        "url": QDRANT_URL,
        "api_key": OPENAI_API_KEY,
    }
)

url = urlparse(CONNECTION_STRING)
vn.connect_to_postgres(
    host=url.hostname,
    port=url.port,
    user=url.username,
    password=url.password,
    dbname=url.path.lstrip("/"),
)

df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

plan = vn.get_training_plan_generic(df_information_schema)

vn.train(plan=plan)


@cl.step(root=True, language="sql", name="Vanna")
async def gen_query(human_query: str):
    sql_query = vn.generate_sql(human_query)
    return sql_query


@cl.step(root=True, name="Vanna")
async def execute_query(query):
    current_step = cl.context.current_step
    df = vn.run_sql(query)
    current_step.output = df.head().to_markdown(index=False)

    return df


@cl.step(name="Plot", language="python")
async def plot(human_query, sql, df):
    current_step = cl.context.current_step
    plotly_code = vn.generate_plotly_code(question=human_query, sql=sql, df=df)
    fig = vn.get_plotly_figure(plotly_code=plotly_code, df=df)

    current_step.output = plotly_code
    return fig


@cl.step(type="run", root=True, name="Vanna")
async def chain(human_query: str):
    sql_query = await gen_query(human_query)
    df = await execute_query(sql_query)    
    fig = await plot(human_query, sql_query, df)

    elements = [cl.Plotly(name="chart", figure=fig, display="inline")]
    await cl.Message(content=human_query, elements=elements, author="Vanna").send()


@cl.on_message
async def main(message: cl.Message):
    await chain(message.content)


@cl.on_chat_start
async def setup():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                initial_index=0,
            )
        ]
    ).send()
    value = settings["Model"]