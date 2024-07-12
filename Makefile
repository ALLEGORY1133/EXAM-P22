mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
admin:
	python3 manage.py createsuperuser

celery:
	celery -A root worker -l INFO

beat:
	celery -A root beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler