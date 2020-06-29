# Use an official Python runtime as a parent image
# FROM ubuntu:18.04
FROM python:3.8

# Set the working directory to /app
WORKDIR /test_listener

# Copy the current directory contents into the container at /app
COPY ./docker_webhook_listener.py /test_listener
COPY ./reqs_listener.txt /test_listener
COPY ./say_hallo.sh /test_listener

RUN python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r reqs_listener.txt

# Make port 80 available to the world outside this container
EXPOSE 9555

CMD ["python", "./docker_webhook_listener.py", "-t", "pvbv12748", "-c bash ./say_hallo.sh"]