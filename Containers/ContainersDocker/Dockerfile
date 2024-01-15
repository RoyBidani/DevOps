# Use the Linux Ubuntu base image
FROM ubuntu:latest

# Install the `yes` command
RUN apt-get update && apt-get install -y --no-install-recommends \
    yes \
    && rm -rf /var/lib/apt/lists/*


# Set the default command to "yes DEVOPS"
CMD ["yes", "DEVOPS"]
