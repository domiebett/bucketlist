[![Build Status](https://travis-ci.org/DomieBett/bucketlist.svg?branch=develop)](https://travis-ci.org/DomieBett/bucketlist) [![Coverage 
Status](https://coveralls.io/repos/github/DomieBett/bucketlist/badge.svg?branch=develop)](https://coveralls.io/github/DomieBett/bucketlist?branch=develop)

# Bucket List Api.
This is an application web api application used to store user bucketlist. People often have things they wish to 
do before they pass on. This application gives them space to document these things and see how much they have achieved.
It's backend is written in flask and its front end in angular js.

## Setting up.

You need to have installed python on your system. If you haven't, you can install it from [here](https://www.python.org/downloads/)
This version comes with an inbuilt pip package installer.
You also need to install postgres database. You can install it from [here](https://www.postgresql.org/download/)

### Install virtualenv

> ``` pip install virtualenv ```

### Create a postgres database. Go to terminal and:

> ``` psql ```

If you get an error stating your username doesnt exist:

> ``` sudo -u postgres -i ``` then ``` psql ``` once again

> ``` CREATE ROLE flask WITH LOGIN; ```

> ``` CREATE DATABASE bucketlist_api OWNER flask; ```

### Create a folder named webapps in your home directory and navigate into it.

> ``` mkdir ~/webapps ```

>``` cd ~/webapps ```

### Create a virtual environment for this project and activate it.

> ``` virtualenv --python=python3 bucket_venv ```

> ``` source bucket_venv/bin/activate ```

### Clone this repo.

> ``` git clone https://github.com/DomieBett/bucketlist.git ```

### Navigate into project folder.

> ``` cd bucketlist ```

### Install requirements.

> ``` pip install -r requirements.txt ```

### Run the database_migrations.

> ``` python manage.py db init ```

> ``` python manage.py db migrate ```

> ``` python manage.py db upgrade ```

### Run the server

> ``` python manage.py runserver ```

You can now access the api at the url http://127.0.0.1:5000

## Author:

Dominic Kipchumba Bett.
