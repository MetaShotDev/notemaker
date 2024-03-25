import os

import dj_database_url
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")



ALLOWED_HOSTS = [
    '*',
]

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DB_URL"), conn_max_age=600)
}

