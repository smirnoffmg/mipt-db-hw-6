from datetime import datetime
from functools import partial

from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from hw6.config import DEFAULT_ARGS, QUERIES, TABLES
from hw6.tasks.db import create_tables, load_table
from hw6.tasks.queries import check_results, run_query


def log_success():
    print("DAG выполнен успешно! Все запросы вернули данные.")


def log_failure():
    print("DAG выполнен с ошибками! Один или несколько запросов вернули 0 строк.")


with DAG(
    dag_id="hw6_etl_pipeline",
    default_args=DEFAULT_ARGS,
    description="ETL pipeline for loading customer/product/orders data and running analytics",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["hw6", "etl"],
) as dag:

    start = EmptyOperator(task_id="start")

    create_tables_task = PythonOperator(
        task_id="create_tables",
        python_callable=create_tables,
    )

    load_tasks = [
        PythonOperator(
            task_id=f"load_{table}",
            python_callable=partial(load_table, table),
        )
        for table in TABLES
    ]

    data_loaded = EmptyOperator(task_id="data_loaded")

    query_tasks = [
        PythonOperator(
            task_id=f"query_{name}",
            python_callable=partial(run_query, name),
        )
        for name in QUERIES
    ]

    queries_done = EmptyOperator(task_id="queries_done")

    check_results_task = BranchPythonOperator(
        task_id="check_results",
        python_callable=partial(check_results, [f"query_{name}" for name in QUERIES]),
    )

    send_failure_email = EmailOperator(
        task_id="send_failure_email",
        to="admin@example.com",
        subject="HW6 DAG Alert: Query returned zero rows",
        html_content="<p>One or more queries returned zero rows. Please investigate.</p>",
    )

    log_success_task = PythonOperator(
        task_id="log_success", python_callable=log_success
    )
    log_failure_task = PythonOperator(
        task_id="log_failure", python_callable=log_failure, trigger_rule="all_done"
    )

    end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

    (
        start
        >> create_tables_task
        >> load_tasks
        >> data_loaded
        >> query_tasks
        >> queries_done
        >> check_results_task
    )
    check_results_task >> log_success_task >> end
    check_results_task >> send_failure_email >> log_failure_task >> end
