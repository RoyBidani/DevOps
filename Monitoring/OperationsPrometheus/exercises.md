

# Prometheus and Grafana Workshop

This workshop guides you through setting up Prometheus and Grafana for monitoring and visualization of metrics.

## Table of Contents

1. [Exercise 1: Run Prometheus on the same EC2 instance](#exercise-1-run-prometheus-on-the-same-ec2-instance)
2. [Exercise 2: Expose Default Metrics from Your Python Project](#exercise-2-expose-default-metrics-from-your-python-project)
3. [Exercise 3: Install Grafana and Integrate with Prometheus](#exercise-3-install-grafana-and-integrate-with-prometheus)
4. [Exercise 5: Set Alert Rules and Send Them to Slack](#exercise-5-set-alert-rules-and-send-them-to-slack)

---

## Exercise 1: Run Prometheus on the same EC2 instance

### Step 1: SSH into your EC2 Instance

Connect to your EC2 instance via SSH.

```bash
ssh -i your-key.pem ec2-user@your-ec2-instance-ip
```

### Step 2: Download Prometheus

You can download Prometheus using `wget`:

```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.30.3/prometheus-2.30.3.linux-amd64.tar.gz
```

### Step 3: Extract Prometheus

```bash
tar -xzf prometheus-2.30.3.linux-amd64.tar.gz
cd prometheus-2.30.3.linux-amd64
```

### Step 4: Create a Prometheus Configuration File (prometheus.yml)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'your-python-app'
    static_configs:
      - targets: ['localhost:8000']
```

### Step 5: Run Prometheus

```bash
./prometheus --config.file=prometheus.yml
```

Prometheus should now be running on your EC2 instance, and you can access its web interface at `http://your-ec2-instance-ip:9090`.

---

## Exercise 2: Expose Default Metrics from Your Python Project

Assuming you are using a Python web framework like Flask, you can use a library like `prometheus_client` to expose metrics. Here's a simple example:

```python
import Api
from flask import Flask, render_template, request
from prometheus_client import start_http_server, Summary, Counter, generate_latest


# Create a Flask app
app = Flask(__name__)

# Create a Prometheus summary metric for request processing time
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Create a Prometheus counter metric for counting /weather requests
WEATHER_REQUESTS = Counter('weather_requests_total', 'Total number of /weather requests')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/weather", methods=['POST'])
def weather_display():
    location = request.form['location']
    weather_info = Api.get_weather(location)

    if weather_info[0]['cod'] == '404':
        error_message = 'City not found. Please enter a valid city.'
        return render_template('index.html', error_message=error_message)

    # Increment the weather request counter
    WEATHER_REQUESTS.inc()

    return render_template('weather.html', location=location, weather_info=weather_info)

# Add a /metrics route for Prometheus to scrape
@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)
    
    # Start your Flask app on host '0.0.0.0' and port 8080
    app.run(host='0.0.0.0', port=8080)
```

---

## Exercise 3: Install Grafana and Integrate with Prometheus

### Step 1: Install Grafana

```bash
sudo yum install -y https://dl.grafana.com/oss/release/grafana-8.0.6-1.x86_64.rpm
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### Step 2: Access the Grafana Web Interface

1. Open your web browser and navigate to the Grafana web interface. The default URL is usually `http://localhost:3000`.

2. Log in to Grafana using your credentials (the default username and password is usually `admin`/`admin`, but you should change this in a production environment).

### Step 3: Add Prometheus Data Source

1. Click on the gear icon (⚙️) in the left sidebar to access the "Configuration" menu.

2. Under the "Data Sources" section, click "Add data source."

3. Select "Prometheus" from the list of available data sources.

4. In the "HTTP" section, configure the following settings:
   - Name: Give your data source a name (e.g., "Prometheus").
   - URL: Enter the URL where your Prometheus server is running (e.g., `http://localhost:9090`).

5. Click the "Save & Test" button to verify the connection to Prometheus. You should see a "Data source is working" message if the connection is successful.

### Step 4: Create a Dashboard

1. Click on the "+" icon in the left sidebar to create a new dashboard.

2. In the "New Dashboard" screen, click "Add new panel."

3. In the panel editor, configure the panel settings:
   - Visualization: Choose the visualization type that best suits your metric data (e.g., "Graph" or "Singlestat").
   - Query: Use the Prometheus query language to select the metric you want to display. For example, to display the `weather_requests_total` metric, you can use `weather_requests_total` as the query.

4. Customize the panel as needed, including setting the title, axes, legends, and thresholds.

5. Click "Apply" to save the panel.

### Step 5: Organize Panels on the Dashboard

1. Return to the dashboard by clicking the dashboard name at the top of the screen.

2. Click "Add new panel" to add more panels as needed, each configured to display different metrics or visualizations.

3. To arrange and organize the panels on the dashboard, click the panel title and use the "Move" and "Resize" options.

### Step 6: Save the Dashboard

1. Click the disk icon (💾) at the top of the dashboard to save it.

2. Give your dashboard a name and optionally specify a folder to organize it. Click "Save" to confirm.

### Step 7: View and Share the Dashboard

You can now view and share your Grafana dashboard with others. Access the dashboard from the main dashboard list, and use the "Share" option to generate a shareable link or embed the dashboard in other web pages.

---

## Exercise 5: Set Alert Rules and Send Them to Slack

### Step 0: Create Slack Webhook

1. **Create Slack Incoming Webhook**:
   - Go to your Slack workspace.
   - Click on "Apps" in the left sidebar.
   - Search for "Incoming Webhooks" and install the app if not already installed.
   - Click on "Add to Slack" for the desired channel.
   - Copy the webhook URL provided after setup.

### Step 1: Create Alertmanager Configuration

Create a configuration file for Alertmanager, such as `alertmanager.yml`. You can create this file in the same directory as `prometheus.yml`.

```bash
nano alertmanager.yml
```

Here's a basic configuration example that includes Slack integration:

```yaml
route:
  receiver: 'slack-notifications'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK/URL'
        channel: '#prometheus'
        text: '{{ range .Alerts }}*{{ .Labels.alertname }}* is firing for {{ .Labels.instance }}. Value: {{ .Annotations.summary }}\n{{ end }}'
```

Replace `'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK/URL'` with the actual Slack webhook URL you created.

Save and exit the file.

To get the Alertmanager container up and running, don't forget to mount your configuration file:

```bash
docker pull prom/alertmanager
docker run -d --restart always -p 9093:9093 -v /path/to/alertmanager.yml:/etc/alertmanager/alertmanager.yml --name=alertmanager prom/alertmanager
```

### Step 2: Set Up Alerting in Prometheus

1. **Edit `prometheus.yml`**:
   Edit your Prometheus configuration file (`prometheus.yml`) to include alerting rules. Open the file for editing:

   ```bash
   nano prometheus.yml
   ```

   Add the following lines to your `prometheus.yml` file to configure alerting:

   ```yaml
   alerting:
     alertmanagers:
       - static_configs:
           - targets: ['localhost:9093']  # Replace with your Prometheus's private IP and Alertmanager container IP
   rule_files:
     - /home/prometheus-2.30.0.linux-amd64/alerting_rules.yml
   ```

   Replace `/home/prometheus-2.30.0.linux-amd64/alerting_rules.yml` with the path to your `alerting_rules.yml` file.

   Save and exit the file.

### Step 3: Create Alerting Rules

Now create another file, `alerting_rules.yml` with your alerting rules:

```yaml
groups:
  - name: my_alert
    rules:
      - alert: CityViewedMoreThanOnce
        expr: city_views_total > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: City {{ $labels.city }} has been viewed more than once
```

### Step 4: Refresh the Prometheus Configurations

Refresh the Prometheus configurations with your changes:

```bash
./prometheus --config.file=prometheus.yml
```

Make sure to replace `/home/prometheus-2.30.0.linux-amd64/alerting_rules.yml` with the actual path to your `alerting_rules.yml` file.

Your Prometheus should now be set up to send alerts to Alertmanager, which will, in turn, send them to your Slack channel using the webhook you configured.
