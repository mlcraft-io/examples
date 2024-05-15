# Benchmarks

This directory contains benchmarks for the Synmetrix backend. The benchmarks are

- Cube caching benchmark
- Cube pre-aggregations (materialized views) benchmark
- Synmetrix with Cube Highload benchmark: 1000 datasources with 1000 metrics each (1M metrics in total)

## Software Requirements

- [Docker](https://docs.docker.com/install)
- [Node.js (Version 20.8.1 or above)](https://nodejs.org/en/download/)
- [Yarn](https://yarnpkg.com/getting-started/install)
- [Python 3.9](https://www.python.org/downloads/)

# Getting Started

To run the benchmarks, you need to have Synmetrix a specific test environment running. 
The test environment is a docker swarm services with cube and hasura replicas to simulate a real-world environment. [Test data](https://github.com/mlcraft-io/mlcraft/blob/main/tests/data/orders.sql) is generated and stored in PostgreSQL database.
The test environment is described in the `docker-compose.test.yml` file in the root of the [Synmetrix repository](https://github.com/mlcraft-io/mlcraft/blob/main/docker-compose.test.yml).

### Clone this repository:

```bash
git clone https://github.com/mlcraft-io/examples
```

and navigate to the `benchmarks` folder:

```bash
cd examples/benchmarks
```

1. Clone the Synmetrix repository:

```bash
git clone https://github.com/mlcraft-io/mlcraft && cd mlcraft
```

2. Start the test Docker Swarm stack:

```bash
./cli.sh swarm up --init --env test synmetrix-test
```

3. Run migrations:

```bash
./migrate.sh
```

NOTE: Benchmarks uses Synmetrix seed data to run tests from `demo@synmetrix.org` user.

4. Run the benchmarks:

```bash
cd ../ && ./run-benchmarks.sh
```

5. Stop the test Docker Swarm stack:

```bash
cd mlcraft && ./cli.sh swarm destroy synmetrix-test
```

# Results

The results of the benchmarks are stored in the `results` directory. The results are stored in the `csv` format representing the benchmark results in a tabular format.
Data from the `csv` files can be visualized using any data visualization tool like Excel, Google Sheets, or any other tool.

