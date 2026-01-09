---
layout: default
title: DS2002 Data Science Systems
---
## Course Description

This course introduces you to the core technical concepts and practical skills needed to interact with systems to process data science workloads. You’ll learn how to choose and manage computing environments and storage options, from small local setups to larger cloud-based systems, and how to use essential database models for storage and analysis.

Throughout the course, you’ll work extensively with the command line, scripting, and managing code and resources across local and cloud platforms. By the end of the course, you’ll have a solid technical foundation and a practical set of tools to support your work in future data science courses and projects.

## Getting Started

To get started with the course, please follow the **[Setup Instructions](setup/)** to configure your development environment.

## Practice

Work through the **[Hands-on Exercises](practice/exercises.md)** to practice and consolidate concepts introduced during class lectures and discussions. 

Each unit contains an "Advanced Concepts" section that allows you to dive deeper into a topic. **Note: Advanced concepts will not be covered in quizzes or labs.**

Check the end of each unit for links to additional resources for further exploration.

## Labs

Weekly labs are released with instructions on the **[course Canvas page](https://canvas.its.virginia.edu/courses/167598)**.

## Repository Management

### Updating Your Fork

To stay current with new releases from the course repository:

1. Add an upstream source (if not already added):
   ```bash
   git remote add upstream git@github.com:ksiller/ds2002-course.git
   ```

2. Fetch from the upstream branch:
   ```bash
   git fetch upstream
   ```

3. Merge your branch with the upstream branch:
   ```bash
   git merge upstream/main main
   ```

### Saving Your Changes

If you generate code, scripts, data files, etc. that you would like to keep, add, commit, and push the files back to **your** fork of the repository:

```bash
git add .
git commit -m "Some meaningful message"
git push origin main
```

Remember that changes you commit and push will be saved to **your** fork of the repository.

