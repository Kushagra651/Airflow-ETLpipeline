<h1>Apache Airflow</h1>

<br>
Airflow is an orchestration toll which helps us build etl(extract,transform,load) pipelines easily and  helps run them
eg-> in big comanies data comes in huge chunks everyday they can train the models daily manually that takes a lot of  man power and its time ineffecient so instead   what they do is they create a etl piepline in which the data from their databases are extracted which is the first step of the etl pipeline and then  apply necessary tansformations to it and then load it to the necessary location as needed it can we easily automated which saves a lot of time 
q-> why cant we simply use github actions instead of airlfow and etl pipelines 
actions is a good tool for test and deplo the new code or feature but it doesnt work for the data and how its transformed and airflow is necessarily an etl  tool

 what is a DAG-?
DAG  stands for direct acyclic graph and these are a collection of well defined task which need to performed in a cretain order as the name suggest directed and also its acyclic in nature means you can go back to the  previous task  making a cycle 

tasks->
there are indiviudal unit of work which are specified clear;y inside a dag using various python functions 

dependencies ->
each task need to have certain specs like  cant start another task before the completion of the previous task to you can set up certain dependencies manually to schedule them in certain way and manipu;ate there working 

 what is orchestration


 steps to create a DAG

 1-> Think about the pipeline and all its need and understand  what it must do

 Extract → Transform → Load

 2-> create a pythoin file to write the dag to it (pileine_dag.py) and import all the required library like datetime and pythonoperator

 3->set dag defaults like (owner,retries etc)

 3-> define the dag  write its uniqu id,catchup,schedule_interval,
 eg-> with DAG(
    dag_id="my_simple_etl",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:


4-> write each task which need be performed as a python function
def extract_data():
def transform_data():
def load_data():

5->convert these functions into tasks

extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract,
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform,
)

load_task = PythonOperator(
    task_id="load",
    python_callable=load,
)


6-> set task order 
extract_task >> transform_task >> load_task

sample  DAG

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("Extracting data...")

def transform():
    print("Transforming data...")

def load():
    print("Loading data...")

with DAG(
    dag_id="simple_etl_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Simple ETL DAG Example"
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load
    )

    extract_task >> transform_task >> load_task


 
 

