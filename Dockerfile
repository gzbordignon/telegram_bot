FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
RUN useradd -ms /bin/bash admin
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chown -R admin:admin /code
RUN chmod 755 /code
USER admin