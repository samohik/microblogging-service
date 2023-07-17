FROM python:3.11

RUN pip3 install --upgrade pip

ADD requirements.txt Flask/

RUN pip install -r Flask/requirements.txt

COPY Flask/ /Flask

EXPOSE 5000