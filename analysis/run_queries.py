import os
from pathlib import Path

import duckdb


def main():
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    sql_path = project_root / "analysis" / "queries.sql"

    # Read and separate SQL statements
    sql = sql_path.read_text(encoding="utf-8")
    statements = duckdb.extract_statements(sql)

    # Execute each query
    with duckdb.connect() as con:
        con.execute("SET SESSION TimeZone = 'UTC'")

        for i, statement in enumerate(statements, start=1):
            result = con.execute(statement.query).df()

            print(f"\n--- Query {i} ---")
            print(result.to_string(index=False))


if __name__ == "__main__":
    main()
