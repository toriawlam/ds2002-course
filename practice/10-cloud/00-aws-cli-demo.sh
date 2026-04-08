#!/bin/bash

# name for the instance can be defined as tags
TAGS='ResourceType=instance,Tags=[{Key=Name,Value=in-class-demo}]'
AMI="ami-0b75f821522bcff85" # Debian Linux
SG="sg-0d3c1292b665a166f" # use existing one, update as needed

# create key pair. needed for ssh access to EC2 instance
aws ec2 create-key-pair --key-name demokey --query 'KeyMaterial' --output text > demokey.pem

# show private key. DON'T SHARE
cat demokey.pem

# show public portion of key. This portion will be placed on the EC2 instance for you
ssh-keygen -y -f demokey.pem

# secure your keym, make it read-only for you
chmod 400 demokey.pem
ls -la demokey.pem
mv demokey.pem ~/.ssh

# Optional
# create new security group. Automatically placed in default vpc
# aws ec2 create-security-group --group-name "demo" --description "SG for demo"
# SG="" # set the new SG ID

# Allow ssh access via port 22 from all IP addresses 0.0.0.0/0
# aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 22 --cidr 0.0.0.0/0

# launch EC2 instance
aws ec2 run-instances --image-id $AMI --count 1 --instance-type t2.micro --key-name demokey --tag-specifications $TAGS --security-groups $SG
# take note of the instance ID and set IID for convenience
IID=""

# get description
aws ec2 describe-instances --instance-ids $IID

# parse with jq
aws ec2 describe-instances --instance-ids $IID | jq '.Reservations[].Instances[] | .InstanceId,.State,.Tags,.PublicIpAddress'
IP="" # set to actual public IP address

# ssh to new EC2 instance, use your private key in ~/.ssh/demokey.pem
# the default account on Debian is "admin", so use that
ssh -i ~/ssh/demokey.pem admin@$IP
# Perform some admin tasks on EC2 instance
sudo apt update
sudo apt install python3-pip git
python3 -V
#create new user, switch to new user, and clone repo into new user's home dir 
sudo adduser mst3k
su mst3k
cd
git clone https://github.com/ksiller/ds2002-course.git
exit # leave mst3k account -> back to admin account
exit # logout from EC2 instance, back in local terminal

# Stop, resize, restart
aws ec2 stop-instances --instance-ids $IID
aws ec2 wait instance-stopped --instance-ids $IID
aws ec2 modify-instance-attribute --instance-id $IID --instance-type '{"Value": "t2.nano"}'
aws ec2 start-instances --instance-ids $IID

# Terminate
aws ec2 terminate-instances --instance-ids $IID
