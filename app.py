#app.py -- svarer til at køre en springboot fil

import os
from dotenv import load_dotenv
import MySQLdb
from flask import Flask
from routes.user_routes import user_bp
from db import get_db_connection
from test_data.dummy_users import dummy_users

# Load .env filen
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return "Velkommen til mit Flask API"

# Hent config fra miljøvariabler (som er indlæst fra .env)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

app.register_blueprint(user_bp, url_prefix="/users")


@app.route("/insert-dummy-users")
def insert_dummy_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        for user in dummy_users:
            cursor.execute("""
                           INSERT IGNORE INTO users (first_name, last_name, email, role)
                VALUES (%s, %s, %s, %s)
                           """, (
                               user["first_name"],
                               user["last_name"],
                               user["email"],
                               user["role"]
                           ))
        connection.commit()
        return "✅ Dummy users inserted (duplicates ignored)."
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        cursor.close()
        connection.close()


@app.route("/create-users-table")
def create_users_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")  # <-- Drop gammel tabel
        cursor.execute("""
                       CREATE TABLE users (
                                              id INT AUTO_INCREMENT PRIMARY KEY,
                                              first_name VARCHAR(50),
                                              last_name VARCHAR(50),
                                              email VARCHAR(100) NOT NULL UNIQUE,
                                              role VARCHAR(50),
                                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );
                       """)
        connection.commit()
        return "✅ 'users' table recreated with new columns."
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        cursor.close()
        connection.close()



if __name__ == "__main__":
    app.run(debug=True)