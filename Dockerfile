# Using an official Python runtime as a parent image
FROM python:3.9-slim

# Setting the working directory in the container
WORKDIR /app

# Copying the dependencies file to the working directory
COPY requirements.txt .

# Installing any needed packages specified in requirements.txt
# The --no-cache-dir option reduces the image size.
# This command will also install the 'en_core_web_sm' model
# as it's listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copying the rest of the application's code into the container at /app
# Making sure to have a .dockerignore file to exclude unnecessary files
# (e.g., .git, __pycache__, venv, .idea, *.tmp)
COPY . .

# Making port 5000 available to the world outside this container
# This is the port your Flask app runs on as defined in app.py
EXPOSE 5000

# Commanding to run the application
# app.py already specifies host='0.0.0.0' and port=5000
CMD ["python", "app.py"]