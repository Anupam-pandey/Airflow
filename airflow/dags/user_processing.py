from urllib import response
from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import json
import pandas as pd

default_arg  = {
'start_date' : datetime(2020,1,1)
}


def _process_user(ti):
    user = ti.xcom_pull(task_ids=['extract_user'])
    if not user or not user[0]:
        raise ValueError("value nhi h")
    users = user[0]['results'][0]
    user_data = {
        'firstname': users['name']['first'],
        'lastname': users['name']['last'],
        'email' : users['email']
    }
    user_data = pd.json_normalize(user_data)
    user_data.to_csv('/tmp/process_user.csv',index=None,header=False)



with DAG('user_processing',schedule_interval='@daily',default_args=default_arg,catchup=False) as dag:

    
    create_table = SqliteOperator(task_id = "create_table", sqlite_conn_id='db_sqlite',sql=
    '''
        CREATE TABLE IF NOT EXISTS users(firstname TEXT,lastname TEXT,email TEXT NOT NULL PRIMARY KEY);
    ''')

    is_api_available = HttpSensor(task_id="is_api_available", http_conn_id='user_api',endpoint='api/')

    extract_user = SimpleHttpOperator(task_id="extract_user", http_conn_id='user_api',endpoint='api/',
                   response_filter = lambda response: json.loads(response.text),method='GET',log_response=True)

    # print(extract_user)

    process_user = PythonOperator(task_id="process_user",python_callable=_process_user)

    store_user = BashOperator(task_id="store_user", bash_command='echo -e ".separator "," \n.import /tmp/process_user.csv users"| sqlite3 /home/anupam/airflow/airflow.db')

    create_table >> is_api_available >> extract_user >> process_user >> store_user


