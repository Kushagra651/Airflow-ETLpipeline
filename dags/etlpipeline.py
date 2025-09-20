from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta  # ✅ Fixed import
import json


## Define the DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=datetime(2025, 1, 1),  # ✅ Fixed: Use datetime instead of days_ago
    schedule='@daily',
    catchup=False

) as dag:
    
    ## step 1: Create the table if it doesnt exists
    @task
    def create_table():
        ## initialize the Postgreshook
        postgres_hook=PostgresHook(postgres_conn_id="postgres_localhost")  # ✅ Updated connection name

        ## SQL query to create the table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        ## Execute the table creation query
        postgres_hook.run(create_table_query)


    ## Step 2: Extract the NASA API Data(APOD)-Astronomy Picture of the Day[Extract pipeline]
    extract_apod=SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_apod',  # ✅ Updated connection name
        endpoint='planetary/apod', 
        method='GET',
        data={"api_key":"{{ conn.nasa_apod.extra_dejson.api_key}}"}, # ✅ Updated connection reference
        response_filter=lambda response:response.json(),
    )

    ## Step 3: Transform the data(Pick the information that i need to save)
    @task
    def transform_apod_data(response):
        apod_data={
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }
        return apod_data


    ## step 4:  Load the data into Postgres SQL
    @task
    def load_data_to_postgres(apod_data):
        ## Initialize the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id='postgres_localhost')  # ✅ Updated connection name

        ## Define the SQL Insert Query
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """

        ## Execute the SQL Query
        postgres_hook.run(insert_query,parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))


    ## step 6: Define the task dependencies ✅ Fixed
    # Create tasks
    table_task = create_table()
    
    # Get transformed data
    api_response = extract_apod.output
    transformed_data = transform_apod_data(api_response)
    
    # Set dependencies
    table_task >> extract_apod >> transformed_data >> load_data_to_postgres(transformed_data)