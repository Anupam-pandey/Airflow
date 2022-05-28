from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from datetime import datetime


# from subdags.subdag_parallel_dag import subdag_parallel_dag
from airflow.utils.task_group import TaskGroup 

default_args = {
'start_date' : datetime(2020,1,1)
}


with DAG('parallel_dag', default_args=default_args,catchup=False,schedule_interval='@daily') as dag:
    
    task_1 = BashOperator(task_id='task_1', bash_command='sleep 3')

    # processing = SubDagOperator(task_id="processing_task",subdag=subdag_parallel_dag("parallel_dag","processing_task",default_args=default_args) )


    with TaskGroup('processing') as tg:
        task_2 = BashOperator(task_id='task_2', bash_command='sleep 3')
        task_3 = BashOperator(task_id='task_3', bash_command='sleep 3')
    
    task_4 = BashOperator(task_id='task_4', bash_command='sleep 3')

    task_1 >> tg >>task_4 


