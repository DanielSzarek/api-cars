release: python ./src/manage.py migrate
web: python ./src/manage.py collectstatic --no-input; gunicorn --pythonpath src cars.api