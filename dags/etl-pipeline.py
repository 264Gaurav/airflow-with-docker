from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# --- Step functions ---

def extract_data(**context):
    # Simulated extract: produce a list of records
    data = ["user1,100", "user2,200", "user3,300"]
    context['ti'].xcom_push(key="raw_data", value=data)

def transform_data(**context):
    # Simulated transform: parse and uppercase usernames
    raw_data = context['ti'].xcom_pull(key="raw_data", task_ids="extract")
    transformed = []
    for record in raw_data:
        user, amount = record.split(",")
        transformed.append({"user": user.upper(), "amount": int(amount)})
    context['ti'].xcom_push(key="transformed_data", value=transformed)

def load_data(**context):
    # Simulated load: print to logs (replace with DB/API write)
    transformed = context['ti'].xcom_pull(key="transformed_data", task_ids="transform")
    print("### Loading data ###")
    for row in transformed:
        print(row)

# --- DAG definition ---
with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2025, 9, 1),
    #schedule=None,    # run manually for now
    #schedule="*/5 * * * *",   # every 5 minutes
    schedule=timedelta(minutes=50),   # every 5 minutes
    catchup=False,
    tags=["etl", "example"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_data,
    )

    # Define flow: Extract → Transform → Load
    extract >> transform >> load
