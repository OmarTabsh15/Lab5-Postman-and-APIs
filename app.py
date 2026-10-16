#!/usr/bin/python
# Lab 5 - Postman and APIs
# Omar Tabsh - 202400798
# User management app: SQLite database functions (CRUD) exposed as a REST API

import sqlite3
from flask import Flask, request, jsonify  # added to top of file
from flask_cors import CORS  # added to top of file


def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn


def create_db_table():
    conn = None
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("User table created successfully")
    except:
        print("User table creation failed - Maybe table already exists")
    finally:
        if conn:
            conn.close()


def insert_user(user):
    inserted_user = {}
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (user['name'], user['email'], user['phone'],
                     user['address'], user['country']))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except:
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

    return inserted_user


def get_users():
    users = []
    conn = None
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)

    except:
        users = []
    finally:
        if conn:
            conn.close()

    return users


def get_user_by_id(user_id):
    user = {}
    conn = None
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]
    except:
        user = {}
    finally:
        if conn:
            conn.close()

    return user


def update_user(user):
    updated_user = {}
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, "
                    "address = ?, country = ? WHERE user_id = ?",
                    (user["name"], user["email"], user["phone"],
                     user["address"], user["country"], user["user_id"],))
        conn.commit()
        # return the user
        updated_user = get_user_by_id(user["user_id"])

    except:
        if conn:
            conn.rollback()
        updated_user = {}
    finally:
        if conn:
            conn.close()

    return updated_user


def delete_user(user_id):
    message = {}
    conn = None
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        if conn:
            conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        if conn:
            conn.close()

    return message


# ---------------- REST API endpoints ----------------

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())


@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))


@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))


@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))


@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))


if __name__ == "__main__":
    create_db_table()  # creates database.db and the users table if missing
    # app.debug = True
    # app.run(debug=True)
    app.run()  # run app
