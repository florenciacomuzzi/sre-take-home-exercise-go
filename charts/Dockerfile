FROM quay.io/mongodb/charts:v1.20.2

LABEL maintainer="thepliable2@gmail.com"

RUN #apt-get update

ARG EMAIL
ARG PASSWORD

ENV EMAIL=${EMAIL} \
    PASSWORD=${PASSWORD}

COPY entrypoint.sh /usr/bin

ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]