# Exercises

## 1. Make sure git remembers your login and password.
To make sure that Git remembers your login and password, you can configure Git to use a credential manager or cache your credentials. There are different approaches depending on your operating system and the credential management tools available.

***Set up Git credential caching:***
- In the terminal, run `git config --global credential.helper cache`.
<br />**NOTE:**By default, Git will cache your credentials for 15 minutes.
- You can adjust the cache timeout using the `--timeout`: `git config --global credential.helper 'cache --timeout=3600'`(adjust the time for your usage).

***Use a credential manager:***
- Git provides credential managers that integrate with the operating system's native credential management tools.
- Install and configure the appropriate credential manager for your operating system.
<br />**We will use `libsecret` or `gnome-keyring`:**
   - Install libsecret or gnome-keyring package depending on your distribution. 
   - Run the following command to enable libsecret or gnome-keyring as the credential helper:
     - For `libsecret`: `git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret`
     - For `gnome-keyring`: `git config --global credential.helper gnome-keyring`
   - **Configuring credential storage:**
     - If you're using a public Git server, you can configure Git to use HTTPS instead of the default SSH. HTTPS allows you to store your credentials securely and automatically.
     - Update your remote repository URLs from SSH to HTTPS:
       - From `git remote set-url origin git@github.com:username/repo.git` to `git remote set-url origin https://github.com/username/repo.git`

## 2. Set a new repository ‘test’ and create a file in it.
### a. Make a few commits with different versions of the file.
### b. Return to one of the previous versions of the file using the commit history.
### c. Present the difference between the versions using Git.
### d. Get the latest version of your file using Git commands.
Create a new repository named 'test':
  - Open terminal, navigate to the directory where you want to create the repo and run the next command in terminal: `git init test`.
  - This will create a new directory named `test` so move into it: `cd test`.
  - Create a new file: `touch file.txt` and you can use any text editor or run `echo "Version 1" > file.txt`.
  - Make a few commits with different versions of the file:
    - `git add file.txt`
    - `git commit -m "Initial version of file.txt"`
    - `echo "Version 2" > file.txt`
    - `git commit -am "Updated file.txt to version 2"`
  - Return to a previous version of the file using commit history:
    - `git log --oneline`
    - Identify the commit hash associated with the version you want to revert to.
    - Now to revert to a previous version, use `git checkout <commit_hash> -- file.txt`
  - See the difference between the versions using Git:
    - To see the differences between versions, you can use the git diff command.
    - `git diff HEAD^ file.txt`(This will display the changes made to the file.)
  - Get the latest version of your file using Git commands:
    - If you want to retrieve the latest version of your file, simply use the git checkout command without specifying a commit hash.
    - `git checkout -- file.txt`(This will restore the latest version of the file from the repository.)

