#services/user_service.py

from db import get_db_connection
import MySQLdb

def get_all_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
                       SELECT id, first_name, last_name, email, role, created_at FROM users
                       """)
        return cursor.fetchall()
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
                       INSERT INTO users (first_name, last_name, email, role)
                       VALUES (%s, %s, %s, %s)
                       """, (
                           data["first_name"],
                           data["last_name"],
                           data["email"],
                           data["role"]
                       ))
        connection.commit()
        data["id"] = cursor.lastrowid
        return data
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()