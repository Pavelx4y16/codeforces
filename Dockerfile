FROM python:3.10.9-slim

LABEL maintainer='dl.gsu.by' \
      os='amazon linux 2' \
      language='Python'

ENV SERVICE_NAME="codeforces"
ENV SERVICE_HOME=/opt/$SERVICE_NAME \
    PORT=8080 \
    HOST="0.0.0.0"

RUN apt-get update
RUN pip install --upgrade pip

COPY codeforces ${SERVICE_HOME}/codeforces
COPY main.py ${SERVICE_HOME}
COPY settings.py ${SERVICE_HOME}
COPY start.sh ${SERVICE_HOME}
COPY requirements/common.txt ${SERVICE_HOME}/requirements.txt
COPY getpass.txt ${SERVICE_HOME}/getpass.txt

RUN mkdir ./logs

RUN pip3 install -r ${SERVICE_HOME}/requirements.txt
RUN chmod +x ${SERVICE_HOME}/start.sh

RUN apt-get clean all

WORKDIR ${SERVICE_HOME}

EXPOSE 8080

ENTRYPOINT ["/bin/bash"]
CMD ["start.sh"]