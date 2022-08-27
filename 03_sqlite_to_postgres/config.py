import os

from dotenv import load_dotenv

load_dotenv()

#  postgres
dsn = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
    'dbname': os.environ.get('DB_NAME')
}

#  sqlite
db_path = 'db.sqlite'
