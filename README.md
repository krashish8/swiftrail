# SwiftRail

This is the repository for the ITW-II Project at IIT (BHU) Varanasi - SwiftRail (Railway Management System).


## Setting up Development Environment

 - Make sure `python3.7` and `pip` are installed. Install `pipenv` by running `pip install pipenv`.
 - Install python dependencies using the command `pipenv install --ignore-pipfile` Please use only pipenv for managing dependencies (Follow this [link](https://realpython.com/pipenv-guide/) if you are new to pipenv).
 - To activate this project's virtualenv, run `pipenv shell`.
 - Alternatively, run a command inside the virtualenv with `pipenv run`.

## Running the project

 - Create database `swiftrail` using the command `CREATE DATABASE swiftrail;` by logging in to `MySQL`.
 - <b>Copy</b> `my.cnf.example` as `my.cnf` and enter the `username` of the MySQL User in `<username>` and `password` in `<password>`.
 - Run `python manage.py makemigrations` for creating new migrations
 - Run `python manage.py migrate` to apply migrations.
 - Run `python script.py` to update data in the database.
 - Start the development server using `python manage.py runserver`.

## Tools and Technologies

 - Django
 - MySQL
 - Django Social Auth
 - Instamojo API
 - Indian Rail API
