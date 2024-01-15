# Final Project:

## 1. Build Python Application Git + Python + DB

The project consists of a Python application using Flask, MongoDB, and Docker. The team collaborates on the same Source Code Management (SCM) for efficient development.

## 2. CI/CD Pipelines

CI/CD pipelines are implemented to automate the Continuous Integration (CI) and Continuous Deployment (CD) processes. These pipelines facilitate the development workflow and ensure the reliability of the application.

## 3. Tagging Logic Using Bash

A robust tagging logic is implemented using Bash scripting. This ensures proper versioning and tagging of the codebase for better tracking and release management.

## 4. Handling Unexpected Situations in CI/CD Pipelines

The CI/CD pipelines are designed to handle unexpected situations gracefully. Error handling and recovery mechanisms are in place to ensure the stability of the deployment process.

## 5. Containerization with Docker

The application is containerized using Docker, allowing for consistency in deployment across different environments.

## 6. Networking: Domain + SSL Cert

The application is configured with a custom domain and secured with an SSL certificate. This enhances security and provides a user-friendly experience.

## 7. Kubernetes Deployment in EKS with Ingress Controller

The deployment of the application is orchestrated using Kubernetes (K8s) in Amazon Elastic Kubernetes Service (EKS). An Ingress Controller is utilized for efficient traffic routing.

## 8. HELM for Templating K8S Manifest Files

HELM is employed for templating Kubernetes manifest files. This simplifies the management and deployment of Kubernetes resources.

## 9. Logs Visibility

Logs visibility is ensured for effective monitoring and troubleshooting. Proper log management practices are implemented to track application behavior.

## 10. Metric Visibility

Metric visibility is established to monitor the application's performance and resource utilization. This facilitates proactive identification and resolution of potential issues.

## 11. Infrastructure as Code (IAC) - Multi-Region EKS Deployment

Infrastructure as Code (IAC) is implemented to replicate the EKS infrastructure in another region. This ensures consistency and scalability across multiple regions.

## 12. Verification of Workload in Another Region

The duplicated EKS infrastructure is verified to ensure the entire workload is functional. This validation confirms the robustness of the deployment across different regions.

## 13. Time Taken for the Entire Deployment

The time taken for the entire deployment process is recorded. This metric provides insights into the efficiency of the CI/CD pipelines and the deployment workflow.

---

# Part 1: Git + Python + DB

### app.py

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId  # Import ObjectId for proper conversion

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongo:27017/notedb'
mongo = PyMongo(app)

@app.route('/')
def index():
    notes = mongo.db.notes.find()
    return render_template('main.html', notes=notes)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        mongo.db.notes.insert_one({'title': title, 'content': content})
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/delete/<note_id>', methods=['GET'])
def delete(note_id):
    mongo.db.notes.delete_one({'_id': ObjectId(note_id)})
    return redirect(url_for('index'))

@app.route('/read/<note_id>', methods=['GET'])
def read(note_id):
    note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})
    return render_template('read.html', note=note)

@app.route('/update/<note_id>', methods=['GET', 'POST'])
def update(note_id):
    note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        mongo.db.notes.update_one({'_id': ObjectId(note_id)}, {'$set': {'title': title, 'content': content}})
        return redirect(url_for('index'))

    return render_template('update.html', note=note)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

```

### Dockerfile

```dockerfile
FROM python:3.8-slim-buster

WORKDIR /FinalProgect

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

```

### docker-compose.yml

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mongo
  mongo:
    image: "mongo:latest"
    ports:
      - "27017:27017"

```

### Requirements.txt

```plaintext
flask
gunicorn
pymongo
requests
bs4
Flask-PyMongo
```
```html
```
### HTML Files

### - layout.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notes App</title>
</head>
<body>
    <header>
        <h1>Notes App</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>

```
### - main.html:
```html
{% extends 'layout.html' %}

{% block content %}
<h2>All Notes</h2>
<ul>
    {% for note in notes %}
    <li><a href="{{ url_for('read', note_id=note._id) }}">{{ note.title }}</a> - <a href="{{ url_for('update', note_id=note._id) }}">Edit</a> - <a href="{{ url_for('delete', note_id=note._id) }}">Delete</a></li>
    {% endfor %}
</ul>
<a href="{{ url_for('create') }}">Create a new note</a>
{% endblock %}

```
### - create.html:
```html
{% extends 'layout.html' %}

{% block content %}
<h2>Create Note</h2>
<form method="post">
    <label for="title">Title:</label>
    <input type="text" id="title" name="title" required>
    <br>
    <label for="content">Content:</label>
    <textarea id="content" name="content" required></textarea>
    <br>
    <input type="submit" value="Create Note">
</form>
{% endblock %}

```
### - read.html:
```html
{% extends 'layout.html' %}

{% block content %}
<h2>{{ note.title }}</h2>
<p>{{ note.content }}</p>
<a href="{{ url_for('update', note_id=note._id) }}">Edit</a>
<a href="{{ url_for('delete', note_id=note._id) }}">Delete</a>
<a href="{{ url_for('index') }}">Back to Notes</a>
{% endblock %}

```
### - update.html:
```html
{% extends 'layout.html' %}

{% block content %}
<h2>Edit Note</h2>
<form method="post" action="{{ url_for('update', note_id=note['_id']) }}">
    <label for="title">Title:</label>
    <input type="text" id="title" name="title" value="{{ note.title }}" required>
    <br>
    <label for="content">Content:</label>
    <textarea id="content" name="content" required>{{ note.content }}</textarea>
    <br>
    <input type="submit" value="Update Note">
</form>
<a href="{{ url_for('index') }}">Cancel</a>
{% endblock %}

```
- error.html:
```html
{% extends 'layout.html' %}

{% block content %}
<h2>Error</h2>
<p>Something went wrong.</p>
<a href="{{ url_for('index') }}">Back to Home</a>
{% endblock %}

```
### - delete.html:
```html
{% extends 'layout.html' %}

{% block content %}
<h2>Delete Note</h2>
<p>Are you sure you want to delete this note?</p>
<form method="post" action="{{ url_for('delete', note_id=note._id) }}">
    <input type="submit" value="Delete">
</form>
<a href="{{ url_for('index') }}">Cancel</a>
{% endblock %}

```

---

# Part 2: CI/CD Pipelines

