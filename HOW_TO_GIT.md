# How to correctly use the git repository
## How to work on your own part
### 1. Create your own branch to work on your dedicated task (only one branch for multiple people working on the same task)
```bash
git branch <your_branch_name>
```
### 2. Set your new branch as the current working branch
```bash
git checkout <you_branch_name>
```
To see the status of your branch at any time, you can use :
````bash
git status
````
### 3. You can now freely work and commit your modification on your local branch
````bash
git commit -m "<description of your commit>"
````
### 4. Creating the branch on the remote repository and setting your local repository to track this branch
```bash
git push -u origin <you_branch_name>
```
### 5. Pushing new modification on your remote branch
````bash
git push
````
### 6. Pulling eventual modifications made on the branch by colleagues
````bash
git pull
````

## How to Merge Your Branch with the Main Branch

When you decide that your task is finished and your code as been tested, you may want to add your modifications to the main branch.
However, you have to follow strictly the following steps to avoid creating any conflict on the main branch.

### 1. Synchronize your local `main` branch with the remote version

```bash
git checkout main
git pull
```

### 2. Switch to your branch

```bash
git checkout <your_branch_name>
```

### 3. Commit and push your progress on this branch
This step is already described in the first part of this document.

### 5. Merge the `main` branch into your branch

```bash
git merge main
```

### 6. Handle conflicts (if any)

- Resolve the conflicts.
- Commit the changes made to resolve conflicts on your branch.

### 7. Verify if anything new has been added to the `main` branch

```bash
git checkout main
git pull
```
- If the `main` branch has changed, repeat from step 2.

### 8. Push the merging changes on your remote repository
````bash
git checkout <your_branch_name>
git push
````

### 9. Merge your branch into the `main` branch
Two methods are available for this last step, one using the website Github and anothe rusing the CLI. Choose the one that suits you the most.
#### - First option -> Website : Opening a pull request that has to be accepted on the Github
a. Go to the website git repository on Github.

b. Open the "Pull requests" tab

c. Click on "Create pull request"

d. Choose "main" as base and <you_branch_name> as compare

e. Proceed to the opening of the pull request

f. Notify your teammates that they have to review your pull request and accept it if they are ok with it OR accept yourself the request if you know what you are doing and that everyone is ok with it

#### - Second Option -> CLI : Directly push from your local repository
```bash
git checkout main
git merge <your_branch_name>
git push
```

I hope that it helped you mates ;)
