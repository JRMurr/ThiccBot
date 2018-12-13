FROM python:3.7-alpine
#https://github.com/trstringer/python-flask-docker-compose-debugging
EXPOSE 8000
WORKDIR /thiccflask
RUN apk update \
  && apk --no-cache add bash \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev
  
# Copy in requirements.txt first so changing the source
# code doesn't require these steps to run again
COPY requirements.txt .
COPY setup.py .
RUN pip install --no-cache-dir  -U -r requirements.txt

COPY . /app


CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "src.main:app"]
# CMD ls