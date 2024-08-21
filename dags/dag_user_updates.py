from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
import logging
import os
import random
from pprint import pprint
import json
from dotenv import load_dotenv


load_dotenv()
# Define the default arguments
PAYMENT_METHOD=['web','pos','app','cashout']
PRODUCT_PURCHASED=['topup','data','dstv','phcn','airtime']
MONGODB_URI = os.environ['MONGODB_URI']
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 15),
    'retries': 1,
    'retry_delay': timedelta(seconds=15),
}

uri = f"{MONGODB_URI}?retryWrites=true&w=majority&appName=mongo-to-bq"
client = MongoClient(uri)
myCollection = client['customers']['wallet_transactions']


logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log format
    handlers=[logging.StreamHandler()]  # Output logs to the console
)


def get_random_document_id(**kwargs):
    pipeline = [
        {"$sample": {"size": 3}}  # Randomly select 2 document
    ]
    id_list = []
    random_doc = myCollection.aggregate(pipeline)
    for doc in random_doc:
        docf = json.dumps(str(doc["uid"]))
        id_list.append(docf.strip('"'))
    kwargs['ti'].xcom_push(key='uid', value=id_list)
    logging.info(id_list)
    return id_list



def update_document(x, **kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='sampling_various_uids', key='uid')
    # uid = str(json.dumps(str(data[0])).replace('"',''))
    uid = str(data[x]).replace('"','')
    update_operation = {
        "$set": {
            "timeUpdated": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z'),
            "amount": (100 + round((random.random()*500),2)),
            "paymentMethod": random.choice(PAYMENT_METHOD),
            "product": random.choice(PRODUCT_PURCHASED)
        }
    }
    result = myCollection.find_one_and_update(
        filter={"uid":uid},
        update = update_operation, 
        return_document=True,
        upsert=True
        )
    if result:
        print(f"Document {uid} updated successfully")
        aa = myCollection.find_one(uid)
        print(json.dumps(str(aa)))
        logging.info(aa)
    else:
        print("No document found or no changes made")


# The Main flow of the DAG

with DAG(
    'dag_generate_updates',
    default_args=default_args,
    description='DAG for generating random user and moving to Mongo Atlas',
    catchup=False,
    schedule=timedelta(minutes=2),
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    sampling_documents = PythonOperator(
        task_id='sampling_various_uids',
        python_callable=get_random_document_id,
        provide_context=True,
        dag=dag,
    )

    end = EmptyOperator(
        task_id="end"
    )



with TaskGroup("group_1", dag=dag) as first_doc:
    delay_task = TimeDeltaSensor(
        task_id='wait_for_some_seconds',
        delta=timedelta(seconds=random.randint(5,30))
    )
    generate_update_1 = PythonOperator(
        task_id='Pushing_update_to_doc1',
        provide_context=True,
        python_callable=update_document,
        op_kwargs={'x': 0},
        dag=dag,
    )
    delay_task >> generate_update_1



with TaskGroup("group_2", dag=dag) as second_doc:
    delay_task = TimeDeltaSensor(
        task_id='wait_for_some_seconds',
        delta=timedelta(seconds=random.randint(5,30))
    )
    generate_update_2 = PythonOperator(
        task_id='Pushing_update_to_doc2',
        provide_context=True,
        python_callable=update_document,
        op_kwargs={'x': 1},
        dag=dag,
    )
    delay_task << generate_update_2



with TaskGroup("group_3", dag=dag) as third_doc:
    delay_task = TimeDeltaSensor(
        task_id='wait_for_some_seconds',
        delta=timedelta(seconds=random.randint(5,15))
    )
    generate_update_3 = PythonOperator(
        task_id='Pushing_update_to_doc3',
        provide_context=True,
        python_callable=update_document,
        op_kwargs={'x': 2},
        dag=dag,
    )
    delay_task >> generate_update_3







# Set the task in the DAG
start\
>> sampling_documents\
>> [
    first_doc, 
    second_doc, 
    third_doc
    ]\
>> end