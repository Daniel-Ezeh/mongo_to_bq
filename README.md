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