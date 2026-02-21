FROM nvcr.io/nvidia/pytorch:25.03-py3

ARG USER_NAME
ARG USER_UID=1000
ARG USER_GID=1000

ENV USER_HOME=/home/$USER_NAME

# create user
RUN set -eux; \
    # check and delete user
    if getent passwd "$USER_NAME"; then \
        userdel -r "$USER_NAME"; \
    fi; \
    # check and delete user by UID
    if getent passwd "$USER_UID"; then \
        userdel -r $(getent passwd "$USER_UID" | cut -d: -f1); \
    fi; \
    # create group and user
    if ! getent group "$USER_GID"; then \
        groupadd --gid "$USER_GID" "$USER_NAME"; \
    fi; \
    useradd --uid "$USER_UID" --gid "$USER_GID" -m "$USER_NAME";

# install sudo
RUN apt-get update; \
    apt-get install -y sudo; \
    # configure sudo permissions
    echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/"$USER_NAME"; \
    chmod 0440 /etc/sudoers.d/"$USER_NAME";

USER $USER_NAME

# create project directory
RUN mkdir -p $USER_HOME/CapriLLM

# install uv
RUN curl -LsSf https://gitee.com/wangnov/uv-custom/releases/download/0.10.4/uv-installer-custom.sh | sh \
    && source $USER_HOME/.local/bin/env
