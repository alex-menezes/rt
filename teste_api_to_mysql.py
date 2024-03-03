from datetime import datetime
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd

# Defina os parâmetros da API
API_URL = 'https://www.boredapi.com/api/activity'

# Defina os parâmetros do banco de dados MySQL
MYSQL_CONN_ID = 'mysql_default'
MYSQL_TABLE_NAME = 'atividade'
MYSQL_SCHEMA = 'dw'

def extract_data():
    response = requests.get(API_URL)
    data = response.json()
    return data

def transform_data(data):
    # Aqui você pode fazer qualquer transformação necessária nos dados
    return data

def load_data_to_mysql(data):
    engine = create_engine(f'mysql://{MYSQL_CONN_ID}')
    df = pd.DataFrame(data)
    df.to_sql(MYSQL_TABLE_NAME, con=engine, schema=MYSQL_SCHEMA, if_exists='append', index=False)

# Defina o nome do seu DAG e os argumentos padrão
dag = DAG(
    'api_to_mysql',
    description='Exemplo de DAG para extrair dados de uma API e carregar no MySQL',
    schedule_interval='@daily',
    start_date=datetime(2024, 2, 17),
    catchup=False
)

# Defina as tarefas do DAG
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data_to_mysql',
    python_callable=load_data_to_mysql,
    provide_context=True,
    dag=dag
)

# Defina a ordem das tarefas
extract_task >> transform_task >> load_task