# api-cars
Netguru recruitment task - REST API for cars.

## Description
API contains 4 enpoints:
* GET /cars - get cars from application database with their current average rate
* POST /cars - add a new car, but only if car exists in: https://vpic.nhtsa.dot.gov/api/
* POST /rate - add a new rate for cat with values from 1 to 5
* GET /popular - get cars from application database order by number of rates

To quickly test API, please check out the [Links](#Links)

To create your own instance with docker: [Run with docker](#Run with docker)

For more information about API and used technologies: [Information](#Information)

## Links
`<API-Doc>` : https://redoc/ <br />
`<swagger>` : https://swagger/

## Run with docker

### Requirements
`<Docker>` : https://docs.docker.com/engine/install/ubuntu/ <br />
`<docker-compose>` : https://docs.docker.com/compose/install/

### Quick Run
1. Clone or Download code form this repo
2. Move to the catalog with Dockerfile and docker-compose.yml
3. Run: ***sudo docker build .***
4. Run: ***sudo docker-compose up***
5. The application will be serving on __127.0.0.1:8000__

Now you are ready to try it out!

If you do not have a Docker but you want to quickly get it running - just use a typical python venv and install modules from requirements.txt, given in main catalog.

### Env configuration
There is a list of environment variables, that app is using and you may change them.
You can find them in _.env.dev_ file. ****Defualt values are prepared for devs not for a production!****

List of env variables with short description :
* DEBUG - 1 for true, 0 for false
* SECRET_KEY - Key that helps pbkdf2 algorithm keep passwords safety
* DJANGO_ALLOWED_HOSTS - hosts that can use an app (like 127.0.0.1)
* SQL_ENGINE - Which database do we use (for it is postgres - django.db.backends.postgresql)
* SQL_DATABASE - Database name
* SQL_USER - Database user
* SQL_PASSWORD - User password
* SQL_HOST - Database host
* SQL_PORT - Database port


### Unit tests
I prepared some unit tests (using TDD).

Run tests: *_sudo docker-compose exec web python src/manage.py test api_*

## Information
As it had been written in the task, app was created in Python with my favourite web framework - Django.

Libraries used in the app:
* [Django REST framework](https://www.django-rest-framework.org/) - powerful toolkit for creating Web APIs
* [Requests](https://pypi.org/project/requests/) - easy to use module for sending requests (I used it to connect with https://vpic.nhtsa.dot.gov/api/)
* [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) - for me it is the best option for API documentation and for easy testing. Everytime when I work with people who will need my API I show them swagger and show how to use it.
* [psycopg2](https://pypi.org/project/psycopg2/) - the most popular PostreSQL database adapter. I chose postgres, because I use it everyday at my current work and I got to know well with that database.

