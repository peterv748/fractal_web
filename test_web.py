from flask import Flask, render_template, request, url_for
# from flask_thumbnails import Thumbnail
import os
import random
from redis import Redis, RedisError
import socket



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

@app.route('/link1')
def show_link1():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    return render_template("link1.html", hostname=socket.gethostname(), visits=visits)

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
