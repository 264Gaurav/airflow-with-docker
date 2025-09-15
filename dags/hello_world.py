from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define the DAG
with DAG(
    dag_id="hello_world",
    start_date=datetime(2025, 9, 1),
    schedule=None,   # <-- correct for Airflow 3.x
    catchup=False,
    tags=["example"],
) as dag:

    # Task 1: print system date
    print_date = BashOperator(
        task_id="print_date",
        bash_command="date"
    )

    # Task 2: say hello
    say_hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow!'"
    )

    # Define task order: first print_date, then say_hello
    print_date >> say_hello
