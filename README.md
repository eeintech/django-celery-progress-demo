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
> :warning: Celery will try to connect to a local redis server as defined in [celery_progress_demo/celery.py](https://github.com/eeintech/django-celery-progress-demo/blob/b3bec3c0f11b1f382e87d22b5d7818051ba0a8ca/celery_progress_demo/celery.py#L11) file. If it is not able to connect, it will show an error. To install and run redis, check out their [installation guide](https://redis.io/docs/getting-started/installation/), or [read this](https://eeinte.ch/stream/progress-bar-django-using-celery/#step-1) if you are running this demo on a shared hosting server.

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
