

```markdown
# Step 1 — Installing the Dependencies

Before installing GitLab, it is important to install the software that it leverages during installation and on an ongoing basis. The required software can be installed from Ubuntu’s default package repositories.

First, refresh the local package index:

```bash
sudo apt update
```

Then install the dependencies by entering this command:

```bash
sudo apt install ca-certificates curl openssh-server postfix tzdata perl
```

You will likely have some of this software installed already. For the postfix installation, select "Internet Site" when prompted. On the next screen, enter your server’s domain name to configure how the system will send mail.

Now that you have the dependencies installed, you’re ready to install GitLab.

# Step 2 — Installing GitLab

With the dependencies in place, you can install GitLab. This process leverages an installation script to configure your system with the GitLab repositories.

First, move into the `/tmp` directory:

```bash
cd /tmp
```

Then download the installation script:

```bash
curl -LO https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh
```

Feel free to examine the downloaded script to ensure that you are comfortable with the actions it will take. You can also find a hosted version of the script on the GitLab installation instructions:

```bash
less /tmp/script.deb.sh
```

Once you are satisfied with the safety of the script, run the installer:

```bash
sudo bash /tmp/script.deb.sh
```

The script sets up your server to use the GitLab maintained repositories. This lets you manage GitLab with the same package management tools you use for your other system packages. Once this is complete, you can install the actual GitLab application with apt:

```bash
sudo apt install gitlab-ce
```

This installs the necessary components on your system and may take some time to complete.

# Step 3 — Adjusting the Firewall Rules

Before you configure GitLab, you need to ensure that your firewall rules are permissive enough to allow web traffic. If you followed the guide linked in the prerequisites, you will already have a ufw firewall enabled.

View the current status of your active firewall by running:

```bash
sudo ufw status
```

```
Output
Status: active

To             Action   From
--             ------   ----
OpenSSH        ALLOW    Anywhere                  
OpenSSH (v6)   ALLOW    Anywhere (v6)
```

The current rules allow SSH traffic through, but access to other services is restricted. Since GitLab is a web application, you need to allow HTTP access. Because you will be taking advantage of GitLab’s ability to request and enable a free TLS/SSL certificate from Let’s Encrypt, also allow HTTPS access.

The protocol to port mapping for HTTP and HTTPS are available in the `/etc/services` file, so you can allow that traffic in by name. If you didn’t already have OpenSSH traffic enabled, you should allow that traffic:

```bash
sudo ufw allow http
sudo ufw allow https
sudo ufw allow OpenSSH
```

You can check the ufw status again to ensure that you granted access to at least these two services:

```bash
sudo ufw status
```

```
Output
Status: active

To             Action   From
--             ------   ----
OpenSSH        ALLOW    Anywhere                  
80/tcp         ALLOW    Anywhere                  
443/tcp        ALLOW    Anywhere                  
OpenSSH (v6)   ALLOW    Anywhere (v6)             
80/tcp (v6)    ALLOW    Anywhere (v6)             
443/tcp (v6)   ALLOW    Anywhere (v6)
```

This output indicates that the GitLab web interface is now accessible once you configure the application.

# Step 4 — Editing the GitLab Configuration File

Before you can use the application, update the configuration file and run a reconfiguration command. First, open GitLab’s configuration file with your preferred text editor. This example uses nano:

```bash
sudo nano /etc/gitlab/gitlab.rb
```

Search for the `external_url` configuration line. Update it to match your domain and make sure to change `http` to `https` to automatically redirect users to the site protected by the Let’s Encrypt certificate:

```plaintext
/etc/gitlab/gitlab.rb
...
## GitLab URL
##! URL on which GitLab will be reachable.
##! For more details on configuring external_url see:
##! https://docs.gitlab.com/omnibus/settings/configuration.html#configuring-the-external-url-for-gitlab
##!
##! Note: During installation/upgrades, the value of the environment variable
##! EXTERNAL_URL will be used to populate/replace this value.
##! On AWS EC2 instances, we also attempt to fetch the public hostname/IP
##! address from AWS. For more details, see:
##! https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html
external_url 'https://your_domain'
...
```

Next, find the `letsencrypt['contact_emails']` setting. If you’re using nano, you can enable a search prompt by pressing CTRL+W. Write `letsencrypt['contact_emails']` into the prompt, then press ENTER. This setting defines a list of email addresses that the Let’s Encrypt project can use to contact you if there are problems with your domain. It’s recommended to uncomment and fill this out to inform yourself of any issues that may occur:

```plaintext
/etc/gitlab/gitlab.rb
letsencrypt['contact_emails'] = ['sammy@example.com']
```

Once you’re done making changes, save and close the file. If you’re using nano, you can do this by pressing CTRL+X, then Y, then ENTER.

Run the following command to reconfigure GitLab:

```bash
sudo gitlab-ctl reconfigure
```

This will initialize GitLab using the information it can find about your server. This is a completely automated process, so you will not have to answer any prompts. The process will also configure a Let’s Encrypt certificate for your domain.

# Step 5 — Performing Initial Configuration Through the Web Interface

With GitLab running, you can perform an initial configuration of the application through the web interface.

## Logging In for the First Time

Visit the domain name of your GitLab server in your web browser:

```
https://your_domain
```

On your first visit, you’ll be greeted with a login page:


On your first visit, sign as ‘root’.

GitLab generates an initial secure password for you. It is stored in a folder that you can access as an administrative sudo user:

```bash
sudo nano /etc/gitlab/initial_root_password
```

```plaintext
/etc/gitlab/initial_root_password
# WARNING: This value is valid only in the following conditions
#          1. If provided manually (either via `GITLAB_ROOT_PASSWORD` environment variable or via `gitlab_rails['initial_root_password']` setting in `gitlab.rb`, it was provided before database was seeded for the firs$
#          2. Password hasn't been changed manually, either via UI or via command line.
#
#          If the

