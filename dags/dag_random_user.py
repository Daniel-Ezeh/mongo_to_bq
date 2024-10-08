from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import sys
import time
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random_user_gen as ru


load_dotenv()
# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 15),
    'retries': 2,
    'retry_delay': timedelta(seconds=15),
}

def insert_doc():
    max_retries=5
    base_delay=1
    multiplier=2
    MONGODB_URI = os.environ['MONGODB_URI']
    retries = 0
    while retries < max_retries:
        try:
            uri = f"{MONGODB_URI}?retryWrites=true&w=majority&appName=mongo-to-bq"
            client = MongoClient(uri)
            myCollection = client['customers']['wallet_transactions']
            customer = ru.get_random_user()
            myCollection.insert_one(customer)
        except Exception as e:
            print(f"Error: {e}")
            retries += 1
            delay = base_delay * (multiplier ** (retries - 1))
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    raise ConnectionError(f"Failed to connect to MongoDB after {max_retries} retries")

    

# Define the DAG
with DAG(
    'Random_api_to_mongo',
    default_args=default_args,
    description='DAG for generating random user and moving to Mongo Atlas',
    catchup=False,
    schedule=timedelta(minutes=5),
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    transfer_to_mongo_collection = PythonOperator(
        task_id='transfer_to_mongo_collection',
        python_callable=insert_doc,
        dag=dag,
    )

    end = EmptyOperator(
        task_id="end"
    )

# Set the task in the DAG
start\
>> transfer_to_mongo_collection\
>> end