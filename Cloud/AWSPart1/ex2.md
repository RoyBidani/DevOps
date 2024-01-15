1)
```
#!/bin/bash
#Set the region where your EC2 instances are located
REGION="eu-west-3"

#Get the instance IDs of all running EC2 instances
INSTANCE_IDS=$(aws ec2 describe-instances --region $REGION --filters "Name=instance-state-name,Values=running" --que$

#Shut down the EC2 instances
if [[ -n "$INSTANCE_IDS" ]]; then
  echo "Shutting down EC2 instances: $INSTANCE_IDS"
  aws ec2 stop-instances --region $REGION --instance-ids $INSTANCE_IDS
else
  echo "No running EC2 instances found"
fi

```



2) IAM policy that only allows to find and stop EC2
Go to IAM, select Policies and create a new IAM Policy, click on Create policy.

Now you can create your own policy or use the one I created stop_ec2. Just switch to JSON and paste the code below.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeRegions",
                "ec2:StopInstances",
                "ec2:DescribeInstanceStatus"
            ],
            "Resource": "*"
        }
    ]
}

```


3) IAM role with minimal privileges
Now you can create an IAM Role. Go to IAM, select Roles. Create a new IAM Role, click Create roles, and then select Lambda.


Add the policy you created earlier and move on. Now, you can add a name such as stop_ec2, a description to the role and click Create role.



4) Lambda function
Now we move on to create Lambda Functions. From the services, select Lambda and click Create function.


I create a lambda function using Python 3.10 and name it stop_ec2.

Very important! Remember to change the Execution role to the role you created in the previous section. In my case it is stop_ec2. You add the policy to the role, and you add the role to the function, it’s so simple 
AWS Lambda from scratch



The function is very simple, it is supposed to find all EC2s in a given account, in all regions. If it finds an EC2 it prints out their id and state. All machines that have a state equal to running will be automatically stopped.


```
import boto3 
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

def lambda_handler(event, context):
    for region in regions:
        ec2_client = boto3.client('ec2', region)
        all_instances = ec2_client.describe_instances()
        if all_instances:
            print("List all instances:")
            for reservation in all_instances['Reservations']:
                for instance in reservation['Instances']:
                    print(instance['InstanceId'] + "-" + instance['State']['Name'])
                    
                    if instance['State']['Name'] == 'running':
                        print("Stopping ec2: " + instance['InstanceId'])
                        ec2_client.stop_instances(InstanceIds=[instance['InstanceId']])
```




5) Cloud Watch Event
Once you’ve created your function and verified that it works properly, then you can automate its triggering, for example, by adding a CloudWatch Event. This allows you to run the function at a specific time. 

All you have to do is click Add Trigger, select CloudWatch Events from the list, add a name and description.
I like to use cron expressions, but you don’t have to. My function will run every day at one o’clock in the morning.


AWS Lambda – add trigger

