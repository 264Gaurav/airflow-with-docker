from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG('hello_world', start_date=datetime(2025,9,1), schedule_interval=None, catchup=False) as dag:
    t1 = BashOperator(task_id='print_date', bash_command='date')
