# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /home/geekhunter

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP=/home/geekhunter
ENV APP_HOME=/home/geekhunter/web

# # create the geekhunter user
RUN addgroup -S geekhunter && adduser -S geekhunter -G geekhunter
# RUN addgroup geekhunter root
# Create all required directories:
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

# # # chown all the files to the app user
# RUN chown -R geekhunter:geekhunter $APP_HOME

# # # change to the geekhunter user
# USER geekhunter
