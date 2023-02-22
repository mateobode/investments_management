#pull official base image
FROM python:3.10-slim

#set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

#set work directory
WORKDIR /usr/src/app

#install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

##copy entrypoint.sh
#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

#copy project
COPY . /usr/src/app

#run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

#run project through cli
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]