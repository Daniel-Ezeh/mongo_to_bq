# mongo_to_bq


Python version: Python 3.10.11

pyenv global 3.10.11
Then check using "python3 --version"


* If having trouble with resetting the python version, use

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
source ~/.bashrc 
pyenv rehash


* Then create a virtual environment using:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


* Then Start up Airflow:

export AIRFLOW_HOME="$(pwd)"
airflow db reset
airflow db init
airflow standalone


export AIRFLOW_HOME="$(pwd)"
airflow db init
airflow webserver -D --port 8080
airflow scheduler


BUILDING THE IMAGE

ENABLE CLOUD BUILD API AND CLOUD RUN API
gcloud services enable cloudbuild.googleapis.com run.googleapis.com


BUILD YOUR IMAGE
gcloud builds submit --tag gcr.io/[PROJECT_ID]/[IMAGE_NAME]


docker build -t your_image_name .
docker run --env-file .env -p 8000:8000 your_image_name


TO SIGN IN AND SET UP GOOGLE ACCOUNT
gcloud auth list
gcloud config set account `ACCOUNT`
gcloud auth login
gcloud projects list
gcloud auth application-default login
gcloud config set project [PROJECT_ID]



