FROM python:3.7-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git 

WORKDIR /thiccbot

# Copy in requirements.txt first so changing the source
# code doesn't require these steps to run again
COPY requirements.txt .

RUN pip install -U -r requirements.txt

COPY . ./src

CMD python main.py
