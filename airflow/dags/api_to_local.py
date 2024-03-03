from datetime import datetime
import requests
import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def extract_from_api_and_save_local():
    api_url = 'https://random-data-api.com/api/v2/users'
    response = requests.get(api_url)
    data = response.json()
    with open('/tmp/dados.json', 'w') as f:
        json.dump(data, f)

dag_api_to_local = DAG(
    'api_to_local',
    description='Consulta uma API e salva os dados localmente',
    schedule_interval='@daily',
    start_date=datetime(2024, 2, 17),
    catchup=False
)

extract_and_save_task = PythonOperator(
    task_id='extract_and_save',
    python_callable=extract_from_api_and_save_local,
    dag=dag_api_to_local
)
