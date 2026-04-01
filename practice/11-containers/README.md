# Containers

The goal of this activity is to familiarize you with containerization using Docker and related technologies. Containers are essential for creating reproducible environments, packaging applications with their dependencies, and deploying software consistently across different systems.

> **Note:** Work through the examples below in your terminal (Codespace or local), experimenting with each command and its various options. If you encounter an error message, don't be discouraged—errors are learning opportunities. Reach out to your peers or instructor for help when needed, and help each other when you can. 

* Start with the **In-class Exercises**. 
* Optional: Explore the **Advanced Concepts** if you wish to explore containers in more depth.

## Setup

**Option 1:**
If you want to use Docker containers on your own computer, follow the setup guide in `../../setup/docker.md`.

**Option 2:**
Alternatively spin up a Linux Ubuntu EC2 instance in AWS.

1. SSH to the Ubuntu EC2 instance (see [Lab 09](../../labs/09-ec2/README.md))
2. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh ./get-docker.sh
   ```

## In-class exercises

### Pulling & Running Docker Images

To pull a container image, find its location from Docker Hub or another registry. This should appear
something like:

```bash
docker pull godlovedc/lolcow
```

The `pull` command downloads the image from Docker Hub to your machine.

To run the default command of the image, execute:
```bash
docker run godlovedc/lolcow
```

Output:
```
 _____________________________________
/ Everything will be just tickety-boo \
\ today.                              /
 -------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

### Running in Interactive Mode

The LolCow container told you a joke (ran a process) and then exited immediately to return to your shell. 

Let's find a new image to explore how we can use a container interactively. Go to [Docker Hub](https://hub.docker.com/) and search for an Ubuntu image. Take note of the image name (`ubuntu`) and choose a tag. The tag is the portion after the `:`.

To work with a container interactively, append the `-it` flag to the `docker run` command. Be sure to add a shell or some other executable program after the image name and replace `<tag>` with the actual tag you found:

```bash
docker run -it ubuntu:<tag> /bin/bash
```

Note how the prompt has changed to something like this:
```
root@4489de2c677f
```
You're in a bash shell inside the container!

Now, run
```bash
cat /etc/os-release
```

To exit out of the interactive container shell, enter
```
exit
```

### Listing Docker images

To view all images you have built or pulled to your computer, run:

```bash
docker images
```

The output may look like this (column names vary slightly by Docker/runtime version):
```
IMAGE                                ID             DISK USAGE   CONTENT SIZE   EXTRA
godlovedc/lolcow:latest              a692b57abc43        370MB          104MB    U   
jekyll/jekyll:latest                 400b8d1569f1       1.23GB          322MB        
mysql:8.0                            99d774bf02a4       1.08GB          243MB    U   
```

How to read this table:

- `IMAGE`: repository and tag (for example, `mysql:8.0`) used to pull and run that image.
- `ID`: unique image identifier; you can use this instead of image name in commands like `docker rmi`.
- `DISK USAGE`: total local storage used by the image, including shared layers.
- `CONTENT SIZE`: size of this image's own filesystem layers/content.
- `EXTRA`: optional runtime-specific metadata. In some runtimes, `U` indicates an unpacked image. If this column is blank, that is normal.


### View Running Containers

To see all containers running locally:

```bash
docker ps
```

You should see output similar to:

```
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                      PORTS                                         NAMES
a57e5166fda7   ubuntu:latest    "/bin/bash"              4 seconds ago    Exited (0) 3 seconds ago                                                  heuristic_pare
```

To see all container instances, including those that have stopped, run this:
```bash
docker ps -a
```

```
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS                      PORTS                                         NAMES
ed9a3ade7cec   godlovedc/lolcow:latest   "/bin/sh -c 'fortune…"   3 seconds ago    Exited (0) 2 seconds ago                                                  hardcore_napier
a57e5166fda7   ubuntu:latest             "/bin/bash"              5 minutes ago    Exited (0) 5 minutes ago                                                  heuristic_pare
```

You can now refer to a specific container by using either the full name `heuristic_pare` or the first few characters of the container ID, such as `a57e`.

### Inspect Properties of a Container

To inspect all metadata attributes about a running container, such as IP address, or volume mounts, etc.
use the `inspect` command. This will return a JSON payload of fields:

```bash
docker inspect a57e
```

Try to find the `Cmd[]` section. It describes the command that's executed by default.

### File System

Each container image has its own filesystem. Let's check this out by comparing host and container output:

```bash
pwd
docker run --rm ubuntu:latest pwd
```

The first command runs on the host in your active shell. If you're in this repo's practice directory it will show something like:
```
/home/mst3k/ds2002-course/practice/11-containers/
```

The second command runs `pwd` inside a temporary Ubuntu container and will show:
```
/
```

Similarly, compare the output of `ls` and `docker run --rm ubuntu:latest ls`.

### Mount Storage

To mount a directory from your local workstation into a container when launched, use the `-v` flag with
a mapping of `HOST_DIRECTORY:CONTAINER_DIRECTORY`:

```bash
docker run -it -v .:/my_folder/ ubuntu:latest /bin/bash
```

