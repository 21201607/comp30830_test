import pymysql 
import traceback
import requests
import time
from datetime import datetime
import json

weather_apiKey = "1b2d168422195fdadf28f15d5f1dba4e"
city_name = 'Dublin,ie'
parameters = {"q" : city_name, "appid" : weather_apiKey} 
weather_URL = "http://api.openweathermap.org/data/2.5/weather"

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS weather_Dublin_test(
        Clouds INTEGER,
        feels_like DOUBLE,
        humidity INTEGER,
        pressure INTEGER,
        temp DOUBLE,
        temp_max DOUBLE,
        temp_min DOUBLE,
        sunrise VARCHAR(255),
        sunset VARCHAR(255),
        visibility INTEGER,
        weather_description VARCHAR(255),
        weather_main VARCHAR(255),
        wind_deg INTEGER,
        wind_speed DOUBLE,
        dt VARCHAR(255)
    );
    """
        
    try:
        res = cursor.execute(sql)
        print('create ok')
    except Exception as e:
        print(e)
        

def write_to_db(text):
    weather_data = json.loads(text)
    
    weather_vals = (
        str(weather_data['clouds']['all']),
        str(weather_data['main']['feels_like']),
        str(weather_data['main']['humidity']),
        str(weather_data['main']['pressure']),
        str(weather_data['main']['temp']),
        str(weather_data['main']['temp_max']),
        str(weather_data['main']['temp_min']),
        str(datetime.fromtimestamp(weather_data['sys']['sunrise'])),
        str(datetime.fromtimestamp(weather_data['sys']['sunset'])),
        str(weather_data['visibility']),
        str(weather_data['weather'][0]['description']),
        str(weather_data['weather'][0]['main']),
        str(weather_data['wind']['deg']),
        str(weather_data['wind']['speed']),
        str(datetime.fromtimestamp(weather_data['dt']))
    )
    
    sql = """INSERT INTO dbbikes.weather_Dublin_test (Clouds,feels_like,humidity,pressure,
    temp,temp_max,temp_min,sunrise,sunset,visibility,weather_description,
    weather_main,wind_deg,wind_speed,dt) 
    VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
    '%s','%s','%s','%s','%s')""" % weather_vals
    
    try:
        cursor.execute(sql)
        db.commit()
        print("insert ok")
    except:
        db.rollback()
        print("insert wrong")
    
    db.close()
    

while True:
    try:
        db = pymysql.connect(
            host="dbbikes.ccmhqwttjfav.us-east-1.rds.amazonaws.com",
            user="admin",
            password="12345678",
            port=3306,
            database="dbbikes")
        cursor = db.cursor()  
            
        create_table()

        now = datetime.now()
        r = requests.get(weather_URL, params = parameters)
        print(r,now)
            
        write_to_db(r.text)
            
        time.sleep(300)
        
    except:
        print(traceback.format_exc())    