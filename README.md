# FabLab

1.Grab a copy of the project.

    git clone new_project.git

2.Create a virtual environment and install dependencies.

    mkvirtualenv new_project
    or
    virtualenv new_project (in mac)
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




#DONE:

      1- Display materials

      2- Pagination

      3- User Levels

      4- Create a Loan

      5- Add materials to the loan

        5.1- Display list of materials on Loan

        5.2- Modify quantity of material

            -if type of material is UNIQUE: quantity cannot be modified

      6- Add Loaner and expected Return Date to the Loan

      7- Create Type/Material/Loaner

      8- Display all Type/Material/Loaner on a table

      9- Modify Loaner
      
      10- Change Password
    
      11- Forget Password
      
      12 - Display Loans

#TO DO:

    1- Modify Material/Type
    
    2- Delete Type/Material/Loaner
    
    3- Mark as Returned Loans
    
    4- Delete Loans
    
    
    