Run `ls`.
```bash
bin  boot  dev  etc  home  lib  media  mnt  my_folder  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

Note the `my_folder` directory inside the container. Run `ls my_folder` and you should see the contents of your current host directory, now **mounted** inside `/my_folder`.

Now run: 
```bash
echo "hello from the container" > my_folder/hello.txt
```

Then `exit`.

Through this mechanism you can dynamically bring folders and files into the container. Any files you add to `my_folder` will persist when you exit the container. Pretty cool!

### Stop a Running Container

To stop a container:

```bash
docker stop heuristic_pare
```

or

```bash
docker stop a57e
```

### Deleting Docker images

>**Note:** Images can only be removed when there is no container instance with that image running anymore.

To delete an image, use the `rmi` (remove image) command with either the image name:tag or ID.

```bash
docker rmi image_name
```

To delete all unused images:

```bash
docker system prune
```

### Creating Docker Containers

This directory contains a few container examples. We focus on the mechanism of the build process rather than the specific implementation details underlying each project.

Let's try the Fortune Teller. The Dockerfile is located in `fortune/Dockerfile`.

```Dockerfile
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        fortune fortunes-min && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/games:${PATH}

ENTRYPOINT ["fortune"]
```

How this Dockerfile works:

- `FROM ubuntu:18.04` sets the base operating system image.
- `RUN ...` uses the Ubuntu package manager `apt-get` to install `fortune` and `fortunes-min`, then removes cache files of the `apt` package manager to keep the image smaller.
- `ENV PATH=/usr/games:${PATH}` adds the install location of `fortune` to the executable path.
- `ENTRYPOINT ["fortune"]` sets the default startup command, so `docker run fortune:latest` executes the `fortune` command inside the container and prints a fortune immediately.

Let's build it:
```bash
cd fortune
docker build -t fortune:latest .
```

Execute `docker images` to confirm the new `fortune:latest` image is ready.

And then run it:
```bash
docker run --rm fortune:latest
```

Run it a few more times for additional fortune telling.

### Apptainer - Containers in HPC Environments

On many clusters (including UVA’s), you **cannot run the Docker daemon** as an ordinary user: shared systems avoid giving everyone root-equivalent features that Docker traditionally needed. **[Apptainer](https://apptainer.org/)** (formerly Singularity) is a common alternative: you run container images **as yourself**, and you typically execute **immutable `.sif` image files** instead of talking to a long-lived daemon.

Go to your home directory. On the HPC system you also need to load the `apptainer` software module.

```bash
cd ~
module load apptainer
```

#### Creating an Apptainer image from a Docker image

The general form is `apptainer pull <output.sif> <transport>://<image reference>`. For images on Docker Hub, the transport is `docker` (for example `docker://ubuntu:latest` or `docker://godlovedc/lolcow:latest`).

```bash
apptainer pull lolcow-latest.sif docker://godlovedc/lolcow:latest
```

