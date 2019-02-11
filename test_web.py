from flask import Flask, render_template, request, url_for
# from flask_thumbnails import Thumbnail
import os
import random
from redis import Redis, RedisError
import socket
import datetime


app = Flask(__name__)
# thumb = Thumbnail(app)
# app.config['THUMBNAIL_MEDIA_ROOT'] = './'
# app.config['THUMBNAIL_MEDIA_URL'] = './media'
# app.config['THUMBNAIL_DEFAUL_FORMAT'] = 'PNG'
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2, port=6379)


images = [
    "mandel1.png",
    "mandel2.png",
    "mandel3.png",
    "julia1.png",
    "julia2.png",
    "julia3.png",
    "koch1.png",
    "koch2.png",
    ]

image_path = " "

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
   
    image_path = imagename + ".png"
    full_filename = url_for('static', filename=image_path)

    return render_template("fractals.html", user_image = full_filename, hostname=socket.gethostname(), visits=visits)

@app.route('/news')
def show_news():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

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
def show_web_hoook():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    date_time= datetime.datetime.now()
    message_post = " "
    message_get = " "

    if request.method=='POST':
        message_post= "last redeploy: "+ " docker stack deploy -c docker-compose.yml fractal has been executed"
    else:
        message_get= "no updates sofar"

    return render_template("web_hook.html", hostname=socket.gethostname(), visits=visits, message_post=message_post, message_get=message_get, date_time=date_time)

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
