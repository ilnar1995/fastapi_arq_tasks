FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN mkdir /fast_api_project
WORKDIR /usr/fast_api_project

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -yyq ncat
RUN pip install -r requirements.txt

COPY . .

COPY arq /usr/local/lib/python3.8/site-packages/arq
COPY arq_dashboard /usr/local/lib/python3.8/site-packages/arq_dashboard
RUN rm -rf /usr/fast_api_project/arq
RUN rm -rf /usr/fast_api_project/arq_dashboard

#CMD ["python", "base.py"]
COPY /docker/entrypoint.sh .
#RUN chmod +x ./entrypoint.sh
#RUN chmod +x ./entrypoint-celery.sh


EXPOSE 8000
#FROM python:3.8
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
## install psycopg2 dependencies
#RUN mkdir /usr/fast_api_project
#WORKDIR /usr/fast_api_project
#
#COPY requirements.txt .
#COPY pyproject.toml .
#
#RUN apt-get update \
#    && apt-get install -yyq ncat
#
#
#RUN pip install --upgrade pip \
#    && pip install -r requirements.txt \
#
#
#COPY . .
#
##CMD ["python", "base.py"]
#RUN chmod a+x docker/*.sh
## COPY ./entrypoint.sh .
##RUN chmod +x ./entrypoint-celery.sh
#
## EXPOSE 8000
## ENTRYPOINT ["/usr/src/django_project/entrypoint.sh"]
##EXPOSE 8000
##CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#
