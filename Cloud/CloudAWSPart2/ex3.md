# Adding Feature Button to Weather Website and Automating Backups with AWS Lambda

## Table of Contents

1. [Adding a Feature Button](#adding-a-feature-button)
   - Step 1: Create a DynamoDB Table
   - Step 2: Modify Weather Template
   - Step 3: Implement the DynamoDB API Endpoint

2. [Automating Backups with AWS Lambda](#automating-backups-with-aws-lambda)
   - Step 1: Create an AWS Lambda Function
   - Step 2: Update the IAM Policy
   - Step 3: Write the Lambda Function Code
   - Step 4: Set Up a Trigger for the Lambda Function

---

## Adding a Feature Button

To enhance your weather website, follow these steps to add a feature button that allows users to store weather data to DynamoDB.

### Step 1: Create a DynamoDB Table

1. Go to the AWS Management Console and navigate to DynamoDB.
2. Click on "Create table" and provide a table name, e.g., "WeatherDB."
3. Set the primary key, such as "location," to uniquely identify each item in the table.
4. Click "Create" to create the DynamoDB table.

### Step 2: Modify Weather Template

1. Update your weather.html template to include a new feature button to store data to DynamoDB.
2. Use a form with an action to the API endpoint `/api/store-to-dynamodb` and a hidden input field to store the location value.

```html
<form action="/api/store-to-dynamodb" method="post">
    <input type="hidden" name="location" value="{{ location }}">
    <button type="submit">Store Data to DynamoDB</button>
</form>
```

### Step 3: Implement the DynamoDB API Endpoint

1. Update your app.py file to include a new API endpoint `/api/store-to-dynamodb`.
2. Handle the data storage by fetching the weather data from the form, serializing it to JSON, and storing it in DynamoDB using the boto3 library.

```python
@app.route('/api/store-to-dynamodb', methods=['POST'])
def store_to_dynamodb():
    # Get weather data from the form
    location = request.form['location']
    weather_info = Api.get_weather(location)

    # Serialize the weather_info list to a JSON string
    weather_info_json = json.dumps(weather_info)

    # Store weather data in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table_name = 'WeatherDB'
    table = dynamodb.Table(table_name)
    table.put_item(Item={'location': location, 'weather': weather_info_json})

    # Render the page again
    return render_template('weather.html', location=location, weather_info=weather_info)
```

---

## Automating Backups with AWS Lambda

To automate backups of weather data, you can set up an AWS Lambda function. Follow these steps to accomplish it.

### Step 1: Create an AWS Lambda Function

1. Go to the AWS Management Console and navigate to Lambda.
2. Click on "Create function" and choose "Author from scratch."
3. Enter a name for your function (e.g., "WeatherDataBackup") and choose "Python" as the runtime.
4. Set up permissions by choosing an existing role with DynamoDB write access or create a new role with the required permissions.
5. Click "Create function" to create the Lambda function.

### Step 2: Update the IAM Policy

To allow the Lambda function to write data to DynamoDB, you need to update the IAM policy for the Lambda function's execution role. Follow these steps:

1. Go to the AWS Management Console and navigate to the IAM service.
2. In the left-hand menu, click on "Roles" and find the role named "WeatherBackup-role-m98orqes" (the role mentioned in the error message).
3. Click on the role to view its details.
4. Scroll down to the "Permissions" section and click on the "Attach policies" button.
5. In the search box, type "AmazonDynamoDBFullAccess" and select the policy named "AmazonDynamoDBFullAccess."
6. Click on the "Attach policy" button to attach the selected policy to the role.

### Step 3: Write the Lambda Function Code

In the Lambda function, use the boto3 library to fetch the weather data for Tel Aviv. Serialize the weather data to JSON and store it in the DynamoDB table created earlier.

```python
    import json
import urllib.request
import boto3

def lambda_handler(event, context):
    key = '3407b726ce32e0fdd2588dc7b3058dd3'
    cnt = 56
    location = "tel%20aviv"
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&cnt={cnt}&APPID={key}'

    # Make the API call using urllib
    with urllib.request.urlopen(url) as response:
        weather = json.loads(response.read())

    weather_info = []
    if weather.get('cod') == '404':
        weather_info.append({'cod': weather.get('cod')})
        return weather_info
    elif weather.get('cod') == '200':
        cod = weather.get('cod')
        day = None
        night = None
        country = weather['city']['country']
        for item in weather['list']:
            dt = item['dt_txt']
            date = dt.split(' ')[0]
            time = dt.split(' ')[1]
            humidity = item['main']['humidity']
            temp = int(item['main']['temp'] - 273.15)
            if time == '12:00:00':
                day = temp
            elif time == '21:00:00':
                night = temp
                weather_info.append({'cod': cod, 'date': date, 'day_temp': day, 'night_temp': night, 'humidity': humidity})
                day = None
                night = None

    # Serialize the weather_info list to a JSON string
    weather_info_json = json.dumps(weather_info)

    # Store weather data in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table_name = 'WeatherDB'
    table = dynamodb.Table(table_name)
    table.put_item(Item={'location': location, 'weather': weather_info_json})
```

### Step 4: Set Up a Trigger for the Lambda Function

1. Go to the AWS Management Console and navigate to CloudWatch.
2. Under "Events," click on "Rules" and then click "Create rule."
3. Choose "Event Source" as "Schedule."
4. Set the schedule expression to `cron(0 18 * * ? *)` to trigger the function daily at 18:00 UTC.
5. For the target, select "Lambda function" and choose the Lambda function created in Step 1.
6. Click "Create rule" to set up the trigger.

With this setup, the Lambda function will run automatically every day at 18:00 UTC, fetch the weather data for Tel Aviv, and store it in DynamoDB. This ensures daily automated backups of weather data.
