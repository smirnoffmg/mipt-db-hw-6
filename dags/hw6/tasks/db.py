import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

from hw6.config import DATA_DIR, POSTGRES_CONN_ID, SQL_DIR, TABLES


def create_tables():
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    sql = (SQL_DIR / "schema.sql").read_text()
    hook.run(sql)


def load_table(table_name: str):
    cfg = TABLES[table_name]
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    df = pd.read_csv(
        DATA_DIR / cfg["file"],
        sep=cfg.get("sep", ","),
        na_values=["", "n/a", "N/A"],
    )
    df.columns = [c.lower() for c in df.columns]

    for col in cfg.get("date_columns", []):
        df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in cfg.get("bool_columns", []):
        df[col] = df[col].map({"True": True, "False": False, True: True, False: False})

    conn = hook.get_conn()
    cur = conn.cursor()

    columns = cfg["columns"]
    placeholders = ", ".join(["%s"] * len(columns))
    cols_str = ", ".join(columns)

    pk = cfg.get("primary_key")
    conflict = f" ON CONFLICT ({pk}) DO NOTHING" if pk else ""

    insert_sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders}){conflict}"

    for _, row in df.iterrows():
        values = tuple(None if pd.isna(row[col]) else row[col] for col in columns)
        cur.execute(insert_sql, values)

    conn.commit()
    cur.close()
