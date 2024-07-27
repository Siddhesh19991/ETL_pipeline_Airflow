<img width="1645" alt="Screenshot 2024-07-27 at 8 31 17 PM" src="https://github.com/user-attachments/assets/055c480b-1770-4596-93ec-e70104e264cf"># ETL_pipeline_Airflow

In this project we are setting up an ETL pipeline to collect weather data for linköping city in Sweden and automating this flow using Apache Airflow. We will be using "OpenWeather" API to get the data. So the overall ETL strutucve that will be built is shown in the diagram below: 

<img width="744" alt="Screenshot 2024-07-27 at 8 44 47 PM" src="https://github.com/user-attachments/assets/0e01909a-22a5-4b79-ab37-fa4d4cf294a7">



Steps: 
1 Creating an EC2 instance using Amazon AWS. 
2 After we create the instance, we need to edit the inbound rule for this instance to allow access to the Airflow UI through Port 8080. 


We need to now install some dependancies since there will be nothing installed in this machine. I will need to install everything 

```python
sudo apt update 
sudo apt install python3-pip
sudo apt install python3.12-venv
```

Now we create a virtual environment

```python
python3 -m venv airflow_venv
source airflow_venv/bin/activate

```

Install packages
```python
pip3 install pandas
pip3 install s3fs #needed to connect to our S3 bucket 
pip3 install apache_airflow
```

We acess airflow UI to visually see the DAG process. This is where the point 2 mentioned above comes into play i.e 2 After we create the instance, we need to edit the inbound rule for this instance to allow access to the Airflow UI through Port 8080. 
:
```python
airflow standalone 
```
We then connect the EC2 instance to VS studio for ease of development and to create the DAG workflow 


### DAG workflow 

We have setup 3 tasks with each depdent on the previous task so the second task will only run if the first task succeeds and so on. We have set up the DAG arguments as the followiing: 

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
So it runs daily to get the data. 

The tasks are as follows: 
1) API check
2) Extact data from the API
3) Tranfsomr the data into the desicer format and the load it to S3 stogare for fuether use i,e data analysis, dashboard, machine learing etc.

Note: to get a better understanding as to how to do the transformations, I entered the API link into the browser to see how the output looks like and it looks like this: 
<img width="1588" alt="Screenshot 2024-07-27 at 8 33 09 PM" src="https://github.com/user-attachments/assets/673dbd19-9691-49f9-bdf0-91973b26ea61">


Finally, once everytin is setup, we can go to the apackge airflow UI and run the DAG. We can 
<img width="844" alt="Screenshot 2024-07-27 at 8 34 14 PM" src="https://github.com/user-attachments/assets/574bed2e-5c7c-43aa-853b-7c8702dcd812">



