# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /test_web_app

# Copy the current directory contents into the container at /app
COPY . /test_web_app

# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["python3.8", "docker_webhook_listener.py -t pvbv12748 -c "bash" "./say_hallo.sh""]