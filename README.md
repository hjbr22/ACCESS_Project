# ACCESS Recommender
## Running the application
1. Pull down the repo in your home directory: ```git clone <URL>```
2. Run ```source setup.sh``` (you must have virtualenv installed)
3. Run the app with  ```flask run``` or ```python3 -m flask run```

## Developing
1. Follow the above steps to set up your application
2. Pick an issue from the Issues tab on GitHub 
3. Assign yourself to that issue (on the right where it says Assignees)
4. Make sure you are on the flask-app branch (```git branch``` use ```git checkout <branch-name>``` to switch branches)
5. Pull from GitHub to make sure your local files are up to date (```git pull```)
6. From the flask-app branch, Create a new branch ( ```git checkout -b issue-<#>-<descriptor>```)
    This is the branch where you will make the changes to resolve the Issue
7. Once the issue is resolved and everything is pushed, create a pull request from your branch to the flask-app branch on the GitHub website.
8. **Never** Push to the main (flask-app) branch. Others will be pulling from that branch and unfinished
    code will lead to errors for them as well
9. We will review Pull Requests (PRs) together and merge them to the flask-app branch or suggest changes

## Database
- If you make any changes to the database or the models file, make sure you make the appropriate changes in the
    ```reset_database.py``` file as well. (If you add a new column to the RPS table, 
    make sure to add some data for that column in the ```reset_database.py``` file as well)
- If you want to reset the database at any point, run ```python3 reset_database.py```.
    Doing this will drop and recreate all tables and populate them with some sample data.

## Getting Modules
- To get a list of the available modules on an HPC run `module avail`
- To capture that output into a file, (first make sure you are in your scratch or work space)
    run  `module avail &> <file-name>.txt` (replace `file-name` with a descriptive name)
- To parse through that data and get only the software and version, pass the file to the `get_modules_and_versions` function
    in the `parse_modules` file in this repo.

**TODO:**
See the issues on GitHub for TODO items
