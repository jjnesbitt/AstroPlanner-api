#FROM python:3.6-alpine
FROM alpine:3.7

COPY ./src ./requirements.txt /app/
WORKDIR /app

RUN apk add --update --no-cache python3 python3-pip uwsgi-python3
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uwsgi --http :8000 --wsgisrc/wsgi.py"]
