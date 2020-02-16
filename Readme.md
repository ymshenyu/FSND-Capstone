# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting started

### Installing dependencies
* Install [Python 3](python.org/downloads/)
* Creat virtual environment by following the [tutorial](https://docs.python.org/3/tutorial/venv.html) (optional)
* Install project dependencies via pip: 
 ```bash
 $ pip install -r requirements.txt
 ```
* Install postgresql

### Runing the server
Each time you open a new terminal session, run:
```bash
$ source setup.sh
```
This will setup the environment variables include database URL, three different tokens based on different roles.

Then create the database and run local migrations:
```bash
$ createdb casting_agency
$ python manage.py db upgrade
```
To run the production server, execute the command below:
```bash
$ python app.py
```
If you want to run the development server:
```bash
$ export FLASK_ENV=development
$ python app.py
```

### About hosting
This project has been deployed to production using Heroku and can be found at this URL: https://guobang-fsnd-capstone.herokuapp.com/

### About roles
We currently have 3 different roles which are casting assistant, casting director, and executive producer. You can test the API endpoints with their token and you can see their permissions below.
#### Casting assistant
* ```read:information```
#### Casting director
* All permissions a Casting Assistant has
* ```create:actor```
* ```delete:actor```
* ```update:actor```
* ```update:movie```
#### Executive Producer
* All permissions a Casting Director has
* ```create:movie```
* ```delete:movie```

You can get the tokens [here](https://github.com/ymshenyu/FSND-Capstone/blob/master/setup.sh)

### API endpoints
* GET
    * ```/actors``` Returns all actors information in the database.
    * ```/movies``` Returns all movies information in the database.
    * ```read:information``` permission is needed.
* POST
    * ```/acotrs``` Add actor to database. ```create:actor``` permission is needed.
    * ```/movies``` Add movie to database. ```create:movie``` permission is needed.
* PATCH
    * ```/actors/id``` Update the specific actor information. ```update:actor``` permission is needed.
    * ```/movies/id``` Update the specific movie information.  ```update:movie``` permission is needed.
* DELETE
    * ```/actors/id``` Delete the specific actor information. ```delete:actor``` permission is needed.
    * ```/movies/id``` Update the specific movie information. ```delete:movie``` permission is needed.
### About test
#### Testing with unittest library
```bash
$ createdb casting_agency_test
$ python test_app.py
```