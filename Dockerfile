FROM python:3.12-alpine

RUN mkdir /dream_job

WORKDIR /dream_job

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "link_manager_site.wsgi:application"]
