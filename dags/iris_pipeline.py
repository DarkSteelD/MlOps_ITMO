from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import data
import train
import test

default_args = {
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    dag_id="iris_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    load_data_task = PythonOperator(
        task_id="load_data",
        python_callable=data.load_data,
    )

    prepare_data_task = PythonOperator(
        task_id="prepare_data",
        python_callable=data.prepare_data,
    )

    train_model_task = PythonOperator(
        task_id="train_model",
        python_callable=train.train_model,
    )

    test_model_task = PythonOperator(
        task_id="test_model",
        python_callable=test.test_model,
    )

    load_data_task >> prepare_data_task >> train_model_task >> test_model_task 