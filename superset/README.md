# Integrating Synmetrix with Apache Superset

[Apache Superset][superset] is a leading open-source tool for data exploration and visualization, enabling users to dive deep into datasets and extract meaningful insights. For those seeking a managed Superset experience, [Preset][preset] provides a hassle-free, fully-managed Superset service.

## Connecting Synmetrix to Superset Using SQL API

Synmetrix, with its robust SQL API, allows for a straightforward connection to Apache Superset, making it easy to visualize data managed by Synmetrix.

### Setting Up the Connection

Connecting Apache Superset to Synmetrix treats Synmetrix as a PostgreSQL database, thanks to the SQL API provided by Synmetrix. This approach simplifies the integration process, enabling users to quickly set up and start visualizing their data.

### Configuring Synmetrix with Superset

1. Start Synmetrix and Superset using Docker Compose provided in this directory. Run the following command to start the services:

```bash
docker-compose pull synmetrix && docker-compose up -d 
```

Before proceeding, ensure you have gone through the [Synmetrix Quick Start guide](https://docs.synmetrix.org/docs/quickstart#step-3-explore-synmetrix).

Synmetrix provided with seed data for the demo purposes.

2. Set up the Superset database, users, and roles:

```bash
./init-superset.sh
```

The default credentials are `admin` for both username and password. Feel free to modify these as needed.

### Apache Superset Connection

In Apache Superset, navigate to **Data > Databases** and choose **+ Database** to add a new database connection. Use the Synmetrix SQL API credentials for configuration:

![Apache Superset: databases page](https://ucarecdn.com/cb3fe91a-6ce2-4c0e-8997-fdb2d4507beb/)

Use the following credentials to configure the connection:

| Host      | Port  | Database | User                 | Password              |
|-----------|-------|----------|----------------------|-----------------------|
| synmetrix | 15432 | db       | demo_pg_user         | demo_pg_pass          |

## Querying Data from Synmetrix in Superset

After establishing the connection, Synmetrix's data models become accessible as tables in Superset. This allows users to create datasets and design charts using Synmetrix's structured data models. For example, consider a data model for "orders":

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

This configuration enables the `orders` table to be used in Superset for creating insightful visualizations, leveraging measures and dimensions defined in Synmetrix for comprehensive data analysis.

By connecting Synmetrix to Apache Superset, users gain the ability to visualize and interact with their data in a powerful and intuitive manner, enhancing data-driven decision-making processes across the organization.


## Worth to check out

* [Superset](https://superset.apache.org/)
* [Preset](https://preset.io)
* [Data Models](https://docs.synmetrix.org/docs/core-concepts/data-models)
* [SQL API](https://docs.synmetrix.org/docs/core-concepts/sql-interface)