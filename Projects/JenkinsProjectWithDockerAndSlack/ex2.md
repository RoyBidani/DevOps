
```markdown
### 1. Ensure the Following Files and Directory are in Your Repository:
- `Dockerfile`
- `nginx.conf`
- `app_test.py`
- `app` directory containing all the app files.

#### Dockerfile:
```Dockerfile
# Build stage1: Python build
FROM python:3.9-slim-buster as builder

WORKDIR /app

# Install the necessary Python dependencies
RUN pip install wheel gunicorn flask requests chardet charset_normalizer -t .

# Copy app source code into the container
COPY app /app

# Deploy Stage2: NGINX for reverse proxy
FROM nginx:1.21-alpine as deploy

WORKDIR /app

# Copy app build from the previous stage
COPY --from=builder /app /app

# Install pip
RUN apk --no-cache add py3-pip

# Install gunicorn using pip
RUN pip install gunicorn

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 8080

CMD nginx && gunicorn --bind 0.0.0.0:8000 app:app
```

#### nginx.conf:
```nginx
server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://0.0.0.0:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### app_test.py:
```python
import unittest
import requests

class WebTestReachable(unittest.TestCase):

    def test_web_reachable(self):
        try:
            # Make a GET request to the website
            response = requests.get('http://localhost:8000')
            # Check that the response status code is 200
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.ConnectionError:
            # The website is not reachable
            self.assertFalse('Website is not reachable')


if __name__ == '__main__':
    unittest.main()
```

### 2. Create a Jenkins Pipeline:
```groovy
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_USERNAME = 'roybidani'
        DOCKERHUB_PASSWORD = 'R14081998'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching source code from GitLab...'
                git branch: 'main', credentialsId: '22f7c2eb-c3b6-4f21-bab1-bd30d73f3703', url: 'http://172.31.33.251/root/weather-app'
            }
        }

        
        
        stage('Build App Image') {
            steps {
                echo 'Start Docker build...'
                script {
                    sh "docker build -t roybidani/weather_app:app -f Dockerfile ."
                }
            }
        }
        stage('Run Website') {
            steps {
                echo 'Running website in a Docker container...'
                script {
                    sh "docker run -d -p 8000:8000 roybidani/weather_app:app"
                }
            }
        }
        
        stage('Test Website') {
            steps {
                echo 'Running and testing Docker image...'
                script {
                    // Find the container ID of the running container listening on port 8000
                    def testContainerId = sh(returnStdout: true, script: "docker ps -q --filter publish=8000/tcp").trim()

                    // Run the test script inside the Docker container if a container is found
                    if (testContainerId) {
                        sh "docker exec $testContainerId python3 app_test.py"
                    } else {
                        error "No running container found on port 8000"
                    }

                    // Stop and remove the test Docker container
                    sh "docker stop $testContainerId"
                    sh "docker rm -f $testContainerId"
                }
            }
        }
        
        stage('Push Docker image') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                script {
                    // Log in to Docker Hub
                    sh "docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_PASSWORD"

                    // Push the Docker image to Docker Hub
                    sh "docker image push roybidani/weather_app:app"
                }
            }
        }
    }
}

```


