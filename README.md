# Hotel content provider

Object of this task is to create interface for hotel owners to add their hotels and create a REST API for agents which allows them to book available rooms in hotels.
Hotel owners can:
  - Register
  - Login
  - Add/delete hotel
  - Update information about hotel
  - Get list of his hotels

Agent can:
  - Get list of available room in hotels 
  - Filter results with date or coordinates
  - Иook a room
  - Get list of agent bookings

  
## Project deployed on DigitalOcean
http://68.183.9.108/

## Deploy on your local machine
1. Install requirements
`pip install -r requirements.txt`
2. Database settings
Create .env file and edit it
`SECRET_KEY=Your_secret_key`
3. Postgres settings
Set your db settings in .env
`DB_NAME=database_name`
`DB_USER=user`
`DB_PASS=password`
4. Make migrations
`python manage.py makemigrations`
`python manage.py migrate`
5. Create superuser
`python manage.py createsuperuser`
6. Start project
`python manage.py runserver`
