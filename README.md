# Django Celery-Progress Demo
This is demo application built on Django for [celery-progress](https://github.com/czue/celery-progress).

Check out my [step-by-step guide](https://eeinte.ch/stream/progress-bar-django-using-celery/) on how-to setup your own progress bar!

To get started using this demo:
1. Clone this repo
2. Create and/or activate your Python environment:
```
$ python3 -m venv python3-env
$ source python3-env/bin/activate
```
3. Install the required packages:
```
(python3-env) $ pip install -r requirements.txt
```
4. Apply Django migrations and start server:
```
(python3-env) $ ./manage.py migrate
(python3-env) $ ./manage.py runserver
```
5. In a different terminal window, start your message broker server then start Celery:
```
(python3-env) $ ./start_celery
```
6. Go to http://localhost:8000/ and have fun!

## Screenshots
### Start task
![init](media/init.png)

### Task in-progress
![progress](media/progress.png)

### Task completed
![success](media/success.png)

### Task failed
![success](media/error.png)
