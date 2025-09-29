# Ansible Runner Docker Images

This repository provides Docker images for running Ansible with additional Python libraries. The images are based on Alpine Linux for minimal size and include Ansible along with common automation tools.

## Features

- **Multi-stage builds** for reduced image size
- **Alpine Linux** base for lightweight containers
- **Multiple Ansible versions** supported
- **Additional Python libraries** for automation tasks
- **Non-root user** (UID 1000) for Kubernetes compatibility

## Included Packages

### Ansible Versions
- 2.9, 2.10, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, latest

### Additional Python Libraries
- requests
- pyyaml
- jinja2
- netaddr
- kubernetes

## Building Images

### Local Build
```bash
./build.sh
```

### Build and Push
```bash
./build.sh --push
```

This will build images for all supported Ansible versions and tag them as `kenchrcum/ansible-runner:<version>`.

## Usage

### Run Ansible Commands
```bash
docker run --rm kenchrcum/ansible-runner:latest ansible --version
```

### Use in Kubernetes
The images run as user ID 1000, making them compatible with Kubernetes security contexts.

Example pod spec:
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: ansible-runner
    image: kenchrcum/ansible-runner:latest
    securityContext:
      runAsUser: 1000
```

### Mounting Playbooks
```bash
docker run --rm -v $(pwd)/playbooks:/workspace kenchrcum/ansible-runner:latest ansible-playbook playbook.yml
```

## Customization

### Adding More Libraries
Edit `requirements.txt` to add additional Python packages.

### Changing Ansible Versions
Modify the `ANSIBLE_VERSIONS` array in `build.sh` to include/exclude versions.

## Files

- `Dockerfile` - Multi-stage Docker build
- `requirements.txt` - Additional Python dependencies
- `build.sh` - Build script for multiple versions
- `.dockerignore` - Docker ignore patterns

## License

This project is released under the Unlicense. See [LICENSE](LICENSE) for details.