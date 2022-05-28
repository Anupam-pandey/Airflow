from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from datetime import datetime



# from subdags.subdag_parallel_dag import subdag_parallel_dag
from airflow.utils.task_group import TaskGroup 

default_args = {
'start_date' : datetime(2020,1,1)
}


with DAG('trigger_rule', default_args=default_args,catchup=False,schedule_interval='@daily') as dag:
    
    task_1 = BashOperator(task_id='task_1', bash_command='exit 1', do_xcom_push=False)

    task_2 = BashOperator(task_id='task_2', bash_command='exit 1', do_xcom_push=False)

    task_3 = BashOperator(task_id='task_3', bash_command='exit 0', do_xcom_push=False, trigger_rule="all_failed")

    [task_1 , task_2] >> task_3

