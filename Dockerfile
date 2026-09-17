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

# Hetzner can temporarily return null resource references while a server is
# being created, migrated, or restored. The collection otherwise crashes on
# fields such as server.location.name instead of returning null.
COPY patches/patch_hetzner_hcloud.py /tmp/patch_hetzner_hcloud.py
RUN python /tmp/patch_hetzner_hcloud.py && rm /tmp/patch_hetzner_hcloud.py

# Remove build dependencies to keep image small
RUN apk del build-base libffi-dev openssl-dev

# Switch back to ansible user
USER ansible

# Default command
CMD ["ansible", "--version"]
