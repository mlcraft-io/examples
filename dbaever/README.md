## Guide to Connecting Synmetrix with DBeaver Using SQL API

Connecting Synmetrix's SQL API via a PostgreSQL client like DBeaver offers a sophisticated interface for executing SQL queries on your data models. This guide details establishing a connection with DBeaver and suggests alternative PostgreSQL clients for flexibility in your workflow.

### Getting Started

Before proceeding, ensure you have completed Synmetrix's [Quick Start guide](https://docs.synmetrix.org/docs/quickstart#prerequisite-software).

### Setting Up DBeaver for Synmetrix

1. **Install DBeaver**: Download and install DBeaver from [https://dbeaver.io/](https://dbeaver.io/).

2. **New PostgreSQL Connection**: In DBeaver, right-click in the Database Navigator pane and select `New > Database Connection`. Choose PostgreSQL as the database type.

3. **Input Connection Details**: Enter the Synmetrix SQL interface credentials:
   - **Host**: localhost
   - **Port**: 15432
   - **Database**: db (Use the actual database name provided by Synmetrix.)
   - **Username**: demo_pg_user
   - **Password**: demo_pg_pass

4. **Test Connection**: Click "Test Connection" to verify the setup, then "Finish" to save the connection.

5. **SQL Console**: Navigate to your connection in DBeaver, open it, and use the SQL editor/console to begin querying your data models.

### Sample SQL Queries

Execute the following sample queries to interact with your Synmetrix data models:

#### Query Orders

```sql
SELECT * FROM orders ORDER BY createdAt LIMIT 3;
```

Result:
```
count|number|status    |createdAt              |completedAt            |__user|__cubeJoinField|
-----+------+----------+-----------------------+-----------------------+------+---------------+
    1|  78.0|processing|2019-01-02 00:00:00.000|2019-01-29 00:00:00.000|      |               |
    2|  48.0|completed |2019-01-02 00:00:00.000|2019-01-27 00:00:00.000|      |               |
    1|  38.0|shipped   |2019-01-02 00:00:00.000|2019-01-17 00:00:00.000|      |               |
```

#### Aggregate Orders and Products

```sql
SELECT p.name, SUM(o.count) FROM orders o CROSS JOIN products p GROUP BY p.name LIMIT 5;
```

Result:

```
name                    |SUM(o.count)|
------------------------+------------+
Tasty Plastic Mouse     |         121|
Intelligent Cotton Ball |         119|
Ergonomic Steel Tuna    |         116|
Intelligent Rubber Pants|         116|
Generic Wooden Gloves   |         116|
```

#### Group Orders by Date and Status

```sql
SELECT status, DATE_TRUNC('month', createdAt) AS date, COUNT(*) 
FROM orders 
GROUP BY date, status 
ORDER BY date ASC;
```

Result:

```
status    |date                   |COUNT(UInt8(1))|
----------+-----------------------+---------------+
processing|2019-01-01 00:00:00.000|             50|
completed |2019-01-01 00:00:00.000|             48|
shipped   |2019-01-01 00:00:00.000|             57|
shipped   |2019-02-01 00:00:00.000|             34|
processing|2019-02-01 00:00:00.000|             39|
...
```

#### Advanced Query with Conditional Logic

```sql
SELECT
  city,
  CASE WHEN status = 'shipped' THEN 'done' ELSE 'in-progress' END AS real_status,
  SUM(number) AS total
FROM (
  SELECT users.city, orders.number, orders.status
  FROM orders CROSS JOIN users
) AS inner_query
GROUP BY city, real_status
ORDER BY city;
```

Result:

```
city         |real_status|total  |
-------------+-----------+-------+
Austin       |done       |20870.0|
Austin       |in-progress|40354.0|
Chicago      |done       |18307.0|
Chicago      |in-progress|40370.0|
Los Angeles  |done       |23692.0|
...
```

### Video Tutorial

[![](https://img.youtube.com/vi/8l_Ud3IM0OQ/0.jpg)](https://youtu.be/8l_Ud3IM0OQ)

### Exploring Other PostgreSQL Clients

While DBeaver is a robust option for connecting to Synmetrix, various other clients also offer comprehensive features for database management and SQL querying. Here are some alternatives:

- **psql CLI**: The official command-line tool for PostgreSQL. [Learn more](https://www.postgresql.org/docs/current/app-psql.html).
- **Apache Superset**: An open-source tool for data exploration and visualization. [Learn more](https://superset.apache.org/).
- **Tableau Cloud/Desktop**: A leading visualization tool with cloud and desktop versions. [Cloud](https://www.tableau.com/cloud) | [Desktop](https://www.tableau.com/).
- **Power BI**: Microsoft's business analytics service. [Learn more](https://powerbi.microsoft.com/).
- **Metabase**: An open-source business intelligence tool. [Learn more](https://www.metabase.com/).
- **Google Data Studio**: A free tool from Google for creating dashboards and reports. [Learn more](https://datastudio.google.com/).
- **Excel through Devart plugin**: Connect Excel to various databases, including PostgreSQL. [Learn more](https://www.devart.com/excel-addins/).
- **Deepnote**: A collaborative notebook for data science. [Learn more](https://deepnote.com/).
- **Hex**: A project-based notebook for teams. [Learn more](https://hex.pm/).
- **Observable**: Create, collaborate, and share data visualizations. [Learn more](https://observablehq.com/).
- **Streamlit**: Turn data scripts into shareable web apps. [Learn more](https://streamlit.io/).
- **Jupyter notebook**: An open-source web application for creating and sharing documents with live code. [Learn more](https://jupyter.org/).
- **Hightouch**: Sync data between your warehouse and business apps. [Learn more](https://hightouch.io/).

Each of these clients provides unique features and capabilities, making them suitable for different data management and analysis needs. Consider your specific requirements and preferences when choosing the right tool for connecting to Synmetrix.