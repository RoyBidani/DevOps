# Deploying Python Web Application on AWS Elastic Beanstalk

## Table of Contents

1. [Create requirements.txt](#create-requirements.txt)
2. [Create Virtual Environment](#create-virtual-environment)
3. [Install Requirements and Run the App](#install-requirements-and-run-the-app)
4. [Freeze Dependencies to requirements.txt](#freeze-dependencies-to-requirements.txt)
5. [Create Procfile](#create-procfile)
6. [Prepare App Directory](#prepare-app-directory)
7. [Create IAM Role](#create-iam-role)
8. [Create AWS Elastic Beanstalk Environment](#create-aws-elastic-beanstalk-environment)
9. [Wait for Environment Creation](#wait-for-environment-creation)
10. [Access the Web App](#access-the-web-app)

---

## Create requirements.txt

1. Create a file named `requirements.txt` and include the necessary dependencies (based on the imports in your code):

```plaintext
Flask==2.0.1
requests==2.26.0
boto3==1.18.14
```

## Create Virtual Environment

2. In your app directory, create a virtual environment:

```bash
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv myenv 
source myenv/bin/activate
```

## Install Requirements and Run the App

3. Install the requirements inside the virtual environment and run the app:

```bash
pip install -r requirements.txt
python3 app.py
```

Ensure that the app runs as expected.

## Freeze Dependencies to requirements.txt

4. After verifying that everything works, check the dependencies to insert them into `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## Create Procfile

5. Create a file named `Procfile` (without any extension) in your app directory:

```plaintext
web: gunicorn --bind 0.0.0.0:8000 app:app
```

## Prepare App Directory

6. Make sure you have all the necessary files inside the app directory:
   - `app.py`
   - `/templates` (if using Flask templates)
   - `/static` (if using static files)
   - `requirements.txt`
   - `Procfile`

Zip all these files together.

## Create IAM Role

7. In AWS IAM, create a new role with the policy "AWSElasticBeanstalkWebTier."

## Create AWS Elastic Beanstalk Environment

8. Go to AWS Elastic Beanstalk and create a new environment:
   - Environment tier -> Web server environment
   - Name the environment
   - Platform -> Python 3.9
   - Application code -> Upload your code
   - Check 'Local file' and upload the `.zip` file containing your app.
   - Click 'Next'

## Configure Environment Settings

9. Configure the following settings for the environment:
   - Service access -> Service role -> Use an existing service role (Select the IAM role from Step 7)
   - Choose your EC2 key pair
   - At EC2 instance profile, choose the Rule created in Step 7.
   - Click 'Next'
   - Virtual Private Cloud (VPC) -> Choose your VPC
   - Instance settings -> Check "Public IP address" -> Activated
   - Instance subnets -> Choose the desired subnet
   - Click 'Next'
   - EC2 security groups -> Check the desired security group
   - Click 'Next' and then click 'Submit'

## Wait for Environment Creation

10. Wait until the environment is created.

## Access the Web App

11. Once the environment creation is complete, you will be able to access the web app through the URL provided by AWS Elastic Beanstalk. The instance created for the app will handle incoming requests and serve the application.
