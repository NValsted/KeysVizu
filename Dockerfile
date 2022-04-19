FROM ubuntu:20.04

RUN apt update -yq && apt install software-properties-common -yq
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -yq \
    python3.9 \
    python3.9-distutils \
    python3-pip

RUN ln -s /usr/bin/python3.9 /usr/bin/python

RUN apt-get update -yq && apt-get install -yq \
    curl \
    build-essential \
    python3.9-dev \
    python3.9-venv \
    python3-setuptools \
    ffmpeg \
    libsm6 \
    libxext6

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py

RUN curl -sSL https://install.python-poetry.org | python3.9 -
ENV PATH=/root/.local/bin:$PATH

COPY pyproject.toml /pyproject.toml
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip3 install -r requirements.txt

WORKDIR /KeysVizu
ENTRYPOINT [ "python", "main.py" ]
