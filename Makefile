all:
	@echo "Available commands: \n\
		make installdeps : to install poetry and other dependent packages\n\
		make createmigrations: generate the migration files for defined models \n\
		make install : to install poetry, other dependent packages, and create migrations \n\
		make migrate : creates tables in database \n\
		make adminuser : creates a superuser to access the django admin \n\
		make rundb: runs postgres server in dockerized enviroment
		make dev : runs django development server \n\
		make run : run the django application \n\
		make shell : start a poetry shell with all required packages available in the environment \n\
		make lint : runs linters on all project files and shows the changes \n\
		make test : run the test suite  \n\
		make coverage : runs tests and creates a report of the coverage \n\
		make update : sync pyproject.toml with poetry.lock file \n\
	"

installdeps:
	python3 -m pip install poetry
	poetry install

createmigrations:
	poetry run python manage.py makemigrations

install: installdeps createmigrations

migrate:
	poetry run python manage.py migrate

dev:
	poetry run python manage.py runserver 0.0.0.0:8000

worker:
	poetry run celery -A project.celery worker --loglevel=info

beat:
	poetry run celery -A project beat --loglevel=info

flower:
	test $(password) || (echo '>> password is not set. (e.g password=mysecretpassword)'; exit 1)
	@echo 'creating Flower admin user'
	poetry run celery -A project.celery flower --address=0.0.0.0 --port=5555 --basic_auth=admin:$(password)

run:
	export DJANGO_SETTINGS_MODULE='project.settings';\
	poetry run gunicorn project.wsgi:application --bind localhost:8000

rundb:
	poetry run docker-compose up db

shell:
	@echo 'Starting poetry shell. Press Ctrl-d to exit from the shell'
	poetry shell
	poetry run python manage.py shell

lint:
	@echo '---Running autopep8---'
	poetry run autopep8 ramailo -r -d
	poetry run autopep8 ramailo -r -i
	poetry run isort ramailo

coverage:
	@echo 'Running tests and making coverage files'
	poetry run coverage run manage.py test
	poetry run coverage report
	poetry run coverage html
	@echo 'to see the complete report, open ./htmlcov/index.html on the htmlcov folder'

adminuser:
	test $(password) || (echo '>> password is not set. (e.g password=mysecretpassword)'; exit 1)
	@echo 'creating Django admin user'
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
	User.objects.create_superuser('admin', '', '$(password)')" \
	| poetry run python manage.py shell
	@echo 'Username: admin , Password: $(password)'

test:
	@echo 'Running tests'
	poetry run pytest --reuse-db -vv --durations=10 $(module)

update:
	poetry lock --no-update