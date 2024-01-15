:'
grant read and write permissions to the directory
'
chmod -R 777 /home/parallels/roy.bidani/Devops/SystemSotrage/SharedFolder
:'
Install and configure Samba, which allows for file sharing with Windows systems
'
sudo apt-get install samba
:'
Edit the Samba configuration file by running the following command:
'
sudo nano /etc/samba/smb.conf
:'
Scroll to the bottom of the file and add the following lines:
'
[Shared]
path = /home/parallels/roy.bidani/Devops/SystemSotrage/SharedFolder
writable = yes
guest ok = yes
guest only = yes
create mask = 0777
directory mask = 0777
force user = roy

:'
Create a Samba user and set a password for them:

Run the following command to create a Samba user:
'
sudo smbpasswd -a username
:'
Restart the Samba service to apply the changes:
'
sudo service smbd restart

:'
to connect:
via termina
'
gio mount smb://IP_address/shared
:'
via file system:
'
other location -> smb://IP_address/shared
