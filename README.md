# ACCESS Recommender
## Running the application
1. Pull down the repo in your home directory: ```git clone <URL>```
2. Run ```source setup.sh```
3. Run the app with  ```flask run``` or ```python3 -m flask run```

## Developing
1. Follow the above steps to set up your application
2. Pick an issue from the Issues tab on GitHub (on the right where it says Assignees)
3. Assign yourself to that issue
4. Make sure you are on the flask-app branch (```git branch``` use ```git checkout <branch-name>``` to switch branches)
5. Pull from GitHub to make sure your local files are up to date (```git pull```)
6. From the flask-app branch, Create a new branch ( ```git checkout -b issue-<#>-<descriptor>)
    This is the branch where you will make the changes to resolve the Issue
4. Once the issue is resolved, create a pull request from your branch to the flask-app branch.
8. **Never** Push to the main (flask-app) branch. Others will be pulling from that branch and unfinished
    code will lead to errors for them as well
9. We will review Pull Requests (PRs) together and merge them to the flask-app branch or suggest changes

**TODO:**
See the issues on GitHub for TODO items
