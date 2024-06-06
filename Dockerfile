FROM python:3.11.9-alpine

WORKDIR /blueray

COPY . .
RUN apk update && apk add postgresql-client
RUN chmod +x wait-for-postgres.sh
RUN pip install -r requirements.txt
