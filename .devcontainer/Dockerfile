FROM nvcr.io/nvidia/pytorch:25.03-py3

ARG USER_NAME
ARG USER_UID
ARG USER_GID

# Create the user
RUN if getent passwd $USER_UID > /dev/null; then \
        userdel -r $(getent passwd $USER_UID | cut -d: -f1) 2>/dev/null || true; \
    fi \
    && groupadd --gid $USER_GID $USER_NAME 2>/dev/null || true \
    && useradd --uid $USER_UID --gid $USER_GID -m $USER_NAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo -e "\n$USER_NAME ALL=(ALL) NOPASSWD:ALL\n" >> /etc/sudoers

# Set the default user.
USER $USER_NAME
