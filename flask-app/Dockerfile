FROM python:3.10.2

WORKDIR /flask-app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

CMD [ "sh", "-c", "flask run -h 0.0.0.0 -p 5000" ]
