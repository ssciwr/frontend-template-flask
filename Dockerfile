FROM ubuntu:22.04

# python 3.10 is included by default 
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install --no-install-recommends -y \
        python3-pip \
    && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN useradd --create-home myuser
USER myuser
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]