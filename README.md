# ETL_pipeline_Airflow

This project sets up an ETL (Extract, Transform, Load) pipeline to collect weather data for Linköping City in Sweden using the [OpenWeather API](https://openweathermap.org/). The pipeline is automated with Apache Airflow and hosted on an Amazon EC2 instance. Below are the steps to set up the environment, install dependencies, and configure the ETL pipeline. 

<img width="744" alt="Screenshot 2024-07-27 at 8 44 47 PM" src="https://github.com/user-attachments/assets/0e01909a-22a5-4b79-ab37-fa4d4cf294a7">

### Setting Up the EC2 Instance and Installing Dependencies
1. Start by launching an EC2 instance using Amazon AWS.
2. Once the EC2 instance is running, SSH into the instance and execute the following commands to set up the environment: 
```python
sudo apt update 
sudo apt install python3-pip
sudo apt install python3.12-venv
```

### Create a virtual environment and Install Required Packages
```python
python3 -m venv airflow_venv
source airflow_venv/bin/activate

```
```python
pip3 install pandas
pip3 install s3fs #needed to connect to our S3 bucket 
pip3 install apache_airflow
```

To start Airflow, execute:
```python
airflow standalone 
```

We then connect the EC2 instance to Visual Studio Code for development and create the DAG (Directed Acyclic Graph) workflow.

### DAG workflow 

Configure the DAG with the following arguments to run the workflow daily:
```python
default_args = {
    'owner': 'weather_airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 27), #year-month-day
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
      schedule_interval = "@daily"
}
```

The ETL pipeline includes the following tasks:

1. API Check: Verify API connectivity and response.
2. Extract Data: Retrieve data from the OpenWeather API.
3. Transform and Load: Transform the data into the desired format and load it into an S3 bucket for further analysis, dashboard creation, or machine learning.


Note: To get a better understanding of how to transform the data, I entered the API link into the browser to see what the response looks like: 
<img width="1588" alt="Screenshot 2024-07-27 at 8 33 09 PM" src="https://github.com/user-attachments/assets/673dbd19-9691-49f9-bdf0-91973b26ea61">


Once everything is set up, you can access the Airflow UI and manually run the DAG from the dashboard:

<img width="844" alt="Screenshot 2024-07-27 at 8 34 14 PM" src="https://github.com/user-attachments/assets/574bed2e-5c7c-43aa-853b-7c8702dcd812">



