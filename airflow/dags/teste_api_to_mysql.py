from datetime import datetime
import requests
from airflow import DAG
from airflow.models import Connection
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.models import Variable
from sqlalchemy import create_engine
import pandas as pd
from airflow.hooks.base_hook import BaseHook
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.hooks.mysql_hook import MySqlHook

# Defina os parâmetros da API
API_URL = 'https://random-data-api.com/api/v2/users?size=100&is_xml=true'
#cnn = Connection.get_connection_from_secrets()

mysql_hook = MySqlHook(mysql_conn_id='mysql_teste')

def extract_data():
    response = requests.get(API_URL)
    data = response.json()
    print('******')
    print(mysql_hook)
    return data

def save_to_mysql(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='extract_data')
    # Aqui você pode salvar os dados em uma base de dados MySQL
    # Este é apenas um exemplo para demonstração
    engine = connection = create_engine(conn.get_extra())
    df = pd.json_normalize(data)
    df.to_sql(MYSQL_TABLE_NAME, con=engine, if_exists='append', index=False)
    # Você pode usar o MySqlOperator para salvar os dados em uma tabela MySQL


# Defina o nome do seu DAG e os argumentos padrão
dag = DAG(
    'api_teste',
    description='Exemplo de captura de dados de uma API e salvamento em MySQL com XCom',
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

save_task = PythonOperator(
    task_id='save_to_mysql',
    python_callable=save_to_mysql,
    provide_context=True,
    dag=dag
)

# Defina a ordem das tarefas
extract_task >> save_task