
# Ansible Usage Guide

This guide provides step-by-step instructions for using Ansible to manage an AWS EC2 Ubuntu server instance. It covers essential tasks, such as installing Ansible, configuring AWS credentials, connecting to instances, and executing commands remotely.

## Table of Contents

1. [Install Ansible](#1-install-ansible)
2. [Configure Ansible to Manage an AWS EC2 Instance](#2-configure-ansible-to-manage-an-aws-ec2-instance)
3. [Set Up Control Node to Access VM](#3-set-up-control-node-to-access-vm)
4. [Run Ad Hoc Command to Log Node Configuration](#4-run-an-ad-hoc-command-that-logs-your-successful-node-configuration)
5. [Copy Files to Managed Nodes](#5-copy-a-file-to-each-of-the-managed-nodes-using-an-ad-hoc-command)
6. [Create a New User on Managed Nodes](#6-create-a-new-user-on-each-of-the-managed-nodes-using-an-ad-hoc-command)
7. [Write Your First Playbook](#7-write-your-first-playbook)
8. [Deploy Your Python Web Application](#8-write-a-playbook-that-deploys-your-python-web-application)
9. [Run a Docker Container](#9-write-a-playbook-that-runs-a-docker-container)

---

## 1. Install Ansible

To install Ansible, use a package manager or a virtual environment. Here's one way to do it using a package manager:

```bash
sudo apt update
sudo apt install ansible
```

## 2. Configure Ansible to Manage an AWS EC2 Instance

1. Set up an AWS EC2 instance named "Control Node."
2. Install Ansible on your control node.
3. Configure your AWS credentials using an AWS credentials file:

   a. Create the AWS credentials file:
      ```bash
      mkdir ~/.aws
      nano ~/.aws/credentials
      ```

   b. Add your credentials to the file:
      ```ini
      [default]
      aws_access_key_id = YOUR_ACCESS_KEY
      aws_secret_access_key = YOUR_SECRET_KEY
      ```

4. Create an Ansible inventory file (`inventory.ini`) with your EC2 instance's IP address:
   ```ini
   nano inventory.ini
   [ec2]
   YOUR_EC2_INSTANCE_IP ansible_ssh_user=ubuntu ansible_ssh_private_key_file=/path/to/your/private/key.pem
   ```
   Replace placeholders with actual values.

5. Confirm Private Key Corresponds to Public Key:
   On your local machine, generate the public key from the private key:
   ```bash
   ssh-keygen -y -f /path/to/your/private/key.pem > /path/to/your/public/key.pub
   ```
   Add the content of `public/key.pub` to `~/.ssh/authorized_keys` on the remote host.

6. Test Ansible's connection to your EC2 instance:
   ```bash
   ansible -i inventory.ini ec2 -m ping
   ```

## 3. Set Up Control Node to Access VM

Edit `/etc/hosts` on the control node to map the VM's IP address to a hostname.

## 4. Run an Ad Hoc Command to Log Node Configuration

Run this command to log successful node configuration:
```bash
ansible all -i inventory.ini -m shell -a "echo 'Node configuration successful' | sudo tee -a /var/log/syslog"
```

## 5. Copy Files to Managed Nodes

Copy a file to managed nodes using the `copy` module:
```bash
ansible all -i inventory.ini -m copy -a "src=/local/path dest=/remote/path"
```

## 6. Create a New User on Managed Nodes

Create a new user on managed nodes using the `user` module:
```bash
ansible all -i inventory.ini -m user -a "name=newusername state=present" -b
```

## 7. Write Your First Playbook

Create a YAML file (`my_first_playbook.yml`) to stop a service and install NGINX:
```yaml
---
- name: My First Playbook
  hosts: ec2
  tasks:
    - name: Stop printer.target service
      systemd:
        name: printer.target
        state: stopped

    - name: Install NGINX
      apt:
        name: nginx
        state: latest
```
Run the playbook:
```bash
ansible-playbook -i inventory.ini my_first_playbook.yml -b
```

## 8. Deploy Your Python Web Application

Create a playbook (`deploy_app.yml`) to copy files and install dependencies:
```yaml
---
- name: Deploy Python Web App
  hosts: ec2
  tasks:
    - name: Copy application files
      copy:
        src: /local/path/to/app
        dest: /remote/path/to/app

    - name: Install application dependencies
      pip:
        requirements: /remote/path/to/app/requirements.txt
```
Run the playbook:
```bash
ansible-playbook -i inventory.ini deploy_app.yml -b
```

## 9. Run a Docker Container

Create a playbook (`run_docker_container.yml`) to install Docker and run a container:
```yaml
---
- name: Run Docker Container
  hosts: ec2
  tasks:
    - name: Install Docker dependencies
      apt:
        name: ['docker.io', 'python3-docker']
        state: latest

    - name: Start Docker service
      systemd:
        name: docker
        enabled: yes
        state: started

    - name: Pull Docker image
      docker_image:
        name: your_image_name
        source: pull

    - name: Run Docker container
      docker_container:
        name: my_container
        image: your_image_name
```
Run the playbook:
```bash
ansible-playbook -i inventory.ini run_docker_container.yml -b
```

By following these steps, you'll be able to effectively manage your AWS EC2 instances using Ansible for various tasks.
