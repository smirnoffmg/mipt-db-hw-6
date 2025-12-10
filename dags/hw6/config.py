from datetime import timedelta
from pathlib import Path

POSTGRES_CONN_ID = "postgres_default"
DATA_DIR = Path("/opt/airflow/data")
OUTPUT_DIR = Path("/opt/airflow/output")
SQL_DIR = Path(__file__).parent / "sql"

DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

TABLES = {
    "customer": {
        "file": "customer.csv",
        "sep": ";",
        "columns": [
            "customer_id",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "job_title",
            "job_industry_category",
            "wealth_segment",
            "deceased_indicator",
            "owns_car",
            "address",
            "postcode",
            "state",
            "country",
            "property_valuation",
        ],
        "date_columns": ["dob"],
        "primary_key": "customer_id",
    },
    "product": {
        "file": "product.csv",
        "sep": ",",
        "columns": [
            "product_id",
            "brand",
            "product_line",
            "product_class",
            "product_size",
            "list_price",
            "standard_cost",
        ],
    },
    "orders": {
        "file": "orders.csv",
        "sep": ",",
        "columns": [
            "order_id",
            "customer_id",
            "order_date",
            "online_order",
            "order_status",
        ],
        "date_columns": ["order_date"],
        "bool_columns": ["online_order"],
        "primary_key": "order_id",
    },
    "order_items": {
        "file": "order_items.csv",
        "sep": ",",
        "columns": [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "item_list_price_at_sale",
            "item_standard_cost_at_sale",
        ],
        "primary_key": "order_item_id",
    },
}

QUERIES = {
    "top3_minmax": {"file": "top3_minmax.sql", "output": "top3_minmax.csv"},
    "top5_segment": {"file": "top5_segment.sql", "output": "top5_by_segment.csv"},
}
