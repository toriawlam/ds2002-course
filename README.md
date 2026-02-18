# ds2002

Welcome to DS2002 Data Science Systems!

This repository tracks your working environment during this course. Some course material
and tools will be distributed in this way so that we all have a common set of tools, scripts, and datasets.

This requires that you clone and stay current with the **course code repository** and have the appropriate
tools to complete exercises. 

## Updating your fork 

To stay current with new releases into the course repository, change into the repository folder and follow these steps:

### Step 1: Add an upstream source
```
git remote add upstream https://github.com/ksiller/ds2002-course.git
```

If you receive an error `error: remote upstream already exists.`, run these commands to remove the existing `upstream` and re-add it.

```
git remote remove upstream
git remote add upstream https://github.com/ksiller/ds2002-course.git
```

Confirm the new `upstream` remote:
```
git remote -v
```

Output:
```
origin  URL_OF_YOUR_REPO (fetch)
origin  URL_OF_YOUR_REPO (push)
upstream        https://github.com/ksiller/ds2002-course.git (fetch)
upstream        https://github.com/ksiller/ds2002-course.git (push)
```

Continue with [Step 2: Fetch from upstream and merge](#step-2-fetch-from-upstream-and-merge).

### Step 2: Fetch from upstream and merge 

This assumes that you have successfully completed [Step 1: Add an upstream source](#step-1-add-an-upstream-source). 

Switch to main branch:
```
git switch main
```

Fetch from the upstream branch:
```
git fetch upstream
```

Merge the upstream branch into your local branch.
```
git merge upstream/main
```

This can be run in a single block:
```
git switch main
git fetch upstream
git merge upstream/main
```

If you get an error like this...
```
fatal: 'upstream' does not appear to be a git repository
fatal: Could not read from remote repository.
```
...then go back to the section and complete the steps for [Step 1: Add an upstream source](#step-1-add-an-upstream-source) first. Then repeat the steps in this section.

At this point your local clone/fork as you see it on your own computer or Codespace is up to date. But your fork on GitHub is not updated yet! In order to do that, follow [Saving your changes](#saving-your-changes).

## Saving your changes

If you've pulled the latest from upstream, or if you generate code, scripts, data files, etc. that you would like to keep, simply add, commit, and push the files back to **your** fork of the repository:
```
git add .
git commit -m "Some meaningful message"
git push origin main
```

Remember that changes you commit and push will be saved to YOUR fork of the repository.
