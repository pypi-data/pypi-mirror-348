FROM python:3.10-slim

ARG USERNAME=dev
ARG UID=1000
ARG GID=1000
ARG IMG_NAME=rox_vectors

# Set environment variables to ensure scripts in non-interactive mode don't stop for user input
ENV DEBIAN_FRONTEND=noninteractive

# Create the user
RUN groupadd --gid $GID $USERNAME \
    && useradd --uid $UID --gid $GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# dialout group
RUN usermod -a -G dialout $USERNAME

# install packages
RUN apt-get install -y \
    locales \
    tree \
    git \
    make \
    iputils-ping

# cleanup
RUN rm -rf /var/lib/apt/lists/*

# set locale
RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8
RUN locale-gen en_US.UTF-8

# install requirements
WORKDIR /root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

#-----------------DEV user-----------------

USER ${USERNAME}
RUN echo 'export PS1="🐳  \[\033[1;36m\]'"rox-vectors"' \[\e[33m\]\W\[\e[m\] \[\033[1;36m\]# \[\033[0m\]"' >> ~/.bashrc

# add local bin to path
RUN echo "export PATH=\$PATH:/home/${USERNAME}/.local/bin" >> ~/.bashrc
ENV PATH="${PATH}:/home/${USERNAME}/.local/bin"


WORKDIR /home/${USERNAME}

# setup folders for saving vscode extensions
# https://code.visualstudio.com/remote/advancedcontainers/avoid-extension-reinstalls
RUN mkdir -p /home/$USERNAME/.vscode-server/extensions \
    && chown -R $USERNAME \
    /home/$USERNAME/.vscode-server



# build timestamp
USER root
RUN echo rox-vectors >> /build_date.txt && \
    date >> /build_date.txt

USER ${USERNAME}
WORKDIR /home/${USERNAME}
