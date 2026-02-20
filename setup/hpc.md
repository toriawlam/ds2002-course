---
layout: default
title: HPC Access
---

# HPC Access

The UVA High Performance Computing (HPC) systems (Rivanna and Afton) are accessible through a web portal, secure shell terminals, or a remote desktop environment. See the <a href="https://www.rc.virginia.edu/userinfo/hpc/login/" target="_blank" rel="noopener noreferrer">official documentation</a>.

**Service Unit Allocation:** The course is using the `ds2002` allocation. You will need to enter `ds2002` in the allocation field when requesting access to an interactive Open OnDemand session (like Code Server (VSCode), JupyterLab, Desktop), or when submitting compute jobs (you'll learn about this in Module 3).

## Login via Web Browser

Open OnDemand is a graphical user interface that allows access to HPC via a web browser. The Open OnDemand access point is <a href="https://ood.hpc.virginia.edu" target="_blank" rel="noopener noreferrer">ood.hpc.virginia.edu</a>. Within the Open OnDemand environment users have access to a file explorer; interactive applications like JupyterLab, RStudio Server & FastX Web; a command line interface; and a job composer and job monitor to submit jobs to the Rivanna and Afton clusters. Detailed instructions can be found on the <a href="https://www.rc.virginia.edu/userinfo/hpc/ood/" target="_blank" rel="noopener noreferrer">Open OnDemand documentation page</a>.

### Step 1: Start Open OnDemand

To start the Open OnDemand web client, go to <a href="https://ood.hpc.virginia.edu" target="_blank" rel="noopener noreferrer">https://ood.hpc.virginia.edu</a>. Your login is your UVA computing ID and your password is your Netbadge password.

![Open OnDemand portal](../docs/images/ood.png)

Proceed with one of these options:

[Step 2a: VSCode](#step-2a-vscode)

[Step 2b: JupyterLab](#step-2b-jupyterlab)

[Step 2c: Linux Desktop](#step-2c-linux-desktop)

### Step 2a: VSCode

1. On the top right of the menu bar of the Open OnDemand dashboard, click on `Interactive Apps`.
2. In the drop-down box, click on `Code Server` (that's VSCode).

**Enter `ds2002` in the allocation field.**

The form should look like this:

![OOD interactive session request](../docs/images/ood-vscode-request.png)

After you click `Launch` it may take a few minutes to start up. This is expected as we are sharing the cluster with hundreds of other users.

When ready, click the `Connect to VSCode` button.

![Open OnDemand Code Server](../docs/images/ood-vscode.png)

If this is your first time using VSCode on UVA's HPC system, click `Clone GitHub repository` in the Welcome window and follow the instructions. Use the url for your **fork of the course repository**, and authorize connection to GitHub.

### Step 2b: JupyterLab 

Follow the <a href="https://www.rc.virginia.edu/userinfo/hpc/software/jupyterlab/" target="_blank" rel="noopener noreferrer">Open OnDemand JupyterLab</a> instructions.

**Enter `ds2002` in the allocation field.**

The form should look like this:

![OOD interactive session request](../docs/images/ood-request.png)

After you click `Launch` it may take a few minutes to start up. This is expected as we are sharing the cluster with hundreds of other users.

![Open OnDemand JupyterLab](../docs/images/ood-jlab.png)

### Step 2c: Linux Desktop 

Follow the <a href="https://www.rc.virginia.edu/userinfo/hpc/ood/desktop/" target="_blank" rel="noopener noreferrer">Open OnDemand Desktop</a> instructions.

**Enter `ds2002` in the allocation field.**

![OOD interactive session request](../docs/images/ood-request.png)

After you click `Launch` it may take a few minutes to start up. This is expected as we are sharing the cluster with hundreds of other users.

![Open OnDemand Desktop](../docs/images/ood-desktop.png)




