# Django Starter - Ramailo

### Requirements
1. Make sure you have installed python3 [Recommended : Python 3.11.4]
2. Setup virtualenv
```
$ python3 -m venv venv
```
3. Activate virtualenv
```
source venv/bin/activate
```

### Run the app in terminal

1. Start a Postgres database server on your machine or in the cloud.
2. Set the values in env.uat as per .env.example file

```
$ make install
$ make createmigrations
$ make migrate
$ make dev
```

3. Setup a password to login to the Django admin dashboard.

```
make adminuser password=<choose-a-secure-password>
```

4. Create a new app. Run following from root folder

```
python manage.py startapp [app_name]

```

5. Start celery worker, beat and flower admin.

```
$ make worker
$ make beat
$ make flower password=<choose-a-secure-password>
```

### Make API calls against the server

1. Go to [http://localhost:8000/swagger](http://localhost:8000/swagger) to see Swagger documentation for API endpoints.
2. Run the APIs by clicking the "Try it now" button on the Swagger page.

2. Go to [http://localhost:8000/admin](http://localhost:8000/admin) and login to the dashboard using username `admin` and the password you chose in step 1 above.

### Run tests and check code coverage

```
$ make test
$ make coverage
```

### Lint your code

```
$ make lint
```

### Watch logs

```
Open logs.log file or console to monitor logs having different log level (e.g., INFO, DEBUG, ERROR).

Log Format: [LEVEL] [TIMESTAMP] [MODULE] [LINE_NUMBER] [MESSAGE]

- LEVEL: Represents the log level of the message, such as "INFO", "DEBUG", "WARNING", etc.
- TIMESTAMP: Represents the timestamp of the log message in the format "YYYY-MM-DD HH:MM:SS,sss".
- MODULE: Represents the name of the Python module where the log message originated.
- LINE_NUMBER: Represents the line number within the Python module where the log message originated.
- MESSAGE: Represents the actual log message content.

Example: [INFO] [2023-07-12 12:34:56,789] [my_module] [42] [This is an example log message]
