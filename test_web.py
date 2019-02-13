from flask import Flask, render_template, request, url_for
# from flask_thumbnails import Thumbnail
import os
import random
from redis import Redis, RedisError
import socket
from datetime import datetime
from newsapi import NewsApiClient

app = Flask(__name__)
temp = None


try:
    redis = Redis(host= "redis", db=0, socket_connect_timeout=2, socket_timeout=2, port=6379)
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

    return render_template("home.html", hostname=socket.gethostname(), visits=visits)

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

    newsapi = NewsApiClient(api_key='1f8755052a0040efa1210d8df55ca6df')

    top_headlines = newsapi.get_top_headlines(q='wiskunde',
                                          sources='rtl-nieuws',
                                          category='wetenschap',
                                          language='nl',
                                          country='nl')
    # checks inbouwen !!!!
    all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='rtl-nieuws',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2018-01-01',
                                      to='2019-02-12',
                                      language='nl',
                                      sort_by='relevancy',
                                      page=2)
    # checks inbouwen !!!!

    sources = newsapi.get_sources()
    # checks inbouwen
    return render_template("news.html", hostname=socket.gethostname(), visits=visits) 

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
