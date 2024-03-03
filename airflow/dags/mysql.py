from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook

# Defina os parâmetros da sua DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 17),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

# Define a função que será executada pela PythonOperator
def execute_query(mysql_conn_id, **kwargs):
    # Crie um objeto MySqlHook para acessar a conexão MySQL
    mysql_hook = MySqlHook(mysql_conn_id='mysql_teste')
    # Defina a sua consulta SQL
    sql_query = "SELECT * FROM user"
    # Execute a consulta e obtenha os resultados
    results = mysql_hook.get_records(sql_query)
    # Faça o que quiser com os resultados
    for row in results:
        print(row)

# Defina o nome do seu DAG e os argumentos padrão
dag = DAG(
    'mysql_query_with_python_operator',
    description='Exemplo de DAG para executar consulta MySQL com PythonOperator',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False
)

# Defina a tarefa do DAG usando PythonOperator
execute_query_task = PythonOperator(
    task_id='execute_query',
    python_callable=execute_query,
    op_args=['mysql_default'],  # Passa o mysql_conn_id como argumento
    provide_context=True,
    dag=dag
)

# A tarefa de execução da consulta MySQL depende de outra tarefa?
# Se sim, defina a ordem das tarefas.
# execute_query_task >> outra_tarefa

