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
                           INSERT IGNORE INTO users (username, email)
                VALUES (%s, %s)
                           """, (user["username"], user["email"]))
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
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users (
                                                            id INT AUTO_INCREMENT PRIMARY KEY,
                                                            username VARCHAR(50) NOT NULL UNIQUE,
                           email VARCHAR(100),
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );
                       """)
        connection.commit()
        return "✅ 'users' table created (or already exists)."
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        cursor.close()
        connection.close()



if __name__ == "__main__":
    app.run(debug=True)