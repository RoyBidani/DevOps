# Advanced

Add HTTPS support for the web application

## create ssl directory and move into it :

```bash
cd /etc/nginx
sudo mkdir ssl
cd ssl
```

## create private.key and certificate.crt files:

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out certificate.crt
```

## add the configuration:

```bash
sudo nano /etc/nginx/sites-available/myproject
```
to the server block add the lines:
```bash
  listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/certificate.crt;
    ssl_certificate_key /etc/nginx/ssl/private.key;
```

## restart services:
```bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl restart myproject
```
