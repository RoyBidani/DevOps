# Configuring Load Balancer for Weather App Instances

This guide will walk you through the process of duplicating an existing instance of the Weather App and setting up a Load Balancer to distribute incoming traffic between two application servers.

## Table of Contents

1. [Create an Image of the Weather App Instance](#create-an-image-of-the-weather-app-instance)
2. [Launch a New Instance from the Image](#launch-a-new-instance-from-the-image)
3. [Create an Application Load Balancer (ALB)](#create-an-application-load-balancer-alb)
4. [Save the Configuration](#save-the-configuration)

## 1. Create an Image of the Weather App Instance

- Go to the AWS Management Console and navigate to the EC2 service.
- Locate and select the existing Weather App instance that you want to duplicate.
- From the "Actions" menu, choose "Create Image."
- Provide a name and description for the image, and click "Create Image."
- Wait for the image creation process to complete.

## 2. Launch a New Instance from the Image

- In the AWS Management Console, go to the EC2 service.
- Under "Images," select "AMIs" and find the image you created in the previous step.
- Choose "Launch Instance" and follow the instance launch wizard.
- Select the instance type, configure instance details, add storage, configure security groups, and review the instance settings.
- Click "Launch" to launch the new instance.

## 3. Create an Application Load Balancer (ALB)

- In the AWS Management Console, navigate to the EC2 service.
- In the left menu, under "Load Balancing," select "Load Balancers."
- Click "Create Load Balancer" and choose "Application Load Balancer."
- Configure the ALB settings:
  - Provide a name for the load balancer.
  - Define the listener ports and protocols (e.g., HTTP on port 80 and HTTPS on port 443).
  - Specify the security groups for the load balancer.
  - Select the availability zones where the instances will be placed.
- In the "Listeners and routing" section, choose the target group that includes the instances you want to load balance.
- Ensure you select port 443 and use the .pem certificate files for HTTPS.
- Click "Next: Configure Security Settings" and proceed to the next steps.

***Note: Make sure the listener and target groups are configured on the same ports for proper routing.***

## 4. Save the Configuration

- After configuring the routing rules, click "Next: Review."
- Review all the settings and configurations you have made.
- If everything looks correct, click "Create" to create the ALB and apply the routing rules.
- Wait for the ALB creation process to complete.

Once the ALB is created and the routing rules are set up, incoming traffic to the load balancer will be distributed to the instances based on the defined routing rules. This will provide high availability and improved performance for your Weather App by distributing the load across multiple application servers.
