A background task manager, made with Django, Celery and Redis. 

## Requirements

Execute the following commands:

```
sudo apt update
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
```
## Execute project locally

## Create a virtual environment by executing the following commands:

```
virtualenv btm
source btm/bin/activate
pip3 install -r requirements.txt
```
## Execute the project by running these commands:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## Don't forget 
To create a celery broker and add it to settings.py, add EMAIL_HOST to settings.py, and add the database settings.

## Execute project with nginx-gunicorn

Install Nginx using the following command:
```
sudo apt install nginx
```
## Set up firewall in two steps:
```
sudo ufw app list
sudo ufw allow 'Nginx HTTP'
```
Check the firewall:
```
sudo ufw status
```
Check server web by entering the localhost to verify (http://localhost/).

Other commands for Nginx include:

```
sudo systemctl stop nginx
sudo systemctl start nginx
sudo systemctl restart nginx 
sudo systemctl reload nginx
sudo systemctl disable nginx
sudo systemctl enable nginx
```
Check that Gunicorn works by running the command below.

```
gunicorn --bind 0.0.0.0:8000 django_celery.wsgi
```
Check localhost:8000.
## Create socket and service files

Create the Gunicorn socket by following these steps:

    Create the file socket systemd for Gunicorn:
```
sudo nano /etc/systemd/system/gunicorn.socket
```
Add the following content:
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
Save and close the file.

    Create the file service systemd for Gunicorn:

```
sudo nano /etc/systemd/system/gunicorn.service
```
Add the following content:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=william
Group=www-data
WorkingDirectory=/home/william/project/django-celery/django_celery
ExecStart=/home/william/project/django-celery/env_celery/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          django_celery.wsgi:application

[Install]
WantedBy=multi-user.target
```
## Save and close the file.

Start and enable the Gunicorn socket. This will create the socket file in /run/gunicorn.sock now and on startup:

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
Check the status of the service:

```
sudo systemctl status gunicorn.socket
```
To test the socket triggering mechanism, send a connection to the socket via curl using the following command:

```
curl --unix-socket /run/gunicorn.sock localhost
```


## Tip : If Gunicorn hasn't started, you can restart using 
```
sudo systemctl status gunicorn.service
```
This will show you the current status of the Gunicorn service, including whether it is active, the process ID (PID), and any recent log messages. If the service is not running or there are errors, you may need to troubleshoot the configuration file or check the Gunicorn logs for more information.

Once you've made these changes, save and close the file.

Finally, enable the new server block by creating a symbolic link from the sites-available directory to the sites-enabled directory:

```
sudo ln -s /etc/nginx/sites-available/django-celery /etc/nginx/sites-enabled/
```
Test the configuration file for syntax errors by running:
```
sudo nginx -t
```
## Restart Nginx to enable the changes:
```
sudo systemctl restart nginx
```

## Conclusion

This was my attempt of creating an app that can handle background tasks using Django, Celery and Redis. 
Thanks for reading!

