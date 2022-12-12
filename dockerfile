FROM python:3.9
 
ENV PYTHONUNBUFFERED 1
 
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
 
WORKDIR /app
COPY ./app /app
 
EXPOSE 8000