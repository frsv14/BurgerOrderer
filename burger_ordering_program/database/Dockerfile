# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /database

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY database.py .



# Set the environment variable for Flask
ENV FLASK_APP=database.py

# Expose the port the app runs on
EXPOSE 3306

# Run the application
CMD ["python3" , "database.py"]
