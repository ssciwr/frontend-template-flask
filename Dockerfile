FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install --no-install-recommends -y \
        python3.9 \
        python 3.9-dev \
        python3-pip \
    && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]