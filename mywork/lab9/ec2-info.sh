#!/bin/bash

aws ec2 describe-instances | jq '.Reservations[].Instances[] | {ImageId,InstanceID,InstanceType,InstanceName: (.Tags[]? | select(.Key=="Name") | .Value),PublicIpAddress,State}'