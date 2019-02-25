from flask import Flask, render_template, request, url_for
import os
import random
from redis import Redis, RedisError
import socket
from datetime import datetime
import json
import requests as req



News_Api_Key = os.environ["NEWSORG_API_KEY"]
Weather_Api_Key = os.environ["OMW_API_KEY"]
IP_Api_Key = os.environ["IPDATA_API_KEY"]
Google_Api_Key = os.environ["GOOGLE_MAPS_API_KEY"]
REDIS_HOST = os.environ["REDIS_HOST"]
news_headlines_url = "https://newsapi.org/v2/top-headlines?sources=rtl-nieuws&apiKey={}".format(News_Api_Key)
news_topic_url = "https://newsapi.org/v2/everything?q=mathematics&from=2019-02-21&apiKey={}".format(News_Api_Key)
weather_url = "https://api.openweathermap.org/data/2.5/weather?q=Aalsmeer,nl&appid={}".format(Weather_Api_Key)

app = Flask(__name__)
temp = None


try:
    redis = Redis(host= REDIS_HOST, db=0, socket_connect_timeout=2, socket_timeout=2, port=6379)
    redis.set("counter", 0)
    redis.set("laststackdeploy", None)
    redis.set("datetimelaststackdeploy", None)
except RedisError:
    temp = None

@app.route('/')
@app.route('/home')
def show_home():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    Kelvin = 273.15
    main_forecast = {}
    main_description = ""
    main_temp = {}
    temp = ""
    url_data = req.get(weather_url)

    json_data_dict = dict(url_data.json())
    if url_data.status_code == 200:
    
       if json_data_dict['cod'] == 200:
          main_forecast = dict(json_data_dict['weather'][0] )
          main_description = main_forecast['description']
          main_temp = dict(json_data_dict['main'])
          temp = str(int(main_temp['temp']- Kelvin))
           
       else:
         print ("no data received")
    else:
      print ("sorry something went wrong, no connection " + url_data.text)

    return render_template("home.html", hostname=socket.gethostname(), visits=visits, api_key=Google_Api_Key, main_description=main_description, main_temp = temp)

@app.route('/fractals')
def show_fractal_index():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    return render_template("fractal_index.html", hostname=socket.gethostname(), visits=visits)

@app.route('/<string:imagename>')
def show_fractal_picture(imagename):
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    image_path = " "
    image_path = imagename + ".png"
    full_filename = url_for('static', filename=image_path)

    return render_template("fractals.html", user_image = full_filename, hostname=socket.gethostname(), visits=visits)

@app.route('/news')
def show_news():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    temp = {}
    url_data = req.get(news_headline_url)
    json_data_dict = dict(url_data.json())
    if url_data.status_code == 200:
    
       if json_data_dict["status"] == "ok":
          number_of_articles = len(json_data_dict["articles"])
          for key in range(0, number_of_articles):
              temp = dict(json_data_dict["articles"][key])
              print (str(key) + ": " + temp["title"])
              print (temp["description"])
              print ("read more: "+ temp["url"])
       else:
        print ("no data received")
    else:
      print ("sorry something went wrong " + url_data.text)
    
    return render_template("news.html", hostname=socket.gethostname(), visits=visits, api_key=News_Api_Key) 

@app.route('/about')
def show_about():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    return render_template("about.html", hostname=socket.gethostname(), visits=visits)

@app.route('/contact')
def show_contact():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    return render_template("contact.html", hostname=socket.gethostname(), visits=visits)

@app.route('/web_hook', methods=['GET','POST'])
def show_web_hook():
    message_post = None
    message_get = None
    date_time = None
    date_time_now = None
    date_time_str = ""
    date_time_now_str=""
    
    try:
            visits = redis.incr("counter")
            if request.method=='POST':
                 date_time= datetime.now()
                 date_time_str = f'{date_time:%d-%m-%Y %H:%M:%S}'
                 message_post= "update: docker stack deploy -c docker-compose.yml fractal has been executed"
                 redis.set("laststackdeploy", message_post)
                 redis.set("datetimelaststackdeploy", date_time_str)
                
            if request.method=='GET':
                message_get= "no updates sofar"
                date_time_now = datetime.now() 
                date_time_now_str = f'{date_time_now:%d-%m-%Y %H:%M:%S}'

            message_post = redis.get("laststackdeploy")
            date_time_str = redis.get("datetimelaststackdeploy")
    except RedisError:
            visits = "<i>cannot connect to Redis, counter disabled</i>"  
            if request.method=='POST':
                 date_time= datetime.now()
                 date_time_str = f'{date_time:%d-%m-%Y %H:%M:%S}'
                 message_post= "last redeploy: docker stack deploy -c docker-compose.yml fractal has been executed"
            else:
                 message_get= "no updates sofar"
                 date_time_now= datetime.now()    
                 date_time_now_str = f'{date_time_now:%d-%m-%Y %H:%M:%S}'

    return render_template("web_hook.html", hostname=socket.gethostname(), visits=visits, message_post=message_post, message_get=message_get, date_time=date_time_str, date_time_now=date_time_now_str)

@app.route('/link2')
def show_link2():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    return render_template("link2.html", hostname=socket.gethostname(), visits=visits)

@app.route('/link3')
def show_link3():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    return render_template("link3.html", hostname=socket.gethostname(), visits=visits)



if __name__=="__main__":
    app.run(host="0.0.0.0", port=80)
