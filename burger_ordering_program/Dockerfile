# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

RUN python add_user.py

RUN python database.py
# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
