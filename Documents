# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /home/geekhunter

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/home/geekhunter

# # create the geekhunter user
# RUN addgroup -S geekhunter && adduser -S geekhunter -G geekhunter
# RUN addgroup geekhunter root

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# # chown all the files to the app user
# RUN chown -R geekhunter:geekhunter $APP_HOME

# # change to the geekhunter user
# USER geekhunter
