FROM alpine:latest

RUN apk update
RUN apk add --no-cache \
    python3 \
    py3-pip 

ADD ./ /usr/src/app
WORKDIR /usr/src/app/src

RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate --noinput
RUN python3 manage.py createsuperuser
