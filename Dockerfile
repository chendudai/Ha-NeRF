ARG UBUNTU_VER=16.04
ARG CONDA_VER=latest
ARG OS_TYPE=x86_64


FROM nvidia/cuda:11.0.3-base-ubuntu${UBUNTU_VER}


# System packages 
RUN apt-get update && \
    apt-get install -yq curl wget jq vim git && \
    apt-get install openssh-server sudo -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use the above args during building https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG CONDA_VER
ARG OS_TYPE
# Install miniconda 
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path
ENV PATH=${CONDA_DIR}/bin:${PATH}
COPY environment.yml .
RUN conda env update --file environment.yml --name base

# clone repo and cd to a directory where the main is:
COPY clone_repo_and_run_python_scripts.sh .
ENTRYPOINT ["bash", "clone_repo_and_run_python_scripts.sh"]
