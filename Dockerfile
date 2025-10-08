# Multi-stage build to reduce image size
FROM python:3.14-alpine3.22 AS builder

# Set build argument for Ansible version
ARG ANSIBLE_VERSION=latest

# Install system dependencies for building
RUN apk add --no-cache \
    git \
    build-base \
    libffi-dev \
    openssl-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt --break-system-packages

# Install Ansible
RUN if [ "$ANSIBLE_VERSION" = "latest" ]; then \
        pip install --no-cache-dir ansible --break-system-packages; \
    else \
        pip install --no-cache-dir ansible~=${ANSIBLE_VERSION}.0 --break-system-packages; \
    fi

# Runtime stage
FROM python:3.14-alpine3.22

# Install minimal runtime dependencies
RUN apk add --no-cache \
    bash \
    curl \
    git \
    openssh-client \
    && rm -rf /var/cache/apk/*

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/ansible* /usr/local/bin/

# Create ansible user with uid 1000
RUN adduser -D -u 1000 ansible && mkdir /workspace && chown -R ansible:ansible /workspace
 
# Set working directory
WORKDIR /workspace

# Switch to ansible user
USER ansible

# Default command
CMD ["ansible", "--version"]
