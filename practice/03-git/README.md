# Git & GitHub


## Setting up and Managing Repositories

Read [git in Data Science](https://uvads.github.io/git-basics/) for a brief introduction.

Then work through the [Creating and Managing Git Repositories Exercises](https://uvads.github.io/git-basics/docs/creating-repositories/). These exercises will cover:

* Init
* Fork (should be familiar from [Setup Instructions](../../setup/))
* Delete
* Managing Collaborators 

## Basic Commands

Work through the [Basic Commands](https://uvads.github.io/git-basics/). These exercises will familiarize you with:

* git diff
* git status
* git add
* git commit
* git push / pull
* git fetch
* git log

## Group activity

At your table, select one person to set up a new repository on GitHub. Work through these steps:

1. **Repository Setup:**
   * The creator adds all group members as collaborators to the new repository on GitHub. The repository should have a single `main` branch.

2. **Clone the Repository:**
   * All group members should clone the new repository to their own environment:
     ```bash
     git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
     cd REPO_NAME
     ```
   **Important:** Make sure you are **not** inside an existing Git repository when running the `git clone` command. You don't want to create nested Git repositories.

3. **Create Unique Files:**
   * Each group member should create a new text file in their local repository. Use unique filenames to avoid collisions (e.g., `alice.txt`, `bob.txt`). Each team member should commit and push their files to the GitHub repository:
     ```bash
     echo "Hello from Alice" > alice.txt
     git add alice.txt
     git commit -m "Add alice.txt"
     git push origin main
     ```

4. **Verify on GitHub:**
   * All: Check the presence of the new files on GitHub by visiting the repository page.

5. **Pull Latest Changes:**
   * All: Run the following command in your environment to get the latest changes from GitHub:
     ```bash
     git pull origin main --merge
     ```
     (The `--merge` flag is explicit and avoids warnings in newer Git versions.)

6. **Create Collision File:**
   * All: Create a new file `collision.txt` in your local repository. The file should contain a single line with your `first name, favorite animal`:
     ```bash
     echo "Alice, cat" > collision.txt
     git add collision.txt
     git commit -m "Add collision.txt"
     git push origin main
     ```

### Resolving Merge Conflicts:

**The early bird gets the worm:** If you are the first person to push the `collision.txt` file, you're in luck—the push should go through without a hitch. However, the others will encounter an error message like this:

```bash
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/YOUR_USERNAME/REPO_NAME.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
```

**To resolve the conflict:**

Starting with the group member next to the first person who successfully pushed, go clockwise and perform the following steps:

1. Pull with rebase to reconcile the differences:
   ```bash
   git pull origin main --rebase
   ```

   **Alternative (using merge instead of rebase):**
   If you prefer to use a merge commit instead of rebasing, you can use:
   ```bash
   git pull origin main --merge
   ```
   (The `--merge` flag is explicit and avoids warnings in newer Git versions. You can also use `--no-rebase` which is equivalent.)
   
   This will create a merge commit. After resolving conflicts, you'll use `git commit` instead of `git rebase --continue` (see step 5 below).

2. Git will pause and indicate that there are conflicts. VSCode (or your editor) will highlight the conflicting lines in `collision.txt`.

3. **Resolve the conflict:** You want to **append** (not replace) the content so that everyone's entry is included. The file should contain all group members' entries, one per line:
   ```
   Alice, cat
   Bob, dog
   Carol, bird
   ```

4. After resolving the conflict, stage the resolved file:
   ```bash
   git add collision.txt
   ```

5. Complete the merge/rebase:
   - **If using rebase** (recommended for cleaner history):
     ```bash
     git rebase --continue
     ```
   - **If using merge**:
     ```bash
     git commit
     ```
     (This completes the merge commit)

6. Push your changes:
   ```bash
   git push origin main
   ```

7. The next person in the group should repeat steps 1-6 until everyone has successfully pushed their entry to the consolidated `collision.txt` file on GitHub. 


## Advanced Concepts (Optional)

### Stashing, rebasing, etc.

If you want to explore additional Git features, review the [Advanced git](https://uvads.github.io/git-basics/docs/advanced/) tutorial.

### Initializing a new repo and connecting it to GitHub with gh cli

You may already have a project set up in a directory on your computer (or in codespace), but it's not set up as a Git repository yet. The following steps show you how to initialize it and connect it to GitHub.

### Create a new local Git repository

1. Create a new directory for your project:
   ```bash
   cd # go to your home directory, or any other directory that is NOT inside an existing repo
   mkdir my-git-project
   cd my-git-project
   ```

2. Initialize a Git repository:
   ```bash
   git init
   ```

3. Verify the repository was created:
   ```bash
   ls -la .git
   ```

You should see a `.git` directory containing the repository metadata. **Note: this repository only exists in your local environment; it is not on GitHub yet.**


4. Create repository from command line (requires GitHub CLI)**
```bash
# Install GitHub CLI if not already installed
# Then create the repository:
gh repo create my-git-project --public --source=. --remote=origin --push
```

This single command creates the GitHub repository and pushes your code. See the "Pushing to remote" section for manual steps.

## Working with branches

1. Create a new branch:
   ```bash
   git branch feature-branch
   ```

   Switch to the new branch:
   ```bash
   git switch feature-branch
   ```

   Or use the shorthand to create and switch in one command:
   ```bash
   git switch -c feature-branch
   ```

2. Make changes on the branch:
   ```bash
   echo "New feature" > feature.txt
   git add feature.txt
   git commit -m "Add new feature"
   ```

3. Switch back to main:
   ```bash
   git switch main
   ```

4. List all branches:
   ```bash
   git branch
   ```

5. Merge the feature branch into main:
   ```bash
   git merge feature-branch
   ```

6. Delete the feature branch (after merging):
   ```bash
   git branch -d feature-branch
   ```

## Pull requests

**Exercise:** Create a pull request on GitHub

1. Create a new branch for your changes:
   ```bash
   git switch -c my-feature
   ```

2. Make some changes:
   ```bash
   echo "## Features" >> README.md
   echo "- Feature 1" >> README.md
   git add README.md
   git commit -m "Add features section to README"
   ```

3. Push the branch to GitHub:
   ```bash
   git push -u origin my-feature
   ```

4. On GitHub:
   - Navigate to your repository
   - You should see a banner suggesting to create a pull request
   - Click "Compare & pull request"
   - Add a description of your changes
   - Click "Create pull request"

5. Review the pull request:
   - Check the "Files changed" tab to see your modifications
   - Add comments if needed
   - Merge the pull request when ready

6. After merging, update your local repository:
   ```bash
   git switch main
   git pull origin main --merge
   git branch -d my-feature
   ```

## Advanced Concepts (Optional)

### Creating a Repository from a Template

GitHub allows you to create new repositories from templates, which can include pre-configured files, workflows, and settings. This is useful for starting projects with best practices already in place.

### Using the Secure Repository Template

The course repository includes a template URL for creating repositories with security best practices. Here's how to use it:

**Step 1: Get the template URL**

The template URL is located in `github-new-repo-from-template.txt` in this directory (`practice/03-git/`). The URL format is:

```
https://github.com/new?owner=YOUR_USERNAME&template_name=secure-repository-supply-chain&template_owner=skills&name=YOUR_REPO_NAME&visibility=public
```

**Step 2: Customize the URL**

Replace the placeholders:
- `YOUR_USERNAME` - Your GitHub username or organization name
- `YOUR_REPO_NAME` - The name you want for your new repository
- `visibility=public` - Change to `visibility=private` if you want a private repository

**Step 3: Create the repository**

1. Copy the complete URL with your customizations
2. Paste it into your browser's address bar
3. Press Enter
4. GitHub will open the repository creation page with the template pre-selected
5. Review the settings and click "Create repository"

**Example:**

If your username is `johndoe` and you want to create a repo called `my-secure-project`:

```
https://github.com/new?owner=johndoe&template_name=secure-repository-supply-chain&template_owner=skills&name=my-secure-project&visibility=public
```

**What you get:**

The "secure-repository-supply-chain" template from GitHub Skills includes:
- Security best practices configuration
- Supply chain security settings
- Dependabot setup for dependency updates
- Security policies
- Code scanning workflows
- GitHub Actions for security checks

**Alternative: Using GitHub's Web Interface**

You can also create a repository from a template using GitHub's web interface:

1. Go to the template repository: https://github.com/skills/secure-repository-supply-chain
2. Click the green **"Use this template"** button
3. Select **"Create a new repository"**
4. Choose your owner, repository name, and visibility
5. Click **"Create repository"**

## Resources

