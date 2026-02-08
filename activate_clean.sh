#!/usr/bin/env bash

deactivate 2>/dev/null

# Remove ROS-related Python environment variables *for this shell only*
# This prevents ROS from injecting its Python packages into the venv.
unset PYTHONPATH PYTHONHOME

source "$(dirname "$0")/.venv_clean/bin/activate"
echo "Clean venv active: $(which python)"