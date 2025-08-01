#services/user_service.py

from db import get_db_connection
import MySQLdb

def get_all_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username, email, created_at FROM users")
        users = cursor.fetchall()
        return users
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

def add_user(data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
                       INSERT INTO users (username, email)
                       VALUES (%s, %s)
                       """, (data["username"], data["email"]))
        connection.commit()
        data["id"] = cursor.lastrowid
        return data
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()