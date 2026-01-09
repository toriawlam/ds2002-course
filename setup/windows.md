---
layout: default
title: Windows Setup
---

# Windows Setup

## Setting Up Your Own Computer for Course Projects (Optional)

**Note: If you are new to programming and are not familiar with installing programming tools on your computer, I highly recommend skipping this step and using [GitHub Codespaces](README.md#using-github-codespaces-for-your-projects-recommended) instead.** This will allow you to get started immediately without the hassle of troubleshooting any setup issues.

However, if you want to set up an environment for class work on your own computer, here are the basic steps. 

To set up your own computer for all course activities I highly encourage you to install all the python packages in a new environment. Think of an environment as an isolated area to install the software packages you need for a specific project, i.e. in this case the course activities. Packages in an environment are isolated from other software packages on your computer.
   - **Best practice:** Create a new environment for each of your projects.
   - **Isolation:** It is typically defined in a specific folder on your computer.
   - **Experimentation:** It allows you to tweak installation of new packages without disrupting packages in other environments. 
   - **Avoid conflict:** It allows you to manage packages that are not compatible in separate environments.

### VSCode

Download and install [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview) from the official website. Follow the platform-specific installation instructions for Windows.

### Tools & Python

Since we're using the Linux command line, you will need to install a Linux-like terminal program. I recommend installing Git-Bash which provides the Linux-style terminal and also Git.

1. Install Git-Bash: Download and install Git-Bash from the [official Git website](https://git-scm.com/downloads).
2. Download the Miniforge Installer: Go to the [conda-forge Miniforge GitHub repository](https://github.com/conda-forge/miniforge) and download the Windows executable file (Miniforge3-Windows-x86_64.exe).
3. Run the Executable Installer: Double-click the downloaded .exe file to run the installer.
   - Follow the prompts, accepting the license agreement.
   - It is highly recommended to install for "Just Me" (per user) to avoid potential permission issues later.
   - Note the installation path: The default installation path is usually within your AppData\Local folder (e.g., C:\Users\YOUR_USERNAME\AppData\Local\miniforge3). Remember this location.
   - Check the "Create start menu shortcuts" option. The most convenient and tested way to use the installed software (such as commands conda and mamba) is via the "Miniforge Prompt" installed to the start menu.
   - Check the "Add Miniforge3 to my PATH environment variable" option. 
4. Create a conda (mamba) environment. In your terminal execute the following command
   ```bash
   mamba env create -n ds2002 -c conda-forge python=3.11 htop jq awscli curl wget git zip unzip tar redis-server redis-py mongodb
   ```
5. Configure Git Bash: After the installation is complete, you need to configure Git Bash to recognize the conda commands.
   - Open a Git Bash terminal.
   - Run the following command to update your ~/.bashrc file. Adjust the path if you installed Miniforge in a non-default location (see step 3):
      ```bash
      echo "source ~/AppData/Local/miniforge3/etc/profile.d/conda.sh" >> ~/.bashrc
      ```
6. Restart Git Bash and Verify:
   - Close and re-open your Git Bash terminal for the changes to take effect.
   - Run `conda activate ds2002`. The prompt should change from `base` to `ds2002` indicating the switch to your new environment.
   - Run the command `conda list`. You should see a list of installed packages, and your prompt should show (ds2002) at the beginning, confirming that the ds2002 environment is active.

**Note: The first step when opening a new terminal is to run `conda activate ds2002`.** You can add that command to the ~/.bashrc file if you wish.

**Please be aware that we have limited bandwidth to guide you through fixing broken installations on your computer. If installations fail, you can always go back to using GitHub Codespaces.**

