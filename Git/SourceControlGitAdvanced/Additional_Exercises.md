# Additional Exercises
***You are working on a team project to build a new website. Your team uses Git for version control. Your team leader has created a feature branch called feature-branch to work on a new feature for the website.***

## 1. Upload your weather-app project to a new project in your Gitlab instance in AWS. From the main branch create a new branch called `feature-change-bg-color`.
**To upload your weather-app project to a new project in your Gitlab instance in AWS, you can follow these steps:**
- Set up a new project in your Gitlab instance on AWS.
- Clone the `weather-app` project locally using the command: `git clone <repository_url>`.
- Navigate to the cloned project's directory using: `cd weather-app`.
- Add the Gitlab repository as a remote using: `git remote add origin <gitlab_repository_url>`.
- Create the new branch using: `git checkout -b feature-change-bg-color`
- Push the project to the Gitlab repository using: `git push`.

## 2. Create a new branch called `feature-changed-title` and switch to it.
To create a new branch called `feature-changed-title` and switch to it, you use the command: `git checkout -b feature-changed-title`.

## 3. Change the title of your front page, and Commit your changes to the `feature-changed-titie` branch.
Change the title of your front page and commit your changes to the `feature-changed-title` branch. 
<br />Assuming you have made the necessary changes, you can use the following commands:
- Stage the changes: `git add <file(s)>`.
- Commit the changes with a descriptive message: `git commit -m "Changed the title of the front page"`.

## 4. Switch back to the `feature-change-bg-color` , change the color of the background of your weather app, and commit your changes.
Switch back to the `feature-change-bg-color` branch, change the color of the background of your weather app, and commit your changes. 
<br/>Assuming you have made the necessary changes, you can use the following commands:
- Switch to the `feature-change-bg-color` branch: `git checkout feature-change-bg-color`.
- Make the required changes.
- Stage the changes: `git add <file(s)>`.
- Commit the changes with a descriptive message: `git commit -m "Changed the background color of the weather app"`.

## 5. Merge the `feature-changed-title` into the `feature-change-bg-color`.
To merge the `feature-changed-title` branch into the `feature-change-bg-color` branch, you use the following command:
`git merge feature-changed-title`
<br />*NOTE:* Make sure you are on the `feature-change-bg-color` branch before executing this command.

## 6. Create a new branch from the `feature-change-bg-color` called `oops-there-will-be-conflict` , and the same line of code in both branches.
To create a new branch from the `feature-change-bg-color` called `oops-there-will-be-conflict` and introduce a conflict, you follow these steps:
- Create the new branch: `git checkout -b oops-there-will-be-conflict`.
- Make changes to the same line of code as in the `feature-change-bg-color` branch, and commit your changes.

## 7. Attempt to merge the `oops-there-will-be-conflict` branch into the `feature-change-bg-color`.
Attempt to merge the `oops-there-will-be-conflict` branch into the `feature-change-bg-color` branch using the command:
- `git merge oops-there-will-be-conflict`
- This will result in a merge conflict.

## 8. Resolve the conflict by editing the conflicting files and deciding which changes to keep, then merge the two branches.
To resolve the conflict, you need to manually edit the conflicting files, choose which changes to keep, and then commit the changes. 
<br />***Follow these steps:***
- Open the conflicting file(s) in any text editor and resolve the conflicting sections.
- Once you have resolved the conflict, stage the changes: `git add <conflicted_file(s)>`.
- Commit the changes: `git commit -m "Resolved merge conflict"`.

## 9. Push the `feature-change-bg-color` to the remote repository.
To push the `feature-change-bg-color` branch to the remote repository, use: `git push origin feature-change-bg-color`.

## 10. Your team leader has reviewed your changes and decided that they want to apply your changes to the main branch. However, they want to keep the commit history clean and organized. Use `git rebase` to rebase the `feature-change-bg-color` onto the `main` branch.
To rebase the `feature-change-bg-color` branch onto the `main` branch, follow these steps:
- Switch to the `feature-change-bg-color` branch: `git checkout feature-change-bg-color`.
- Rebase the branch onto main: `git rebase main`.
- Resolve any conflicts that arise during the rebase process by editing the conflicting files, staging the changes, and continuing the rebase using: `git rebase --continue`.
- Repeat previous step for each conflict until the rebase is complete.
- Once the rebase is complete, push the updated branch to the remote repository using: `git push origin feature-change-bg-color`.

## 11. Create a new branch called `cherry-pick-branch`, and change your front page's title once again.
To create a new branch called `cherry-pick-branch` and change your front page's title once again, follow these steps:
- Create the new branch: `git checkout -b cherry-pick-branch`.
- Make the required changes to the front page's title.
- Stage the changes: `git add <file(s)>`.
- Commit the changes: `git commit -m "Changed the front page's title again"`.

## 12. Your team leader has also reviewed the changes you started to implement in the `cherry-pick-branch`, but only wants to apply one specific commit from that branch to the `main` branch. Only apply the commit you made previously to the `main` branch.
To cherry-pick only one specific commit from the `cherry-pick-branch` to the main branch, use the command:

`git cherry-pick <commit_hash>`

Replace `<commit_hash>` with the actual commit hash of the commit you want to apply to the main branch. This will apply the specific commit to the main branch while keeping the commit history clean and organized.

## 13. Now how can you check the integrity of your repository ?
***To check the integrity of your repository, you can use various Git commands:***
- Check the status of your repository: `git status`. This will show any uncommitted changes or untracked files.
- Verify the commit history: `git log`. This will display the commit history with commit messages, authors, dates, and commit hashes.
- Perform a repository-wide integrity check: `git fsck`. This command verifies the connectivity and integrity of the objects in your repository.
Ensure the working tree is clean: `git diff --exit-code`. If this command produces no output, it means there are no uncommitted changes in the repository.
- Validate the repository's structure: `git fsck --full`. This command performs a more comprehensive check of the repository's structure and objects.

These commands can help you ensure that your repository is in a consistent state and there are no issues with the integrity of the repository.

