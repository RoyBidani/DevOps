# Build stage1: Python build
FROM python:3.9-slim-buster as builder

WORKDIR /app

# Install the necessary Python dependencies including prometheus_client, logging, and wheel
RUN pip install wheel gunicorn flask requests chardet charset_normalizer prometheus_client -t .

# Copy app source code into the container
COPY app /app

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

