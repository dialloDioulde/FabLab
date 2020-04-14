# FabLab

1.Grab a copy of the project.

git clone new_project.git

2.Create a virtual environment and install dependencies.

mkvirtualenv new_project
pip install -r requirements.txt

3.Duplicate new_project/new_project/local_settings_example.py and save as local_settings.py.

4. Enter your database settings in local_settings.py.

5. Initialize your database.

python ./manage.py syncdb
python ./manage.py migrate
If your app has a custom user model, you'll need to create a new superuser for the admin.

python ./manage.py createsuperuser

6.Run the development server to verify everything is working.

python ./manage.py runserver
