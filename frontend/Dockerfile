# Step 1: Start with a lightweight, official Python base image.
FROM python:3.9-slim-bullseye

# --- NEW: Install and configure locales ---
# Install the locales package
RUN apt-get update && apt-get install -y locales
# Uncomment the en_GB.UTF-8 locale in the config file
RUN sed -i -e 's/# en_GB.UTF-8 UTF-8/en_GB.UTF-8 UTF-8/' /etc/locale.gen && \
    # Generate the locale
    locale-gen
# Set the environment variable for the container
ENV LANG en_GB.UTF-8
ENV LANGUAGE en_GB:en
ENV LC_ALL en_GB.UTF-8
# --- End of new section ---

# Step 2: Set the working directory inside the container to /app.
WORKDIR /app

# Step 3: Copy the requirements file into the container.
COPY requirements.txt .

# Step 4: Install the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your main Streamlit application file.
COPY app.py .

# Step 6: Inform Docker that the container will listen on port 8501.
EXPOSE 8501

# Step 7: Define the command that will be executed when the container starts.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]