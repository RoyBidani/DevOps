# Docker Exercises on Ubuntu 22.04 ARM64

This repository contains a set of Docker exercises for Ubuntu 22.04 ARM64.

## Exercise Instructions

### 1. Install Docker:
   - Update the system's package lists: `sudo apt update`
   - Install the `docker.io` package: `sudo apt install docker.io`
   - Start and enable the Docker service: `sudo systemctl start docker` and `sudo systemctl enable docker`

### 2. Run your first container with the `ubuntu:latest` image:
   - Run the command: `docker run -it ubuntu:latest`
     - `it`: These options are used together to keep the container running so that you can interact with the shell inside the container.

### 3. Check if the container is still running:
   - Run the command: `docker ps`

### 4. Find the name of the container you just created, and run another container from the same image and give it a name of your choice.
   - Run the command: `docker ps -a`
   - `sudo docker run -it --name my_cont ubuntu:latest`

### 5. Display existing local images:
   - Run the command: `docker images`

### 6. Stop the containers:
   - Run the command: `docker stop <container_id>`

### 7. Display all containers, including inactive ones:
   - Run the command: `docker ps -a`

### 8. Delete the first container only:
   - Run the command: `docker rm <container_id>`

### 9. Restart the container you named:
   - Run the command: `docker restart <container_name>`

### 10. Create a new directory in the container:
    - Run the command: `docker exec -it <container_name> mkdir /your_directory_name`

### 11. Enter the container shell:
    - Run the command: `docker exec -it <container_name> /bin/bash`

### 12. Exit the container without stopping it:
    - If you are running the container interactively using the `-it` flag, you can press `Ctrl + P` followed by `Ctrl + Q`. This detaches your terminal from the container without stopping it.

