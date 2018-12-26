FROM python:3.7-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git \
    && apk add --virtual build-deps gcc python3-dev g++ make

WORKDIR /thiccbot
RUN pip install -U setuptools

# Copy in requirements.txt first so changing the source
# code doesn't require these steps to run again
COPY requirements.txt .
COPY setup.py .
RUN pip install -U -r requirements.txt

COPY . ./src

# CMD python main.py
