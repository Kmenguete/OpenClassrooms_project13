# set base image python:3.10
FROM python:3.10

ENV PYTHONBUFFERED=1
#set working directory
WORKDIR /OpenClassrooms_project13
COPY requirements.txt .
# install the requirements specified in file using RUN
RUN pip install -r requirements.txt
# copy all items in current local directory(source) to current container directory(destination)
COPY . .
# This command release port 8000 within the container, where the Django app will run
EXPOSE 8000
# command to run when image is executed inside a container
CMD ["python", "manage.py", "collectstatic", "--noinput"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "oc_lettings_site.wsgi:application"]
