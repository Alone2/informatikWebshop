FROM python:3.8

WORKDIR /usr/src/webshop

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "app.py", "True"]