password shown here doesn't work, you must reset the admin password following [this guide](https://docs.gitlab.com/ee/security/reset_user_password.html#reset-your-root-password).

Password: YOUR_PASSWORD

# NOTE: This file will be automatically deleted in the first reconfigure run after 24 hours.

Back on the login page, enter the following:

Username: root
Password: [the password listed on `/etc/gitlab/initial_root_password`]

Enter these values into the fields and click the "Sign in" button. You will be signed in to the application and taken to a landing page that prompts you to begin adding projects:

![Your GitLab dashboard after logging in as root](image-link)

You can now fine-tune your GitLab instance.

## Updating Your Password

One of the first things you should do after logging in is change your password. To make this change, click on the icon in the upper-right corner of the navigation bar and select "Edit Profile":

![Click on the user icon and select 'Edit Profile' to enter the Settings page](image-link)

You'll then enter a User Settings page. On the left navigation bar, select "Password" to change your GitLab-generated password to a secure password. Then click on the "Save password" button when you’re finished with your updates:

![The Password setting is in the left navigation bar. You can update your password from here.](image-link)

You'll be taken back to the login screen with a notification that your password has been changed. Enter your new password to log back into your GitLab instance:

![After changing your password, you'll be asked to log back in with your updated password.](image-link)

## Adjusting your Profile Settings

GitLab selects some reasonable defaults, but these are not usually appropriate once you start using the software.

To make the necessary modifications, click on the user icon in the upper-right corner of the navigation bar and select "Edit Profile".

You can adjust the Name and Email address from "Administrator" and "admin@example.com" to something more accurate. The name you select will be displayed to other users, while the email will be used for default avatar detection, notifications, Git actions through the interface, and more:

![Update your Name and Email within the Edit Profile settings](image-link)

Click on the "Update Profile settings" button at the bottom when you are finished with your updates. You'll be prompted to enter your password to confirm changes.

A confirmation email will be sent to the address you provided. Follow the instructions in the email to confirm your account so that you can begin using it with GitLab.

## Changing Your Account Name

Next, select "Account" in the left navigation bar:

![GitLab Account selection in the left navigation bar](image-link)

Here, you can enable two-factor authentication and change your username. By default, the first administrative account is given the name root. Since this is a known account name, it is more secure to change this to a different name. You will still have administrative privileges; the only thing that will change is the name. Replace "root" with your preferred username:

![Change your username from 'root' into something you prefer.](image-link)

Click on the "Update username" button to make the change. You'll be prompted to confirm the change thereafter.

Next time you log into GitLab, remember to use your new username.
```

Please note that the markdown file format does not support displaying images directly within the document. You would need to replace the "image-link" placeholders with the actual URLs of the images you want to display.
