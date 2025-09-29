# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the backend application code
COPY . /app

# The command to run the application will be specified in docker-compose.yml
# This makes the Dockerfile more reusable.
# Expose the port the app runs on
EXPOSE 8000
