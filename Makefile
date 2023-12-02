# Run Django development server
run:
	python manage.py runserver


#apply makemigrations
m1:
	python manage.py makemigrations

# Apply migrations
m2:
	python manage.py migrate

# Create a superuser
super:
	python manage.py createsuperuser

# Collect static files
static:
	python manage.py collectstatic



# Start a new app
app:
	python manage.py startapp


.PHONY: run m2 super static app  m1 
