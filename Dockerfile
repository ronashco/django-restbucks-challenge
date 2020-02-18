FROM python:3-alpine

# Install dependencies required for psycopg2 python package
RUN apk update && apk add libpq
RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

RUN pip install --no-cache-dir -r requirements.txt

# Remove dependencies only required for psycopg2 build
RUN apk del .build-deps

EXPOSE 8000

CMD ["gunicorn", "restbucks.wsgi", "0:8000"]
