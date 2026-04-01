# Using Docker containers

Docker lets you package software and dependencies into a portable container that behaves consistently across systems. Containers make it easier to run course tools and examples without installing everything directly on your machine. 

The two most popular options to run Docker on your own computer are:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) - first on the scene, requires a paid subscription for larger organizations.
- [Rancher Desktop](https://rancherdesktop.io/) - open source alternative, fully Docker compatible

Complete one setup path below, then run the test commands to confirm your install is working.

## Setup

### Docker Desktop

1. Download Docker Desktop for your operating system from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
2. Install using default options.
3. Launch Docker Desktop and complete first-run prompts.
4. Wait until Docker reports it is running.
5. In a terminal, verify the CLI:

```bash
docker --version
docker info
```

If `docker --version` shows a version string and `docker info` prints system details, setup is complete.

### Rancher Desktop

If you prefer Rancher Desktop instead of Docker Desktop:

1. Download Rancher Desktop from [https://rancherdesktop.io/](https://rancherdesktop.io/).
2. Install and launch the application.
3. During first-run setup, choose **`dockerd (moby)`** as the container runtime (not `containerd`).
4. In application settings, make sure Rancher Desktop installs the Docker CLI/symlink so `docker` commands work directly (no `nerdctl` translation needed).
5. In a terminal, verify:

```bash
docker --version
docker info
```

If both commands work, your Docker-compatible environment is ready.

## Test

Run the following commands to confirm pull, image listing, and container execution.

```bash
docker pull godlovedc/lolcow
```

Expected: Docker downloads image layers and reports success.

```bash
docker images
```

Expected: `lolcow` appears in your local image list.

```bash
docker run godlovedc/lolcow
```

Expected: you see ASCII art output from the container.
