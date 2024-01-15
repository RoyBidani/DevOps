
# Weather Application Deployment Guide 
This README document provides a step-by-step guide on how to deploy the Python-based weather forecast project on an AWS server.
## Initial Setup on Local Machine
1. Navigate to the project directory on your local machine:
   
2. Zip the project using the following command:

## SSH to the AWS Server
Before proceeding, ensure you have run 'chmod 400' on the '*.pem' file, otherwise ssh won't work.
1. Log into your AWS instance:

   
2. Create the necessary directories on the server:
   ```shell
   mkdir weather_app
   cd /var
   mkdir sockets
   sudo chmod +777 sockets
   ```
   
## Copying the Project to the AWS Server
On your local machine, run the following command in a new terminal window to copy the project to your server:
```shell
sudo scp -i /path/to/key.pem  path/to/zip/file  ec2-user@ec2-3-70-236-29.eu-central-1.compute.amazonaws.com:path/to/dir/on/vm
```
## Setting Up the Project on AWS Server
Once the file transfer is complete, switch back to the AWS server terminal:
1. Extract the application archive:
   ```shell
   unzip python_weather_forecast.zip
   ```
2. Remove the archive after extraction:
   ```shell
   rm -dr python_weather_forecast.zip
   ```
3. Navigate to the project directory:
   
4. Create a new Python virtual environment:
   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install the required dependencies:
   ```shell
   pip install gunicorn flask requests
   ```
If you encounter issues with OpenSSL and urllib3 versions while trying to use gunicorn  [Source: StackOverflow post](https://stackoverflow.com/questions/76187256/importerror-urllib3-v2-0-only-supports-openssl-1-1-1-currently-the-ssl-modu), run the following command inside the virtual environment:
```shell
pip install urllib3==1.26.6
```
To deactivate the virtual environment, use `deactivate`.

## Nginx Installation
Install Nginx on the AWS server:
```shell
sudo amazon-linux-extras install nginx1
```
## Nginx Configuration
1. Navigate to the Nginx configuration:
   ```shell
   sudo nano /etc/nginx/conf.d/weather_app.conf
   ```
2. Add the configuration:
   ```nginx
   server {
       listen 80;
       server_name vmIP;
       location / {
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_pass http://unix:/var/sockets/weather_app.sock;
       }
   }
   ```
## Setting Up Gunicorn Service
1. Create a new service file:
   ```shell
   sudo nano /etc/systemd/system/weather_app.service
   ```
2. Add the following content (change to your own working dir , env and execstart should be in your project's dir):
   ```ini
   [Unit]
   Description=Gunicorn instance to serve weather_app
   After=network.target
   [Service]
   User=ec2-user
     
   Group=ec2-user
   WorkingDirectory=/path/to/project/directory
   Environment="PATH=/path/to/project/directory/venv/bin"
   ExecStart=/path/to/project/directory/venv/bin/gunicorn -w 4 app:app -b unix:/var/sockets/weather_app.sock
   [Install]
   WantedBy=multi-user.target
   ```
3. Start the service:
   ```shell
   sudo systemctl start weather_app
   ```
You can check the service status with `sudo systemctl status weather_app`.

## Troubleshooting Gunicorn
If you face any issues while trying to activate Gunicorn service, activate the virtual environment and check the Gunicorn error msg:
```shell
source venv/bin/activate
gunicorn -w 4 main:app -b unix:/var/sockets/weather_app.sock
```

To restart the Gunicorn service:
```shell
sudo systemctl daemon-reload
sudo systemctl start weather_app.service
```
After starting Gunicorn service, restart the Nginx service:
```shell
sudo service nginx restart
```
## Enabling HTTPS
1. Navigate to the project directory:
   ```shell
   cd /path/to/project/directory
   ```
2. Generate a .pem key:
   ```shell
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```
3. Update the Nginx configuration:
   ```shell
   sudo nano /etc/nginx/conf.d/weather_app.conf
   ```
Add the following lines in the server block to enable SSL:
```nginx
listen 443 ssl;
ssl_certificate /path/to/project/directory/cert.pem;
ssl_certificate_key /path/to/project/directory/key.pem;
```
4. Restart Nginx and Gunicorn service:
   ```shell
   sudo systemctl daemon-reload
   sudo systemctl start weather_app.service
   sudo systemctl restart nginx
   ```
Nginx will now listen on port 443 and serve HTTPS traffic using the SSL certificate and private key specified in the configuration.

