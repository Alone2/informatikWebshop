# Informatik Webshop

**Important: Do not use the instuctions below for deployment; they are only suitable for testing**

## Run using Docker 

1. Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) (available in most package managers)
1. Clone this repo using git
2. Run ```docker-compose build``` and ```docker-compose up``` inside the folder you just cloned

## Run on Local Machine
1. Clone this repo using git
2. Setup a mysql server using ```database/setupDatabase.sql``` and use the password ```ef21``` for root
3. Install requirements using ```pip install -r webshop/requirements.txt``` (use python3.8)
4. Run ```cd webshop && python app.py```
