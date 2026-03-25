# Lab 09: Amazon EC2

## Case study

A small organization is moving some workloads off local machines and wants a **pilot Linux server in the cloud** before a larger migration. You stand up that prototype: use the AWS CLI and console to inspect EC2, create an SSH key pair, launch an Ubuntu instance in the shared course account, log in, and install a minimal Python toolchain (including `boto3`, consistent with Lab 08).

When you finish, you will have run through the core provision → connect → configure loop for one VM and will submit scripts plus a short screenshot.

## Learning goals

By completing this lab, you will be able to:

- Confirm AWS CLI identity and use `aws ec2 describe-instances` with `jq` to summarize instances.
- Create an EC2 key pair and use a `.pem` private key with `ssh -i`.
- Gather AMI, subnet, and security group details from the console and launch an instance from a bash script.
- SSH into the instance, install packages, and verify the environment (for example `python3 -c "import boto3"`, `htop`).

---

### 1. Load your environment

For this lab, start an Open OnDemand Code Server (VS Code) session on the UVA HPC system. In your session, open a new terminal and activate your environment:

```bash
module load miniforge
source activate ds2002
```

### 2. Confirm your AWS CLI configuration

You used the `ds2002-user` user account in AWS for Lab 08. Confirm that your AWS CLI is configured accordingly.

```bash
aws sts get-caller-identity
```

The output should look like this:
```json
{
    "UserId": "AIDAYRXHJIA3N7XIGYSMI",
    "Account": "587821826102",
    "Arn": "arn:aws:iam::587821826102:user/ds2002-user"
}
```

