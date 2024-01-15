# ELK Stack Setup Guide

This guide walks you through setting up the ELK (Elasticsearch, Logstash, and Kibana) Stack on an Ubuntu machine and integrating it with a Python-based Weather app running on a separate EC2 instance.

## Table of Contents

1. [Set up ELK Stack](#1-set-up-elk-stack)
2. [Add Logs to the Weather App](#2-add-logs-to-the-weather-app)
3. [Run the Weather App on a Different EC2 Instance with Filebeat](#3-run-the-weather-app-on-a-different-ec2-instance-with-filebeat)

---

## 1. Set up ELK Stack

### Step 1: Install Docker

If Docker is not already installed on your Ubuntu machine, open a terminal and run these commands:

```bash
sudo apt update
sudo apt install docker.io
```

### Step 2: Start and Enable Docker Service

Start and enable the Docker service with these commands:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 3: Install Docker Compose

Install Docker Compose using the following command:

```bash
sudo apt install docker-compose
```

### Step 4: Create a Directory for ELK Stack Configuration

Create a directory to store your ELK Stack configuration files:

```bash
mkdir elk-stack
cd elk-stack
```

### Step 5: Create a Docker Compose File

Create a `docker-compose.yml` file for ELK Stack with the following content:

```yaml
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    container_name: elasticsearch
    ports:
      - 9200:9200
    environment:
      - discovery.type=single-node
  logstash:
    image: docker.elastic.co/logstash/logstash:7.15.0
    container_name: logstash
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - 5044:5044
      - 5000:5000
      - 9600:9600
  kibana:
    image: docker.elastic.co/kibana/kibana:7.15.0
    container_name: kibana
    ports:
      - 5601:5601
```

### Step 6: Start ELK Stack Containers

Start the ELK Stack containers using the following command:

```bash
docker-compose up -d
```

This command will download the ELK Stack Docker images and start the containers in the background.

---

## 2. Add Logs to the Weather App

To add logs to your Python Flask-based Weather app, import the `logging` module and configure it. Here's an example of how to add logs with different severity levels in your app:

```python
import logging  # Import the logging module

# Configure the logger
logging.basicConfig(filename='weather_app.log', level=logging.DEBUG)

@app.route('/logs')  # Define a route for '/logs'
def index():
    # Log messages with different severity levels
    logging.debug('This is a debug message')  # Log a debug message
    logging.info('This is an info message')    # Log an info message
    logging.warning('This is a warning message')  # Log a warning message
    logging.error('This is an error message')    # Log an error message
    logging.critical('This is a critical message')  # Log a critical message
    return 'Weather App'  # Return 'Weather App' as the response
```

This code sets up a Flask web application with logging at different levels and writes logs to a file named `weather_app.log`.

---

## 3. Run the Weather App on a Different EC2 Instance with Filebeat

### Step 1: Set Up a New EC2 Instance

Set up a new EC2 instance (t3a.large) with Ubuntu.

### Step 2: Install Docker and Filebeat

Install Docker on the EC2 instance using the following commands:

```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 3: Create a Docker Compose File

Create a Docker Compose file that creates containers for your Weather app and Filebeat. Configure the following:

```yaml
version: '3'
services:
  app:
    image: corenn2/weather_app:latest
    container_name: weather_app
    # Define other configurations for your app container as needed
    volumes:
      - logs:/logs  # Mount a volume for your app logs
    ports:
      - "80:5000"
    restart: always
  filebeat:
    build:
      context: .
      dockerfile: dockerfile
    container_name: filebeat
    volumes:
      - logs:/logs  # Mount the same volume as your app
    networks:
      - elk_network
    restart: always
networks:
  elk_network:
    driver: bridge
volumes:
  logs:
```

Ensure that you have a Dockerfile for Filebeat that looks like this:

```dockerfile
# Use the official Filebeat image
FROM docker.elastic.co/beats/filebeat:7.15.0

# Copy the Filebeat configuration
COPY filebeat.yml /usr/share/filebeat/filebeat.yml

# Switch to the root user to change file permissions and ownership
USER root

# Adjust file permissions and ownership
RUN chmod 644 /usr/share/filebeat/filebeat.yml && chown root:filebeat /usr/share/filebeat/filebeat.yml

# Switch back to the filebeat user for security
USER filebeat

# Set the Filebeat configuration file as the entry point
CMD ["-c", "/usr/share/filebeat/filebeat.yml"]
```

Configure the `filebeat.yml` file like this:

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /logs/app.log  # Adjust the path to match your log file location

output.logstash:
  hosts: ["172.31.33.223:5044"]  # Replace with your ELK stack server's IP and port

logging.level: info
logging.to_files: true
logging.files.path: /var/log/filebeat
logging.files.name: filebeat.log
```

Ensure that a directory called 'logs' is inside your Weather app directory and that `app.log` is inside it.

### Step 4: Run the Docker Compose

Run the Docker Compose command to start the containers:

```bash
sudo docker-compose up -d
``

`

### Step 5: Configure logstash.conf

On the ELK server, create a 'logstash.conf' file with the following content:

```conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Add your custom filters here if needed.
}

output {
  elasticsearch {
    hosts => "elasticsearch:9200" # Replace with your Elasticsearch host and port
    index => "weather-%{+YYYY.MM.dd}" # Customize the index name
  }
}
```

Then run Logstash using:

```bash
sudo docker rm -f $(sudo docker ps -aq)
sudo docker rmi -f $(sudo docker images -aq)

sudo docker-compose up -d
```

### Step 6: Access Kibana

When all containers are running, access Kibana on port 5601. Go to the left menu, select "Stack Management," then "Index Patterns," and create an index pattern using the index name you defined in the logstash.conf file (`weather-`).

Now, you can create a dashboard visualization to monitor your Weather app logs effectively.

That's it! You've successfully set up the ELK Stack and integrated it with your Python Weather app for logging and monitoring.
