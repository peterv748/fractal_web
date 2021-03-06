# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory to /app
WORKDIR /test_web_app

# Copy the current directory contents into the container at /app
COPY . /test_web_app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt




# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["python", "test_web.py"]