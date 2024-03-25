import os

import dj_database_url
SECRET_KEY = os.environ.get("SECRET_KEY")



ALLOWED_HOSTS = [
    '*',
]

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get("DB_URL"), conn_max_age=600)
}

