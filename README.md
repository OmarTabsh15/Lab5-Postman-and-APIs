# Lab 5 - Postman and APIs

**Omar Tabsh - 202400798**
Software Tools Lab - Fall 2026-2027

A Flask app that adds, reads, updates and deletes users in an SQLite database through a REST API, tested with a Postman collection.

## Endpoints

| # | Endpoint | Method | Description |
|---|----------|--------|-------------|
| 1 | `/api/users` | GET | Get the list of all users in the database |
| 2 | `/api/users/<user_id>` | GET | Get a single user record that matches the id |
| 3 | `/api/users/add` | POST | Create a new user record |
| 4 | `/api/users/update` | PUT | Update a user record |
| 5 | `/api/users/delete/<user_id>` | DELETE | Delete a user record |

## Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The first run creates `database.db` with the `users` table. The API runs on http://localhost:5000.

`sqlite3` ships with Python, so it needs no separate install.

## Postman

The `postman` folder holds:

- `Flask user app.postman_collection.json`: the **Flask user app** collection. It has one request per endpoint, a saved example for each request, and test scripts.
- `Flask user app - Local.postman_environment.json`: the environment that stores the URL in the `baseUrl` variable (`http://localhost:5000`).

To use them:

1. In Postman, choose **Import** and import both files.
2. Select the **Flask user app - Local** environment.
3. Run the requests in order, or use the Collection Runner.

*Add a new user* saves the new `user_id` in the `userId` collection variable. *Get user by ID*, *Update user* and *Delete user* use that variable.

## Example request body

```json
{
    "name": "John Doe",
    "email": "jondoe@gamil.com",
    "phone": "067765434567",
    "address": "John Doe Street, Innsbruck",
    "country": "Austria"
}
```

For `PUT /api/users/update`, also include `"user_id"`.
