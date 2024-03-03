from datetime import datetime
import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.empty import EmptyOperator

def load_from_local_to_mysql():
    with open('./caminho/para/o/arquivo/dados.json', 'r') as f:
        data = json.load(f)
    
    mysql_hook = MySqlHook(mysql_conn_id='mysql_teste')
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    
    for item in data:
        cursor.execute("INSERT INTO sua_tabela (campo1, campo2, campo3) VALUES (%s, %s, %s)", (item['campo1'], item['campo2'], item['campo3']))
    
    connection.commit()
    cursor.close()

dag_local_to_mysql =  DAG(
    'local_to_mysql',
    description='Carrega os dados locais para o MySQL',
    schedule_interval='@daily',
    start_date=datetime(2024, 2, 17),
    catchup=True
) 

load_to_mysql_task = PythonOperator(
    task_id='load_to_mysql',
    python_callable=load_from_local_to_mysql,
    dag=dag_local_to_mysql
)

fim = EmptyOperator(task_id="fim")

# Define a relação de dependência entre as duas DAGs
#external_task_sensor >> dag_local_to_mysql >> fim
