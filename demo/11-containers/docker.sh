#!/bin/bash

#pull image
docker pull godlovedc/lolcow

#run image
docker run godlovedc/lolcow

#run image interactively
docker run -it ubuntu:latest /bin/bash

    cat /etc/os-release
    exit

#list images
docker images

#list running containers
docker ps

#list all containers
docker ps -a

# inspect ubuntu container
docker inspect c0c802659f3c

# file system
pwd
docker run --rm ubuntu:latest pwd

ls
docker run --rm ubuntu:latest ls

# mount storage
docker run -it -v .:/my_folder/ ubuntu:latest
    ls
    ls my_folder
    echo "hello from the container" > my_folder/hello.txt
    ls my_folder
    exit

ls # hello.txt is in current directory on host
cat hello.txt

# stop container
docker stop c0c802659f3c

# delete container
docker rm c0c802659f3c

# delete image
docker rmi ubuntu:latest

# build image
cd fortune
docker build -t fortune:latest .
docker images
docker run --rm fortune:latest

-----

module load apptainer

apptainer pull lolcow-latest.sif docker://godlovedc/lolcow:latest
apptainer run lolcow-latest.sif