### 13. Pull the `nginx:alpine` image and find information about it:
    - Pull the image: `docker pull nginx:alpine`
    - Find the number of layers: `docker image inspect nginx:alpine`
    - Find which port is exposed: `sudo docker exec <container_id> cat /etc/nginx/nginx.conf`
      (If the configuration file doesn't explicitly specify a port, Nginx will typically use the default HTTP port 80.)
    - Find the Nginx version: `docker exec <container_id> nginx -v`

### 14. Create a new Dockerfile for the "yes" image:
    ```
    FROM ubuntu:latest

    RUN apt-get update && apt-get install -y --no-install-recommends \
        yes \
        && rm -rf /var/lib/apt/lists/*

    CMD ["yes", "DEVOPS"]
    ```
    
### 15. Build the "yes" image:
    - Run the command: `docker build -t yes .`

### 16. Run a container using the "yes" image:
    - Run the command: `docker run yes`

### 17. The "yes" image consists of three layers. Each instruction in the Dockerfile creates a new layer, resulting in three layers.

### 18. Push the "yes" image to Docker Hub:
    - Create a Docker Hub account
    - Tag the image: `docker tag yes <username>/yes`
    - Push the image: `docker push <username>/yes`

### 19. Write a Bash script that prints names in an infinite loop:
    - Create a file named `names.sh`:
      ```bash
      #!/bin/bash
      while true
      do
          echo "David"
          echo "Elad"
          echo "Shay"
          echo "Yarin"
          echo "Guy"
          sleep 1
      done
      ```

### 20. Run the script on an Ubuntu-based container:
    - Run the command: `docker run -v absolute/path/to/names.sh:/:/name ubuntu bash /name`

### 21. Create a new Dockerfile for the "lab_names" image:
    ```
    FROM ubuntu:latest

    # Install any necessary dependencies
    RUN apt-get update && apt-get install -y --no-install-recommends \
        bash \
        && rm -rf /var/lib/apt/lists/*

    # Copy the Bash script to the container
    COPY name.sh /name.sh

    # Set the default user for the container
    USER nobody

    # Set the entry point to run the Bash script
    ENTRYPOINT ["bash", "/name.sh"]
    ```
    - Run the command: `sudo docker build -t lab_names -f Dockerfile2 .`
    


### 22. Run Jenkins Server on a Docker Container

#### How to Run Jenkins Server on a Docker Container

1. **Pull Jenkins Image**: Open a terminal or command prompt and execute the following command to pull the official Jenkins Docker image from Docker Hub:
    ```
    docker pull jenkins/jenkins:lts
    ```
    This command will download the latest LTS (Long-Term Support) version of Jenkins.

2. **Run Jenkins Container**: Once the Jenkins image is pulled, you can create and run a Docker container using the following command:
    ```
    docker run -d -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
    ```
    This command creates a new container and maps port 8080 on your machine to the container's port 8080 (used for accessing the Jenkins web interface) and port 50000 (used for Jenkins agent communication).

3. **Access Jenkins**: After the container is running, you can access the Jenkins web interface by opening a web browser and navigating to `http://localhost:8080`. You will be prompted to set up Jenkins by entering an initial admin password.

4. **Retrieve Initial Admin Password**: To retrieve the initial admin password, you need to access the container's console output. Execute the following command to retrieve the password:
    ```
    docker logs <container_id>
    ```

### 23. Run Nginx Container with Custom Port

Using the Nginx official image, run the Nginx default website and set the container port to be accessed as 8989 instead of 80.

1. **Pull Nginx Image**: Open a terminal or command prompt and execute the following command to pull the official Nginx Docker image from Docker Hub:
    ```
    docker pull nginx
    ```

2. **Run Nginx Container**: Once the Nginx image is pulled, you can create and run a Docker container using the following command:
    ```
    sudo docker run -d -p 8989:80 nginx
    ```


### 24. Build Docker Image for Python Weather Application:

   To build a Docker image for a Python weather application, follow these steps:

   1. Create a Dockerfile in the project directory:
      ```Dockerfile
      # Use the official Python image as the base image
      FROM python:3.9

      # Set the working directory inside the container
      WORKDIR /app

      # Copy the requirements.txt file to the container
      COPY requirements.txt .

      # Install the Python dependencies
      RUN pip install --no-cache-dir -r requirements.txt

      # Copy the rest of the application code to the container
      COPY . .

      # Expose the port on which the application will run
      EXPOSE 8000

      # Set the entrypoint command for the container
      CMD ["python", "app.py"]
      ```

   2. Create a requirements.txt file listing the Python dependencies required for the application.
         
     Flask==2.0.1
    requests==2.26.0
    gunicorn==20.1.0
    Jinja2==3.0.1

   3. Build the Docker image:
      ```
      sudo docker build -t weather-app .
      ```

### 25. Deploy Python Web Application using NGINX and Gunicorn (Multistage Build):

   To deploy a Python web application using NGINX and Gunicorn with a multistage build, follow these steps:

   1. Create a Dockerfile for the multistage build in the project directory:
   
      
    # Build stage1: Python build
    FROM python:3.9-slim-buster as builder

    WORKDIR /app

    ADD /app /app

    RUN pip install wheel gunicorn flask requests -t .

    # Deploy Stage2: NGINX for reverse proxy
    FROM nginx:1.21-alpine as deploy

    WORKDIR /app

    # Copy app build from previous stage
    COPY --from=builder /app /app

    # Install pip
    RUN apk --no-cache add py3-pip

    # Install gunicorn using pip
    RUN pip install gunicorn

    # Copy nginx configuration
    COPY nginx.conf /etc/nginx/conf.d

    EXPOSE 8080

    CMD nginx && gunicorn --bind 0.0.0.0:8000 app:app

      

   2. nginx.conf:
    
    server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://0.0.0.0:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    }

    

   3. Build the Docker image:
      ```
      sudo docker build -t myapp .
      ```

   4. Run the application:
      ```
      sudo docker run -d -p 8080:8080 myapp
      ```
      
      
## 26. Using Docker Compose, set up an instance of your Python application automatically.
- See `docker-compose.yml` .
    ```
    version: '3'
    services:
      myapp:
        build:
          context: .
         dockerfile: Dockerfile25
        ports:
          - 8085:8000
        volumes:
          - ./app:/app

    ```

Docker Compose is a tool that allows you to define and manage multi-container Docker applications. It simplifies the process of defining and running multiple Docker containers that work together as a single application.

***Explanation:***
- `services:`: This keyword is used to define the services that will be created and managed by Docker Compose.
- `app:`: This is the name of the service. You can choose any name you like for your services.
- `build:`: This specifies how to build the Docker image for the "app" service. The build process is defined using a series of sub-options.
- `context: .`: This specifies the build context, which is the path to the directory containing the `Dockerfile` and any files required during the build process.
- `dockerfile: Dockerfile`: This specifies the name of the `Dockerfile` used for building the image.
- `ports:`: This option maps ports between the Docker container and the host system.
  - `"8085:80"`: This maps port **`80` in the container** to port **`8000` on the host** system. It means that any requests made to port `8085` on the host will be forwarded to port `80` inside the container.
- `volumes:`: This option allows you to mount directories or files from the host system into the container.
  - `.-/app`: This mounts the current directory on the host system to the `/app` directory inside the container. This allows the container to access and modify the files in the current directory.

  
1. save the docker-compose.yml file.

2. In your project directory, open a terminal and run the following command to start the Docker Compose setup:

    ```
    docker-compose up
    ```
    
This command will build the Docker image using the specified Dockerfile and start the container based on the configuration in the docker-compose.yml file.

You should see the logs from the container, indicating that your Python application is running. You can access your application at http://localhost:8085.



## 27. Use an Nginx container to load balance between two separate container instances of the Flask application. Automate everything to be deployed with Docker Compose.
### The user accessing the website should be able to request it from the Nginx instance only, and not directly from the application instances.

1. Create a docker-compose.yml file in your project directory with the following content:
    ```
        version: '3'
    services:
      app1:
        build:
          context: .
          dockerfile: Dockerfile25
    ports:
      - 8080
      app2:
        build:
          context: .
          dockerfile: Dockerfile25
    ports:
      - 8085
      nginx:
        image: nginx
        ports:
          - 80:80
        volumes:
          - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro

    ```
    
2. Create an nginx.conf file in the project directory with the following content:
   ```
   http {
    upstream app_servers {
        server app1:8080;
        server app2:8085;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://app_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
   }

   ```
   
3. Make sure your Flask application's Dockerfile (Dockerfile25) is in the project directory. Adjust it according to your specific requirements.

4. Build and start the containers using Docker Compose: 

    ```
    docker-compose up -d
    ```
    
Docker Compose will build the Flask application images (app1 and app2) using the Dockerfile25 and the Nginx image (nginx). It will also create a network and link the containers together.

The Flask application instances (app1 and app2) will be accessible internally on ports 8080 and 8085 within the Docker network. Nginx will be accessible externally on port 80.

Access your application through the Nginx load balancer by visiting http://localhost in your web browser. Nginx will distribute the requests between the two Flask application instances.
