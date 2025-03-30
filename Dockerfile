FROM python:3.11.10

WORKDIR /backend
ADD . /backend
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/bash", "start.sh"]
