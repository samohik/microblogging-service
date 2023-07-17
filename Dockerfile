FROM python:3.11

RUN pip3 install --upgrade pip

ADD requirements.txt FastApi/

RUN pip install -r FastApi/requirements.txt

COPY FastApi/ /FastApi

EXPOSE 8000

WORKDIR FastApi/

