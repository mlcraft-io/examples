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
import csv
import yaml

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


async def load_cube_data(
    jwt_token, datasource_id, branch_id, query, retry_count=0, timeout=60
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
        "x-hasura-datasource-id": datasource_id,
        "x-hasura-branch-id": branch_id,
    }
    data = {
        "query": query,
    }
    response = await asyncio.to_thread(
        requests.post, CUBE_LOAD_URL, headers=headers, json=data, timeout=timeout
    )
    if response.status_code == 200 and response.json().get("error") == "Continue wait":
        if retry_count < 20:
            await asyncio.sleep(5)
            return await load_cube_data(
                jwt_token, datasource_id, branch_id, query, retry_count + 1, timeout
            )
    if response.status_code != 200:
        raise Exception(
            f"Failed to load cube data: {response.status_code} {response.text}"
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


async def create_data_source(jwt_token, team_id, user_id, name="Test Data Source"):
    client = hasura_client(HASURA_GRAPHQL_URL, {"Authorization": f"Bearer {jwt_token}"})

    new_data_source_data = await client.create_data_source(
        datasources_insert_input(
            name=name,
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


async def create_version(jwt_token, datasource_id, branch_id, user_id, code, models=[]):
    client = hasura_client(HASURA_GRAPHQL_URL, {"Authorization": f"Bearer {jwt_token}"})

    if len(models) == 0:
        data = [
            dataschemas_insert_input(
                name="Orders.yml",
                user_id=user_id,
                datasource_id=datasource_id,
                code=code,
            )
        ]
    else:
        data = models

    new_version_data = await client.create_version(
        versions_insert_input(
            checksum="1",
            branch_id=branch_id,
            user_id=user_id,
            dataschemas=dataschemas_arr_rel_insert_input(data=data),
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


def save_trials_to_csv(trials, filename):
    # Write trials data to CSV
    with open(filename, "w", newline="") as file:
        file.truncate(0)  # Clear the file before writing
        writer = csv.writer(file)
        writer.writerow(["Trial", "Elapsed Time"])
        for i, elapsed_time in enumerate(trials, start=1):
            writer.writerow([i, elapsed_time])

    return True


def save_highload_test_to_csv(trials, filename):
    # Write trials data to CSV
    with open(filename, "w", newline="") as file:
        file.truncate(0)  # Clear the file before writing
        writer = csv.writer(file)
        writer.writerow(
            [
                "Trial",
                "Models Count",
                "Metrics Count",
                "Test Query Rows Count",
                "Elapsed Time",
            ]
        )
        for i, row in enumerate(trials, start=1):
            writer.writerow([i, row[0], row[1], row[2], row[3]])

    return True


async def test_cache(jwt_token, datasource_id, branch_id, user_id):
    code = ""
    with open("data_models/version_1/orders.yml", "r") as file:
        code = file.read()

    await create_version(jwt_token, datasource_id, branch_id, user_id, code)

    load_benchmark = []
    for i in range(50):
        print(f"Trial {i + 1}")
        start_time = time.time()
        await load_cube_data(
            jwt_token,
            datasource_id,
            branch_id,
            {
                "measures": ["OrdersVersion1.amount"],
                "timeDimensions": [
                    {
                        "dimension": "OrdersVersion1.createdAt",
                        "granularity": "month",
                        "dateRange": ["1997-01-01", "2017-01-01"],
                    }
                ],
            },
            timeout=300,
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        load_benchmark.append(elapsed_time)
        print(f"Elapsed time: {elapsed_time} seconds")

    avg_load_time = sum(load_benchmark) / len(load_benchmark)
    max_load_time = max(load_benchmark)
    min_load_time = min(load_benchmark)

    save_trials_to_csv(load_benchmark, "results/test_cache.csv")

    print(f"Trials: {len(load_benchmark)}, Average Load Time: {avg_load_time} seconds")
    print(
        f"Max Load Time: {max_load_time} seconds, Min Load Time: {min_load_time} seconds"
    )


async def test_preaggregations(
    jwt_token,
    datasource_id,
    branch_id,
    user_id,
    version=True,
):
    if version:
        code = ""
        with open("data_models/version_2/orders_with_preaggregations.yml", "r") as file:
            code = file.read()

        await create_version(jwt_token, datasource_id, branch_id, user_id, code)

    load_benchmark = []
    for i in range(50):
        print(f"Trial {i + 1}")
        start_time = time.time()
        await load_cube_data(
            jwt_token,
            datasource_id,
            branch_id,
            {
                "measures": ["OrdersVersion2.amount"],
                "timeDimensions": [
                    {
                        "dimension": "OrdersVersion2.createdAt",
                        "granularity": "month",
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

    filename = (
        "results/test_preaggregations_1st_run.csv"
        if version
        else "results/test_preaggregations_2nd_run.csv"
    )
    save_trials_to_csv(load_benchmark, filename)

    print(f"Trials: {len(load_benchmark)}, Average Load Time: {avg_load_time} seconds")
    print(
        f"Max Load Time: {max_load_time} seconds, Min Load Time: {min_load_time} seconds"
    )


async def test_1mil_metrics(jwt_token, datasource_id, branch_id, user_id, n):
    models = []

    print(f"Inserting model models_{n}.yml")

    code = ""
    measures_count = 0
    with open(f"data_models/version_3/models_{n}.yml", "r") as file:
        code = file.read()
        yaml_tree = yaml.safe_load(code)
        measures_count = len(yaml_tree["cubes"][0]["measures"])
        models.append(
            dataschemas_insert_input(
                name=f"Orders_{n}.yml",
                user_id=user_id,
                datasource_id=datasource_id,
                code=code,
            )
        )

    await create_version(jwt_token, datasource_id, branch_id, user_id, None, models)

    rows_len = 0
    start_time = time.time()
    try:
        res = await load_cube_data(
            jwt_token,
            datasource_id,
            branch_id,
            {
                "measures": [f"Orders_{n}.measure_0"],
                "timeDimensions": [
                    {
                        "dimension": f"Orders_{n}.createdAt",
                        "granularity": "month",
                        "dateRange": ["1997-01-01", "2017-01-01"],
                    }
                ],
            },
        )
        rows_len = len(res["data"])
    except Exception as e:
        print(e)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return (len(models), measures_count, rows_len, elapsed_time)


async def main():
    user_data = login(USER_LOGIN, USER_PASS)

    if "jwt_token" not in user_data:
        print("Failed to login")
        return

    jwt_token = user_data["jwt_token"]
    user_id = user_data["user"]["id"]

    team_id, user_id = await current_user(jwt_token, user_id)

    # test queries cache
    print("==== Testing cache ====")
    new_data_source_id, branch_id = await create_data_source(
        jwt_token, team_id, user_id
    )
    await test_cache(jwt_token, new_data_source_id, branch_id, user_id)
    await delete_datasource(jwt_token, new_data_source_id)

    # test preaggregations
    print("==== Testing preaggregations ====")
    new_data_source_id, branch_id = await create_data_source(
        jwt_token, team_id, user_id
    )
    await test_preaggregations(jwt_token, new_data_source_id, branch_id, user_id)
    print("==== Testing preaggregations again ====")
    await test_preaggregations(
        jwt_token, new_data_source_id, branch_id, user_id, version=False
    )
    await delete_datasource(jwt_token, new_data_source_id)

    # test 1 million metrics
    print("==== Testing 1000 datasources with 1000 metrics ====")

    new_datasources = []
    trials = []
    for i in range(999):
        print(f"Creating datasource {i+1}")

        new_data_source_id, branch_id = await create_data_source(
            jwt_token, team_id, user_id, name=f"Test Data Source {i+1}"
        )

        trial = await test_1mil_metrics(
            jwt_token, new_data_source_id, branch_id, user_id, i
        )
        trials.append(trial)
        new_datasources.append(new_data_source_id)

    save_highload_test_to_csv(trials, "results/test_1mil_metrics.csv")

    for new_data_source_id in new_datasources:
        await delete_datasource(jwt_token, new_data_source_id)


asyncio.run(main())
