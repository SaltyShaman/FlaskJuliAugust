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


def get_user_by_id(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
                       SELECT id, first_name, last_name, email, role, created_at
                       FROM users WHERE id = %s
                       """, (user_id,))
        return cursor.fetchone()
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()


def update_user(user_id, data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
                       UPDATE users
                       SET first_name = %s, last_name = %s, email = %s, role = %s
                       WHERE id = %s
                       """, (
                           data["first_name"],
                           data["last_name"],
                           data["email"],
                           data["role"],
                           user_id
                       ))
        connection.commit()
        return get_user_by_id(user_id)
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

def delete_user(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
        return {"message": f"User with id {user_id} deleted."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

