
1. connect to the jenkins-slave instance :
a. Add the Jenkins agent user to the 'docker' group:
```
sudo usermod -aG docker jenkins-slave
```
After running this command, you might need to restart the Jenkins agent to apply the changes.

b. Give the 'jenkins-slave' user explicit permissions to the Docker daemon socket:
```
sudo chmod 666 /var/run/docker.sock
```
Keep in mind that granting all permissions (666) to the Docker socket might have security implications. Consider a more restrictive approach if security is a concern.

2. change the webhook in gitlab to the new jenkins public ip

