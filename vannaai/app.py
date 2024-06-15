import os
from urllib.parse import urlparse

from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
import chainlit as cl
from chainlit.input_widget import Select


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


ASSISTANT_NAME = "Synmetrix"


@cl.step(root=True, language="sql", name=ASSISTANT_NAME)
async def gen_query(human_query: str):
    sql_query = vn.generate_sql(human_query)
    return sql_query


@cl.step(root=True, name="")
async def execute_query(query: str):
    if not vn.is_sql_valid(query):
        raise ValueError("Query is not a valid SQL query")

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


@cl.step(type="run", root=True, name=ASSISTANT_NAME)
async def chain(human_query: str):
    if vn.is_sql_valid(human_query):
        sql_query = human_query
    else:
        sql_query = await gen_query(human_query)

    try:
        df = await execute_query(sql_query)
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


@cl.on_chat_start
async def setup():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=[
                    "gpt-4o",
                    "gpt-4-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo",
                ],
                initial_index=0,
            )
        ]
    ).send()
    value = settings["Model"]
