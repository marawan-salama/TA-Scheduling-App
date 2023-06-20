# Project 891
> Manage TA assignments for the entire department.

## Installation
### 1. Apply Migrations
Apply the initial migrations:

`python3 manage.py migrate`


### 2. Create the Superuser
Create a superuser:

`python3 manage.py createsuperuser`


### 3. Populate the Database (Optional)
Add test data to the database using the `populate.py` script:

`python3 manage.py shell`
```py
>>> exec(open('populate.py').read())
```


### 4. Run the Server
`python3 manage.py runserver`
