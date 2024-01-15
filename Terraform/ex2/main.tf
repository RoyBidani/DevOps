# Define the required Docker provider and its version
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

# Configure the Docker provider
provider "docker" {}

# Define a Docker image resource named "weather_app"
resource "docker_image" "weather_app" {
  # Specify the name of the Docker image to use
  name = "roybidani/weather_app:app"
}

# Define a Docker container resource named "weather_app"
resource "docker_container" "weather_app" {
  # Use the image ID of the "weather_app" Docker image
  image = docker_image.weather_app.image_id

  # Set the name of the Docker container
  name = "weather_app_container"

  # Configure port mapping for the Docker container
  ports {
    internal = 8080 # Internal port within the container
    external = 8000 # External port on the host
  }
}

