The initial schema migration is `versions/0001_initial_schema.py`.

From the project root, activate the backend environment and run:

```bash
source .venv/bin/activate
alembic upgrade head
```

To inspect the SQL without connecting to PostgreSQL:

```bash
alembic upgrade head --sql
```

To remove the initial schema:

```bash
alembic downgrade base
```
