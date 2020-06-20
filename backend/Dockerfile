FROM python:3.8-alpine
#https://github.com/trstringer/python-flask-docker-compose-debugging
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

#these are for Pillow
RUN apk --no-cache add build-base python3-dev jpeg-dev zlib-dev freetype-dev
WORKDIR /thiccflask

RUN mkdir lastfm_images
# Copy in requirements.txt first so changing the source
# code doesn't require these steps to run again
COPY requirements.txt .
COPY setup.py .
RUN pip install --upgrade pip && pip install --no-cache-dir  -U -r requirements.txt
COPY fonts/ .


COPY . .

# CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "src.main:app"]