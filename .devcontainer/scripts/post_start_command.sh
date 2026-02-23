#!/bin/bash
set -e

# Create ~/.ssh directory with correct permissions
mkdir -p /root/.ssh
chmod 700 /root/.ssh
# Copy .ssh files from /workspaces/.ssh to ~/.ssh and set permissions
if [ -d /workspaces/.ssh ] && [ "$(ls -A /workspaces/.ssh 2>/dev/null)" ]; then
  cp -ra /workspaces/.ssh/. /root/.ssh/
fi
# Set ownership and permissions for .ssh
chown -R root:root /root/.ssh
chmod 700 /root/.ssh
find /root/.ssh -type f -exec chmod 600 {} \; 2>/dev/null || true
# Copy .gitconfig from /workspaces/.gitconfig to ~/.gitconfig
if [ -f /workspaces/.gitconfig ]; then
  cp -a /workspaces/.gitconfig /root/.gitconfig
  chown root:root /root/.gitconfig
fi

# Initialize uv environment
cd /workspaces/CapriLLM
uv venv
# Install dependencies
uv sync
# Activate uv environment
source /workspaces/CapriLLM/.venv/bin/activate
