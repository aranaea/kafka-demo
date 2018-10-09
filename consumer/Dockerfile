FROM jazzdd/alpine-flask:latest

COPY requirements.txt /app
COPY ./src /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

VOLUME /app

CMD ["-d"]
