FROM python:3.8

WORKDIR /usr/src/webshop

COPY . .

RUN pip install .

EXPOSE 8080

CMD [ "python", "-m", "webshop", "True" ]
