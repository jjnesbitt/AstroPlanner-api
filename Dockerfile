FROM python:3.6-alpine

COPY ./src ./requirements.txt /app/
WORKDIR /app

RUN apk add --update --no-cache gcc musl-dev linux-headers
RUN pip install uWSGI
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uwsgi", "--http", ":8000", "--wsgi", "wsgi", "-p", "5"]
