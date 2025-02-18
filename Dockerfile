# set base image python:3.10
FROM python:3.10

ENV PYTHONBUFFERED=1

# set environment variables
ARG SENTRY_DSN
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY
ENV SENTRY_DSN=$SENTRY_DSN

#set working directory
WORKDIR /OpenClassrooms_project13
COPY requirements.txt .
# install the requirements specified in file using RUN
RUN pip install -r requirements.txt
# copy all items in current local directory(source) to current container directory(destination)
COPY . .
# command to run when image is executed inside a container
CMD python manage.py collectstatic
CMD gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT
