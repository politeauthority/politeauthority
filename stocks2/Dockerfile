FROM debian:jessie
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    git \
    python-pip \
    python \
    python-mysqldb

RUN mkdir /data/ && \
    cd /opt/ && \
    git clone https://github.com/politeauthority/politeauthority.git && \
    cd politeauthority && \
    python setup.py build && \
    python setup.py install && \
    pip install -r stocks2/requirements.txt && \
    cd /opt/politeauthority/stocks2/

ENV PA_MYSQL_HOST="Host"
ENV PA_MYSQL_USER="User"
ENV PA_MYSQL_PASS="Pass"
ENV PA_BASE_LOGGING_DIR='/data/logs'
ENV PA_BUILD="dev"
ENV PA_APP_DATA_PATH="/data/"
ENV TZ=America/Denver

VOLUME /opt/politeauthority/
VOLUME /data/

EXPOSE 80
EXPOSE 5000
