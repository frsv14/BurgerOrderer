# Use the official MySQL image from the Docker Hub
FROM mysql:8.0

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=example
ENV MYSQL_DATABASE=burgerdb

# Copy the database initialization script into the container
COPY database.sql /docker-entrypoint-initdb.d/