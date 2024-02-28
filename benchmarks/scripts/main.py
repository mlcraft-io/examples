import asyncio
import time

from graphql_client import Client
from graphql_client.input_types import (
    datasources_insert_input,
    branches_arr_rel_insert_input,
    branches_insert_input,
    branch_statuses_enum,
    versions_insert_input,
    dataschemas_arr_rel_insert_input,
    dataschemas_insert_input,
)
import requests


HASURA_GRAPHQL_URL = "http://localhost/v1/graphql"
LOGIN_URL = "http://localhost/auth/login"
CUBE_LOAD_URL = "http://localhost/api/v1/load"

USER_LOGIN = "demo@synmetrix.org"
USER_PASS = "demodemo"

test_db_params = {
    "database": "synmetrix_test",
    "host": "postgres_test",
    "password": "test_pg",
    "port": "5432",
    "user": "test_pg",
}


def hasura_client(url=HASURA_GRAPHQL_URL, headers={}):
    client = Client(
        url,
        headers,
    )

    return client


def login(email, password):
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "email": email,
        "password": password,
        "cookie": False,
    }

    response = requests.post(LOGIN_URL, headers=headers, json=data)
    return response.json()


def load_cube_data(jwt_token, datasource_id, branch_id, query, retry_count=0):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
        "x-hasura-datasource-id": datasource_id,
        "x-hasura-branch-id": branch_id,
    }
    data = {
        "query": query,
    }
    response = requests.post(CUBE_LOAD_URL, headers=headers, json=data)
    if response.status_code == 200 and response.json().get("error") == "Continue wait":
        if retry_count < 20:
            return load_cube_data(
                jwt_token, datasource_id, branch_id, query, retry_count + 1
            )
    return response.json()


async def current_user(jwt_token, user_id):
    client = hasura_client(HASURA_GRAPHQL_URL, {"Authorization": f"Bearer {jwt_token}"})
    current_user_data = await client.current_user(user_id)
    current_user = current_user_data.users_by_pk

    if current_user is None:
        raise Exception("Failed to get current user")

    team_id = current_user.members[0].team.id

    return team_id, current_user.id


async def create_data_source(jwt_token, team_id, user_id):
    client = hasura_client(HASURA_GRAPHQL_URL, {"Authorization": f"Bearer {jwt_token}"})

    new_data_source_data = await client.create_data_source(
        datasources_insert_input(
            name="Test Data Source",
            team_id=team_id,
            branches=branches_arr_rel_insert_input(
                data=[
                    branches_insert_input(
                        user_id=user_id,
                        status=branch_statuses_enum.active,
                    ),
                ],
            ),
            db_params=test_db_params,
            db_type="POSTGRES",
        )
    )

    new_data_source = new_data_source_data.insert_datasources_one

    if new_data_source is None:
        raise Exception("Failed to create data source")

    new_data_source_id = new_data_source.id
    branch_id = new_data_source.branches[0].id
    return new_data_source_id, branch_id


async def create_version(jwt_token, datasource_id, branch_id, user_id, code):
    client = hasura_client(HASURA_GRAPHQL_URL, {"Authorization": f"Bearer {jwt_token}"})

    new_version_data = await client.create_version(
        versions_insert_input(
            checksum="1",
            branch_id=branch_id,
            user_id=user_id,
            dataschemas=dataschemas_arr_rel_insert_input(
                data=[
                    dataschemas_insert_input(
                        name="Orders.yml",
                        user_id=user_id,
                        datasource_id=datasource_id,
                        code=code,
                    )
                ]
            ),
        )
    )

    new_version = new_version_data.insert_versions_one

    if new_version is None:
        raise Exception("Failed to create version")

    new_version_id = new_version.id
    return new_version_id


async def delete_datasource(jwt_token, datasource_id):
    client = hasura_client(HASURA_GRAPHQL_URL, {"Authorization": f"Bearer {jwt_token}"})
    await client.delete_data_source(datasource_id)


async def test_cache(jwt_token, datasource_id, branch_id, user_id):
    code = ""
    with open("data_models/orders.yml", "r") as file:
        code = file.read()

    await create_version(jwt_token, datasource_id, branch_id, user_id, code)

    load_benchmark = []
    for i in range(10):
        print(f"Trial {i + 1}")
        start_time = time.time()
        load_cube_data(
            jwt_token,
            datasource_id,
            branch_id,
            {
                "measures": ["Orders.amount"],
                "timeDimensions": [
                    {
                        "dimension": "Orders.createdAt",
                        "granularity": "month",
                        "dateRange": ["1997-01-01", "2017-01-01"],
                    }
                ],
            },
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        load_benchmark.append(elapsed_time)
        print(f"Elapsed time: {elapsed_time} seconds")

    avg_load_time = sum(load_benchmark) / len(load_benchmark)
    max_load_time = max(load_benchmark)
    min_load_time = min(load_benchmark)

    pct_change = ((max_load_time - min_load_time) / min_load_time) * 100
    pct_change_avg = ((max_load_time - avg_load_time) / avg_load_time) * 100

    print(f"Trials: {len(load_benchmark)}, Average Load Time: {avg_load_time} seconds")
    print(
        f"Max Load Time: {max_load_time} seconds, Min Load Time: {min_load_time} seconds"
    )
    print(
        f"Min/Max % Change: {round(pct_change)}%, Avg/Max % Change: {round(pct_change_avg)}%"
    )


async def test_preaggregations(jwt_token, datasource_id, branch_id, user_id):
    code = ""
    with open("data_models/orders_with_preaggregations.yml", "r") as file:
        code = file.read()

    await create_version(jwt_token, datasource_id, branch_id, user_id, code)

    load_benchmark = []
    for i in range(10):
        print(f"Trial {i + 1}")
        start_time = time.time()
        load_cube_data(
            jwt_token,
            datasource_id,
            branch_id,
            {
                "measures": ["Orders.amount"],
                "timeDimensions": [
                    {
                        "dimension": "Orders.createdAt",
                        "granularity": "month",
                        "dateRange": ["1997-01-01", "2017-01-01"],
                    }
                ],
            },
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        load_benchmark.append(elapsed_time)
        print(f"Elapsed time: {elapsed_time} seconds")

    avg_load_time = sum(load_benchmark) / len(load_benchmark)
    max_load_time = max(load_benchmark)
    min_load_time = min(load_benchmark)

    pct_change = ((max_load_time - min_load_time) / min_load_time) * 100
    pct_change_avg = ((max_load_time - avg_load_time) / avg_load_time) * 100

    print(f"Trials: {len(load_benchmark)}, Average Load Time: {avg_load_time} seconds")
    print(
        f"Max Load Time: {max_load_time} seconds, Min Load Time: {min_load_time} seconds"
    )
    print(
        f"Min/Max % Change: {round(pct_change)}%, Avg/Max % Change: {round(pct_change_avg)}%"
    )


async def main():
    user_data = login(USER_LOGIN, USER_PASS)

    if "jwt_token" not in user_data:
        print("Failed to login")
        return

    jwt_token = user_data["jwt_token"]
    user_id = user_data["user"]["id"]

    team_id, user_id = await current_user(jwt_token, user_id)

    new_data_source_id, branch_id = await create_data_source(
        jwt_token, team_id, user_id
    )

    print("==== Testing cache ====")
    await test_cache(jwt_token, new_data_source_id, branch_id, user_id)

    print("==== Testing preaggregations ====")
    await test_preaggregations(jwt_token, new_data_source_id, branch_id, user_id)

    await delete_datasource(jwt_token, new_data_source_id)


asyncio.run(main())
