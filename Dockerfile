FROM python:3.9-alpine3.13

LABEL maintainer="Mellvin"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# dir in which all commands will be run, so obvs should have the django and manage.py
WORKDIR /app 
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        #tells docker not to createa home dir
        --no-create-home \
        #specifies name of the user.
        django-user 

ENV PATH="/py/bin:$PATH"

#switching to this user so that it isn't ran as root.
USER django-user
