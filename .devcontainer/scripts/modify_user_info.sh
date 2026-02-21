#!/bin/bash

# get current user's UID and GID
CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)

# update USER_UID and USER_GID values in devcontainer_base.json file
DEVCONTAINER_JSON="./.devcontainer/devcontainer_base.json"

if [ -f "$DEVCONTAINER_JSON" ]; then
    echo "updating $DEVCONTAINER_JSON file..."
    
    # use sed to replace USER_UID and USER_GID values
    sed -i "s/\"USER_UID\": \"\${localEnv:USER_UID}\"/\"USER_UID\": $CURRENT_UID/g" "$DEVCONTAINER_JSON"
    sed -i "s/\"USER_GID\": \"\${localEnv:USER_GID}\"/\"USER_GID\": $CURRENT_GID/g" "$DEVCONTAINER_JSON"
    
    echo "successfully updated devcontainer_base.json file:"
    echo "  USER_UID: $CURRENT_UID"
    echo "  USER_GID: $CURRENT_GID"
else
    echo "warning: $DEVCONTAINER_JSON file not found"
fi
