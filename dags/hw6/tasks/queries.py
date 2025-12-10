from airflow.providers.postgres.hooks.postgres import PostgresHook

from hw6.config import OUTPUT_DIR, POSTGRES_CONN_ID, QUERIES, SQL_DIR


def run_query(query_name: str, **context):
    cfg = QUERIES[query_name]
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    sql = (SQL_DIR / cfg["file"]).read_text()
    df = hook.get_pandas_df(sql)

    output_file = OUTPUT_DIR / cfg["output"]
    df.to_csv(output_file, index=False)

    context["ti"].xcom_push(key="row_count", value=len(df))
    return len(df)


def check_results(task_ids: list[str], **context):
    ti = context["ti"]

    for task_id in task_ids:
        count = ti.xcom_pull(task_ids=task_id, key="row_count")
        if count == 0:
            return "send_failure_email"

    return "log_success"