If not, go through the `aws configure` steps of [Lab 08](../08-s3/README.md#setup) again.

### 3. Check existing EC2 instances

```bash
aws ec2 describe-instances
```

Use `jq` to filter the list to only include `ImageId`, `InstanceId`, `InstanceType`, a display name for the instance (`InstanceName` or `Name`), `PublicIpAddress`, and `State`.

**Hint:** Start with `aws ec2 describe-instances | jq '.Reservations[].Instances[]'`. That gives one JSON object per instance; add `jq` filters to pick the fields below. The instance name shown in the console is usually the tag with `"Key": "Name"`—extract that tag’s `"Value"` (not every tag value).

The output should look like this (one JSON object per instance; your `jq` filter may emit several in sequence):

```json
{
  "ImageId": "ami-07ff62358b87c7116",
  "InstanceId": "i-09829fd2c5dc3d692",
  "InstanceType": "t3.nano",
  "InstanceName": "ds2002-demo",
  "PublicIpAddress": "54.234.9.240",
  "State": {
    "Code": 16,
    "Name": "running"
  }
}
```

Create a bash script `ec2-info.sh` with your `aws ec2 ... | jq ...` command.

### 4. Create key pair

Before launching a new EC2 instance, create a key pair that will allow you to connect via `ssh` to the running instance post-launch.

Remember, a key pair has a **public** and a **private** component. AWS stores the **public** half of an SSH key pair in your account and associates it with the key pair name you choose. When you create a key pair, AWS returns the **private** key once (in PEM format). **You must save the private key immediately; you cannot download the private key again later.**


```bash
mkdir -p ~/.ssh
```

Create a new key pair named `key-ec2` and save the private key under your hidden `~/.ssh` directory as `key-ec2.pem` (one shared name for the course; do not commit this file to Git):

```bash
aws ec2 create-key-pair \
  --key-name key-ec2 \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/key-ec2.pem
```

The `key-ec2.pem` file is the **private** key. **Keep it secret and never commit it to Git.**

```bash
ls -la ~/.ssh
```
Notice the permissions:
```
-rw------- 1 mst3k users 1675 Mar 24 21:58 /home/mst3k/.ssh/key-ec2.pem
```
This means the key file can be read and (re)written (or deleted) by you only.

Let's tighten the permissions even more to prevent accidental overwriting or deletion.
```bash
chmod 400 ~/.ssh/*.pem
ls -la ~/.ssh
```

```
-r-------- 1 mst3k users 1675 Mar 24 21:58 /home/mst3k/.ssh/key-ec2.pem
```

**`chmod 400`** makes the private key readable only by you; SSH refuses to use a key that is too permissive.

You will use this key in step 7.

### 5. Spin up a new EC2 instance

In order to launch a new EC2 instance, we need to specify:

- AMI image identifier (Amazon Linux, Ubuntu, etc.)

- Instance type (t2.nano, t2.micro, etc.)

- Name of a key pair for SSH access (created in step 4)

- Security group ID (controls inbound/outbound traffic)

- Network subnet ID (which subnet inside the VPC the instance attaches to). You do **not** pass a separate VPC ID here: the subnet already implies the VPC, as long as the security group belongs to that same VPC.

Create a new bash script `launch-ec2.sh` based on this template:

```bash
#!/bin/bash

AMI=NNNN
INSTANCE_TYPE=XXXX
INSTANCE_NAME=XXXX
KEY_NAME=XXXX
SECURITY_GROUP_ID=NNNN
SUBNET_ID=NNNN

# Complete this command with the right flags (e.g. --image-id, --instance-type, --key-name,
# --security-group-ids, --subnet-id) and a Name tag from INSTANCE_NAME.
aws ec2 run-instances
```

Log into the AWS Console as `ds2002-user` using the URL, username, and password provided in `Lab 08` on Canvas. In the AWS Console, gather the following information:

- Search the Amazon Machine Image catalog for an Ubuntu image. Image IDs start with `ami-*`. Assign the value to the `AMI` variable in your bash script.
- Set `INSTANCE_TYPE` to `t2.nano`
- Set `INSTANCE_NAME` to `ds2002-<YOUR_COMPUTING_ID>`, e.g. `ds2002-mst3k` (same `ds2002-<computing id>` prefix as S3 bucket names in [Practice 09](../../practice/09-iam-s3/README.md))
- Set `KEY_NAME` to `key-ec2` (the key pair name from step 4)
- In AWS Console, find the EC2 instance `ds2002-demo`. Select the `Security` tab and locate the ID shown under `Security group`. The Security group IDs start with `sg-*`. Copy that value and assign it to `SECURITY_GROUP_ID` in your bash script.
- Go back to the AWS Console, find the EC2 instance `ds2002-demo` (again). Select the `Networking` tab and locate the subnet ID (values start with `subnet-*`). Copy that value and assign it to `SUBNET_ID` in your bash script.

Complete the `aws ec2 run-instances` command in the bash script using the appropriate options and the environment variables you set at the top of your script.

Execute the `launch-ec2.sh` script. If successful, you should see output similar to this:

```json
{
    "ReservationId": "r-0a1b2c3d4e5f67890",
    "OwnerId": "587821826102",
    "Groups": [],
    "Instances": [
        {
            "InstanceId": "i-0f1e2d3c4b5a67890",
            "ImageId": "ami-0123456789abcdef0",
            "State": {
                "Code": 0,
                "Name": "pending"
            },
            "InstanceType": "t2.nano",
            "KeyName": "key-ec2",
            "PrivateDnsName": "ip-10-0-1-23.ec2.internal",
            "PublicDnsName": "",
            "PublicIpAddress": null
        }
    ]
}
```

Your IDs, AMI, key name, and networking fields will differ. `State.Name` may move from `pending` to `running` shortly after launch; `PublicIpAddress` is often empty until the instance gets a public IP.

> **Note:** The public half of the key pair is registered on the instance at launch so you can SSH with your matching `.pem` private key.

### 6. Confirm your instance appears in the list

Rerun `ec2-info.sh` and redirect its output to `ec2-info.txt` so you can confirm your new EC2 instance is listed.

For example (from the directory where the script lives, after `chmod +x ec2-info.sh` if needed):

```bash
./ec2-info.sh > ec2-info.txt
```

Take note of the public IP address of your new instance.

### 7. Install software on your EC2 instance

- SSH into your instance using the key from step 4 and the instance’s public IP address (see steps 3 and 6 for how to find it).

    ```bash
    ssh -i ~/.ssh/key-ec2.pem ubuntu@<PUBLIC_IP>
    ```

    Replace `<PUBLIC_IP>` with the instance’s public IP from step 6 (or from the `jq` output in step 3).

    Use `ubuntu` for Ubuntu AMIs and `ec2-user` for Amazon Linux if your AMI uses that default user. These accounts are set up by default when you launch an EC2 instance.

    The first time you do this, you will see a message and prompt like this:
    ```
    The authenticity of host '54.236.22.146 (54.236.22.146)' can't be established.
    ECDSA key fingerprint is SHA256:cmNq+Tzj7eN7CVpSrCX7CAw74Oo50tcmwO4RVuqkJf8.
    Are you sure you want to continue connecting (yes/no/[fingerprint])?
    ```

    Type `yes` and press <Enter/Return> to confirm.

    You should see a prompt like this:
    ```bash
    ubuntu@ip-172-31-21-18:~$
    ```

    **Congratulations — you successfully logged in to your new EC2 virtual machine in the AWS cloud.**

- Use the following commands to install packages on the instance (Ubuntu AMIs use `apt`; `python3-pip`, `git`, and `htop` are standard Ubuntu packages):

  ```bash
  sudo apt-get update
  sudo apt-get install -y python3-pip git htop
  python3 -m pip install --user boto3
  ```

  `sudo` runs `apt-get` as root so system packages install cleanly. Avoid `sudo pip install …` on recent Ubuntu releases (PEP 668 “externally managed environment”); installing `boto3` with `python3 -m pip install --user` puts it in your own `~/.local` and matches how you use `boto3` elsewhere in the course. Alternatively you can install the distro package only: `sudo apt-get install -y python3-boto3 git htop` (no `pip` step).

  If you find yourself installing the same packages on every new VM, consider [bootstrapping with user data](../../practice/10-cloud/README.md#user-data-bootstrapping).

- Create the following bash script `ec2-env.sh` to confirm the environment:

  ```bash
  hostname
  cat /etc/os-release
  python3 -m pip list
  ```

  Run the `ec2-env.sh` script on the EC2 instance and redirect its output to `~/my-ec2-instance.txt`.

- Run `htop`. How many processors do you see? Take a screenshot and save it in your lab submission folder (e.g. `mywork/lab9`).

### 8. Optional: Stand up a simple web service

There was no HTTP listener in the steps above—your security group likely allows only SSH. **Nginx** is a lightweight, production-grade web server that listens for HTTP requests and returns web content; in this lab you will use it as a quick way to verify that your EC2 instance can serve traffic publicly on port 80. To run a minimal public service (default Nginx welcome page), follow **[Run a simple web service (Nginx)](../../practice/10-cloud/README.md#run-a-simple-web-service-nginx)** in Practice 10 (Cloud): allow **HTTP (TCP 80)** on the instance (for example by attaching the course HTTP security group), install **`nginx`**, then open `http://<public-ip>/` in a browser. No extra lab deliverable; this is optional practice.

**After you have confirmed that you can reach `http://<public-ip>/`, go back to the AWS Console and remove the `nginx-test` security group from the EC2 instance.** That will block HTTP traffic to the instance.

### 9. Log out from the EC2 instance

In the EC2 terminal session, execute `exit` to leave the EC2 instance.
```bash
ubuntu@ip-172-31-21-18:~$ exit
```

You should see (your IP address will be different):
```
logout
Connection to 54.236.22.146 closed.
```

### 10. Copy files from EC2 instance

In your terminal window, run this command to copy `my-ec2-instance.txt` from the EC2 instance to your local session (your current directory in the Open OnDemand Code Server session). Replace `<PUBLIC_IP>` with your instance’s public IP address.

```bash
rsync -e "ssh -i ~/.ssh/key-ec2.pem" ubuntu@<PUBLIC_IP>:~/my-ec2-instance.txt .
```

**Conclusion: You delivered a working EC2 prototype for the DS2002 startup case study, validated SSH access, and collected baseline system evidence for the team.**

## Submit your work

By the end of this lab, your repository should contain the following in `mywork/lab9/`:

- `ec2-info.sh`
- `ec2-info.txt` (from step 6)
- `launch-ec2.sh`
- Screenshot of `htop` on your EC2 instance
- `my-ec2-instance.txt`

Add, commit, and push your `mywork/lab9` folder, then submit the GitHub URL to that folder in Canvas for grading.