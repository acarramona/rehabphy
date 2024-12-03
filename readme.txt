Instructions:
STEP 1:
    - Create a database in the sqlserver.
    - Database name is rehabphydb
    - Execute the schema.sql script provided against the sqlserver
    - Update the .env file to reflect the url or host of your sqlserver
STEP 2:
    - cd Rehabphy
	- Activate the virtual env
	-   .\venv\Scripts\activate
	- OR
	- source .venv/bin/activate
  

SETP 2:
    - Run the migrations 
        : python manage.py makemigrations
        : python manage.py migrate
    - Start the application server
        : python manage.py runserver


    
    - Physio Team can signup via the link:
        http://127.0.0.1:8000/accounts/signup/physio-team/

    - Once a user is registered they can login.
        http://127.0.0.1:8000/home

