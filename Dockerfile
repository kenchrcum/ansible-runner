# Build Ansible version-specific image from base
FROM kenchrcum/ansible-runner:base

# Set build argument for Ansible version
ARG ANSIBLE_VERSION=latest

# Install Ansible (need to switch to root temporarily for pip install)
USER root

# Install Ansible
RUN if [ "$ANSIBLE_VERSION" = "latest" ]; then \
        pip install --no-cache-dir ansible --break-system-packages; \
    else \
        pip install --no-cache-dir ansible~=${ANSIBLE_VERSION}.0 --break-system-packages; \
    fi

# Remove build dependencies to keep image small
RUN apk del build-base libffi-dev openssl-dev

# Switch back to ansible user
USER ansible

# Default command
CMD ["ansible", "--version"]
