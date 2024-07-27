from airflow import DAG
from datetime import timedelta, datetime 
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import json 
import pandas as pd


#setup arguments for the DAG
default_args = {
    'owner': 'weather_airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 27), #year-month-day
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

#convert kelvin_to_fahrenheit
def k_2_f(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit

def transform_and_load(task_instance): #the task_instance is the previous tasks that we will use in this function i.e extract
  data = task_instance.xcom_pull(task_ids = "extract_data")
  city = data["name"]
  weather_description = data["weather"][0]['description']
  temp_farenheit = k_2_f(data["main"]["temp"])
  feels_like_farenheit= k_2_f(data["main"]["feels_like"])
  min_temp_farenheit = k_2_f(data["main"]["temp_min"])
  max_temp_farenheit = k_2_f(data["main"]["temp_max"])
  pressure = data["main"]["pressure"]
  humidity = data["main"]["humidity"]
  wind_speed = data["wind"]["speed"]
  time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
  sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
  sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

  transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_farenheit,
                        "Feels Like (F)": feels_like_farenheit,
                        "Minimun Temp (F)":min_temp_farenheit,
                        "Maximum Temp (F)": max_temp_farenheit,
                        "Pressure": pressure,
                        "Humidty": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)":sunrise_time,
                        "Sunset (Local Time)": sunset_time                        
                        }
  
  transformed_data_list = [transformed_data]
  df_data = pd.DataFrame(transformed_data_list)


  #get your credentials from AWS
  aws_credentials = {"key": <key>, "secret": <secert_key>}

  #to have a unique file_name for each extracted data
  now = datetime.now()
  dt_string = now.strftime("%d%m%Y%H%M%S")
  dt_string = 'current_weather_data_linköping_' + dt_string

  #To save it to the s3 bucket, template: s3://<your_s3_bucket_name>/
  df_data.to_csv(f"s3://<your_s3_bucket_name>/{dt_string}.csv", index=False, storage_options=aws_credentials)



# We will set all the tasks inside this
with DAG("weather_dag",
  default_args = default_args,
  schedule_interval = "@daily",
  catchup = False) as dag: 

  #Checking if pinging to the API works
  weather_api_check = HttpSensor(
    task_id ="weather_api_check", #should be unique 
    http_conn_id = "weather_api",  #Airflow connection to https://api.openweathermap.org
    endpoint = "/data/2.5/weather?q=Linköping&appid=9876a360d8b8be2e969221da0719b3fa"
    # doc: https://openweathermap.org/current
  )

  #Extracting the data 
  extract_data = SimpleHttpOperator(
    task_id = "extract_data",
    http_conn_id = "weather_api",  #Airflow connection to https://api.openweathermap.org
    endpoint = "/data/2.5/weather?q=Linköping&appid=9876a360d8b8be2e969221da0719b3fa",
    method = "GET",
    response_filter = lambda r: json.loads(r.text),
    log_response = True
  )

  #transforming the data and the laoding it into AWS S3
  transform_load = PythonOperator(
    task_id = "transform_load",
    python_callable = transform_and_load #the function to run
  )




  weather_api_check >> extract_data >> transform_load


