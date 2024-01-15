# ex2

make nginx configuration as follow:
- proxy from port 8080
- limit users for only one request per second
- allow each client IP address to open no moer than 5 connections to the app
- prevent a partner from connecting to the web

## create the systemd service unit file. Creating a systemd unit file will allow Ubuntu’s init system to automatically start Gunicorn and serve the Flask application whenever the server boots:

```bash
sudo nano /etc/systemd/system/myproject.service
```
```bash
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myproject
Environment="PATH=/home/sammy/myproject/myprojectenv/bin"
ExecStart=/home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```
now start the Gunicorn service:
```bash
sudo systemctl start myproject
sudo systemctl enable myproject
sudo systemctl status myproject
```


## Configuring Nginx to Proxy Requests:
creating a new server block configuration file in Nginx’s sites-available directory:

```bash
sudo nano /etc/nginx/sites-available/myproject
                                                               
limit_req_zone $binary_remote_addr zone=req_limit:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=connect_limit:10m;
server {
    listen 8080;
    server_name 10.1.0.87;

    location / {
        proxy_pass http://unix:/home/roy/PythonFinalProject/weather_app.sock;
        limit_req zone=req_limit;
        limit_conn connect_limit 5;
        deny 10.1.0.76;
    }
    location /static {
        alias /home/roy/PythonFinalProject/static;
    }

}

```

## enable the Nginx server block configuration you’ve just created, link the file to the sites-enabled directory:

```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