`apptainer pull … docker://…` downloads from a registry (often [Docker Hub](https://hub.docker.com/)) and builds a local `.sif` file. This `.sif` file is self-contained and you can move it to other locations.

Pull a few more images (still in the directory where you want the `.sif` files):

```bash
apptainer pull ubuntu-latest.sif docker://ubuntu:latest
```

```bash
apptainer pull mysql-8.0.sif docker://mysql:8.0
```

#### Running the Apptainer image

```bash
apptainer run lolcow-latest.sif
```

`apptainer run` executes the container’s default entrypoint. In this case it will run the script that tells you a joke.

Alternatively you can use the `apptainer exec` command:
```bash
apptainer exec ubuntu-latest.sif cat /etc/os-release
```

When you use `apptainer exec` you need to specify the command to execute inside the container after the image filename, in this case `cat /etc/os-release`.

#### Interactive shell

```bash
apptainer shell ubuntu-latest.sif
```

#### Mounting storage

Similar to **Docker** volume mounts, Apptainer can **bind** host paths into the container for `shell`, `exec`, and `run`. Use **`--bind`** (short form **`-B`**) with `host_path:container_path`.

```bash
apptainer shell --bind .:/my_folder ubuntu-latest.sif
```

You can repeat `--bind` (or `-B`) for multiple mappings. See [Apptainer bind paths](https://apptainer.org/docs/user/main/bind_paths_and_mounts.html) in the official docs.

## Advanced Concepts (Optional)

### Running in Detached Mode

To run a container in detached mode, append the `-d` flag to the `docker run` command with the
container image name:

```bash
docker run -d --name mysql-dbhost -e MYSQL_ROOT_PASSWORD=my-secret-pw mysql:8.0
```

Detached mode means the container runs in the background and your terminal prompt returns immediately. Use this when you want a long-running service (such as MySQL) to stay up while you continue using the same terminal for other commands. For example, start MySQL in detached mode, then run `docker ps` to confirm status before connecting with a client.

### Add an Environment Variable

To inject ENV variables into a container, add the `-e` flag with a Key-Value mapping when you run the container:

```bash
docker run -it -e MYKEY=myvalue ubuntu:latest /bin/bash
```

### Attach a Local Port

To map a local port from a container to your workstation, use the `-p` flag with a mapping of
`HOST_PORT:CONTAINER_PORT`. This allows you to view/test a service listening on that port:

```bash
docker run -d --name mysql-dbhost -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 6033:3306 mysql:8.0
```

### Review Logs

To view the output logs from a running container:

```bash
docker logs 2ad2
```

### Shell into a Running Container

Finally, to "hop" into a running container that is running in detached mode, use the `exec -it` command
against the ID or name of the running container. Be sure to add a shell or other executable after the name
of the container.

```bash
docker exec -it 2ad2 /bin/bash
```

### More Build Examples

#### `whalesay`

This is a famous demo container created by Docker to demonstrate an interactive
container image that takes input from a user. To build it, cd into this directory:

```bash
docker build -t whalesay .
```
To run it, simply append a command or quote or joke at the end of the `run` command:
```bash
docker run whalesay Hello everyone!
```

#### `convert`

This is a simple Python ETL pipeline. You can build
it locally by changing into its directory and running:

```bash
docker build -t converter .
```
To try running it on your own, just map a directory to the `/data` path of the container and pass the
fictional ID `0987654321` as a parameter:

```bash
docker run -v ${PWD}:/data converter -i 0987654321
```

### Multi-Stage Builds

Multi-stage builds allow you to use multiple `FROM` statements in a Dockerfile, which helps create smaller final images by separating build dependencies from runtime dependencies:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

### Docker Compose

Docker Compose allows you to define and run multi-container Docker applications using a YAML file. This is useful for orchestrating services that need to work together:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

Note the `build: .` statement for the `web` service. The `.` refers to the current directory and it is assumed that it contains a `Dockerfile` with the image build instructions. In contrast, the `redis` service will utilize an existing image `redis:alpine` from a public repository.

Run with: `docker compose up`


### Dockerfile Best Practices

- Use specific version tags instead of `latest`
- Order Dockerfile instructions from least to most frequently changing
- Use `.dockerignore` to exclude unnecessary files
- Minimize the number of layers
- Use multi-stage builds for smaller images
- Run containers as non-root users when possible

### Container Orchestration

For production environments, consider container orchestration platforms:
- **Kubernetes**: Industry-standard for container orchestration
- **Docker Swarm**: Built-in orchestration for Docker
- **Amazon ECS**: AWS container orchestration service
- **Azure Container Instances**: Serverless containers on Azure

### Running Apptainer with GPU support

If your host has NVIDIA GPUs and drivers available, Apptainer can expose them inside the container with the `--nv` flag.

```bash
apptainer exec --nv pytorch-latest.sif python -c "import torch; print(torch.cuda.is_available())"
```

You can also test GPU visibility with:

```bash
apptainer exec --nv pytorch-latest.sif nvidia-smi
```

If GPUs are configured correctly, these commands should report at least one CUDA device.

### Making Apptainer images executable

Apptainer images include a default runscript. If you mark the `.sif` file as executable, you can launch it directly instead of typing `apptainer run` each time:

```bash
chmod +x lolcow-latest.sif
./lolcow-latest.sif
```

This is functionally similar to:

```bash
apptainer run lolcow-latest.sif
```

## Resources

* <a href="https://www.docker.com/resources/what-container/" target="_blank" rel="noopener noreferrer">What is a Container?</a> - Introduction to containerization concepts
* <a href="https://docs.docker.com/get-started/" target="_blank" rel="noopener noreferrer">Docker Getting Started Tutorial</a> - Official getting started guide
* <a href="https://docker-curriculum.com/" target="_blank" rel="noopener noreferrer">Docker Curriculum</a> - Free interactive Docker tutorial
* <a href="https://labs.play-with-docker.com/" target="_blank" rel="noopener noreferrer">Play with Docker</a> - Interactive Docker playground
* <a href="https://github.com/docker/awesome-compose" target="_blank" rel="noopener noreferrer">Docker Official Samples</a> - Official Docker Compose examples
* <a href="https://docs.docker.com/engine/security/" target="_blank" rel="noopener noreferrer">Docker Security Best Practices</a> - Security guidelines
* <a href="https://apptainer.org/docs/" target="_blank" rel="noopener noreferrer">Apptainer Documentation</a> - Official docs for running containers in HPC environments

### Container Registries

* <a href="https://hub.docker.com/" target="_blank" rel="noopener noreferrer">Docker Hub</a> - Default public registry
* <a href="https://github.com/features/packages" target="_blank" rel="noopener noreferrer">GitHub Container Registry (GHCR)</a> - Integrated with GitHub
* <a href="https://aws.amazon.com/ecr/" target="_blank" rel="noopener noreferrer">Amazon ECR</a> - AWS container registry
* <a href="https://cloud.google.com/container-registry" target="_blank" rel="noopener noreferrer">Google Container Registry</a> - GCP container registry
* <a href="https://azure.microsoft.com/services/container-registry/" target="_blank" rel="noopener noreferrer">Azure Container Registry</a> - Azure container registry
