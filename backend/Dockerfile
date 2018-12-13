FROM python:3.7-alpine
#https://github.com/trstringer/python-flask-docker-compose-debugging
EXPOSE 8000
WORKDIR /thiccflask

# Copy in requirements.txt first so changing the source
# code doesn't require these steps to run again
COPY requirements.txt .

RUN pip install --no-cache-dir  -U -r requirements.txt

COPY . /app


CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "main:app"]
# CMD ls