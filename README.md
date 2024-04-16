Running the backend:

cd backend

create the data base schema wiht following command
python manage.py makemigrations app
python managepy migrate app
python managepy migrate

load the data.json(all the products) into the database(sqlite3) with the following command
python manage.py loaddata data.json

Now run the server with the commad
python manage.py runserver

Runnig the frontend

install all the packages with command
npm install

then run it with
npm start
