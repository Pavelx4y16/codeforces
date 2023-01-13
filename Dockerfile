FROM python:3.10.9-slim

LABEL maintainer='dl.gsu.by' \
      os='amazon linux 2' \
      language='Python'

ENV SERVICE_NAME="codeforces"
ENV SERVICE_HOME=/opt/$SERVICE_NAME \
    PORT=8080 \
    HOST="0.0.0.0"

WORKDIR ${SERVICE_HOME}

RUN apt-get update
RUN pip install --upgrade pip

RUN mkdir logs

COPY codeforces codeforces
COPY main.py .
COPY settings.py .
COPY start.sh .
COPY requirements/common.txt requirements.txt
COPY getpass.txt getpass.txt


RUN pip3 install -r requirements.txt
RUN chmod +x start.sh

RUN apt-get clean all


EXPOSE 8080

ENTRYPOINT ["/bin/bash"]
CMD ["start.sh"]