a.
sudo useradd labuser1
sudo passwd labuser1
sudo mkdir /labusers_home
sudo usermod -d /labusers_home labuser1		// specifies the new home directory for the user


b.
sudo adduser --home /labusers_home labuser2	// performing all actions in single command


***
cut -d: -f1 /etc/passwd		// view the list of all users





