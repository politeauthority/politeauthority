FROM debian:jessie
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    git \
    python-pip \
    python \
    python-mysqldb

RUN mkdir /tmp/politeauthority/ && \
    cd /opt/ && \
    git clone https://github.com/politeauthority/politeauthority.git && \
    cd politeauthority && \
    python setup.py build && \
    python setup.py install && \
    pip install -r stocks2/requirements.txt

ENV PA_MYSQL_HOST="Host"
ENV PA_MYSQL_USER="User"
ENV PA_MYSQL_PASS="Pass"
ENV PA_BASE_LOGGING_DIR='/tmp/politeauthority/logs'
ENV PA_BULD="dev"
ENV TZ=America/Denver

VOLUME /opt/politeauthority/
VOLUME /tmp/politeauthority/
VOLUME /var/log/politeauthority

EXPOSE 5000
CMD python /opt/politeauthority/stocks2/run.py
