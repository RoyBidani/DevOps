# ex1

deploy web application of VM using Gunicorn and Nginx 

## Installing the Components :

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

## Creating a Python Virtual Environment:

```bash
sudo apt install python3-venv

# inside the project directory create the virtual environment to store my Flask project:
python3 -m venv myprojectenv

#Before installing applications within the virtual environment, we need to activate it:
source myprojectenv/bin/activate

```

## Setting Up a Flask Application

```bash
pip install wheel
pip install gunicorn flask
```

## Configuring Gunicorn:

```bash
cd ~/myproject
gunicorn --bind 0.0.0.0:5000 app:app
# after we confirmed it worked we done using the virtual environment, so we can deactivate it:
deactivate

```
