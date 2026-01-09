---
layout: default
title: MacOS & Linux Setup
---

# MacOS & Linux Setup

## Setting Up Your Own Computer for Course Projects (Optional)

**Note: If you are new to programming and are not familiar with installing programming tools on your computer, I highly recommend skipping this step and using [GitHub Codespaces](README.md#using-github-codespaces-for-your-projects-recommended) instead.** This will allow you to get started immediately without the hassle of troubleshooting any setup issues.

However, if you want to set up an environment for class work on your own computer, here are the basic steps. 

To set up your own computer for all course activities I highly encourage you to install all the python packages in a new environment. Think of an environment as an isolated area to install the software packages you need for a specific project, i.e. in this case the course activities. Packages in an environment are isolated from other software packages on your computer.
   - **Best practice:** Create a new environment for each of your projects.
   - **Isolation:** It is typically defined in a specific folder on your computer.
   - **Experimentation:** It allows you to tweak installation of new packages without disrupting packages in other environments. 
   - **Avoid conflict:** It allows you to manage packages that are not compatible in separate environments.

### VSCode

Download and install [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview) from the official website. Follow the platform-specific installation instructions for your operating system (macOS or Linux).

### Tools & Python

MacOS and Linux have terminal applications pre-installed. So you won't need Git-Bash. Follow these steps to install miniforge for Python.

1. Open a terminal window.
2. Download the installer script: The command below automatically detects your system's architecture and downloads the correct Miniforge3 installer from the official conda-forge GitHub repository.
   ```bash
   curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh
   ```
   **Note:** For some specific macOS architectures (like Apple Silicon/arm64), the command might be slightly different; you can check the [Miniforge GitHub page](https://github.com/conda-forge/miniforge) for direct links if the automatic detection fails.
3. Run the installation script: Execute the downloaded script using bash.
   ```bash
   bash Miniforge3-$(uname)-$(uname -m).sh
   ```
   Alternatively, if the automatic detection in the filename does not work, you can use a fixed filename after downloading it, for example:
   ```bash
   bash Miniforge3.sh
   ```
   Follow the prompts: The installer will guide you through the process.
   - Press ENTER or return to view the license agreement.
   - Scroll through the license and type `yes` to accept the terms.
   - Confirm the default installation location (typically ~/miniforge3). Press ENTER to accept it.
   - When asked if you want to initialize Conda for your shell (e.g., bash or zsh), type `yes`.
4. Restart your terminal: For the changes to take effect, close your current terminal window and open a new one.
5. Verify the installation:
   - Once the terminal is restarted, you should see `(base)` in your terminal prompt, indicating the Miniforge base environment is active.
   - Run the following command to verify:
     ```bash
     conda list
     ```
   - If a list of installed packages appears without errors, the installation was successful. 
6. Create a conda (mamba) environment and install the other software packages. In your terminal execute the following command:
   ```bash
   mamba env create -n ds2002 -c conda-forge python=3.11 htop jq awscli curl wget git zip unzip tar redis-server redis-py mongodb
   ```
   
   Run the command `conda activate ds2002` to activate the environment, then run `conda list`. You should see a list of installed packages, and your prompt should show (ds2002) at the beginning, confirming that the ds2002 environment is active.

**Note: The first step when opening a new terminal is to run `conda activate ds2002`.** If your Mac is using zsh and throws an error, you can use `source activate ds2002` instead. You can add that command to the ~/.bashrc (or .zshrc) file if you wish.

**Please be aware that we have limited bandwidth to guide you through fixing broken installations on your computer. If installations fail, you can always go back to using GitHub Codespaces.**

