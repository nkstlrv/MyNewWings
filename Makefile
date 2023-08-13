run:
	python app/manage.py runserver

migrate:
	python app/manage.py migrate


makemigrations:
	python app/manage.py makemigrations

shell:
	python app/manage.py shell_plus --print-sql

celery:
	cd app && celery -A settings worker -l INFO --autoscale=0,10

beat:
	cd app && celery -A settings beat -l INFO