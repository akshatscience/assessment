

1. **Create and activate a virtual environment**:
```powershell
go to your desired directory and type below command to set up virtual environment with name env
python -m venv env
to activate the created virtual environment use below command
.env\Scripts\Activate
```

2. **Install dependencies**:
```powershell
install all the dependencies inside virtual env
pip install -r requirements.txt
```

3. **Add environment variables**
- Create a `.env` file in the project root.
```
SECRET_KEY='your_supabse_db_secret_key'
API_KEY='your_weather_api_key'
DEBUG=True
DB_NAME='your_db_name'
DB_USER='your_db_user'
DB_PASSWORD='your_db_password'
DB_HOST='your_db_host'
DB_PORT='5432'
```

4. **Run migrations and start the dev server**:
```powershell
python manage.py migrate
python manage.py makemigrations
python manage.py runserver
```

## Notes
- Ensure your settings.py loads the `.env` file by using load_dotenv().
