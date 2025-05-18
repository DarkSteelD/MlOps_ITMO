from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import weather

default_args = {
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="weather_pipeline",
    default_args=default_args,
    schedule_interval="* * * * *",
    catchup=False,
) as dag:
    fetch_weather_task = PythonOperator(
        task_id="fetch_weather",
        python_callable=weather.write_weather_to_csv,
    )

    fetch_weather_task 