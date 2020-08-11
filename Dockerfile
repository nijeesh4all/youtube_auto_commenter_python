FROM python:3.8-slim

ADD . ./myapp
WORKDIR /myapp


COPY handler.py .
COPY .env .

RUN pip3 install -r requirements.txt


CMD ["python3","handler.py"]