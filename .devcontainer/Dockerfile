FROM nvcr.io/nvidia/pytorch:25.03-py3

ARG USER_NAME=yyk
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN if getent passwd $USER_UID > /dev/null; then \
        userdel -r $(getent passwd 1000 | cut -d: -f1) 2>/dev/null || true; \
    fi \
    && groupadd --gid $USER_GID $USER_NAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USER_NAME \
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME \
    && chmod 0440 /etc/sudoers.d/$USER_NAME

# # [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USER_NAME