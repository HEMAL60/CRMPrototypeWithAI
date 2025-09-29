# Use an official Python runtime as a parent image
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly copy the application source code.
# The model and training script are handled at runtime via volumes.
COPY ./app ./app

# Expose the port the app runs on
EXPOSE 8000

# Define the standard command to run the app.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

