# Flask + SQLAlchemy + Alembic Boilerplate

This is a sample project of Async Web API with Flask + SQLAlchemy 2.0 + Alembic.
It includes asynchronous DB access using asyncpg and test code.

See [reference](https://github.com/rhoboro/async-fastapi-sqlalchemy/tree/main).

Other References
- [Flask Docs](https://flask.palletsprojects.com/en/3.0.x/)
- [Gunicorn](https://gunicorn.org/)
- [SQL Alchemy](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQL Alchemy - PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

# Setup

## Install

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=root \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgdata:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:15.2-alpine

# Cleanup database
# $ docker stop db
# $ docker rm db
# $ docker volume rm pgdata

(venv) $ APP_CONFIG_FILE=local python3 app/main.py migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

# Run

```shell
(venv) $ APP_CONFIG_FILE=local python3 app/main.py api
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000 (92311)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 92315
```

# Test

```shell
(venv) $ python3 -m pytest
```

# Create Migration

```shell
(venv) $ cd app/migrations
(venv) alembic revision -m "<name_of_migration_file>"
```

# Note API Endpoints

The note API was created to enable `users` to interact (CRUD) with the `notes` table. Each and every single endpoint for Note CRUD requires user authorization token, obtained by logging in and send the token within the request as a bearer token. The authorization is required to make sure only users can access the resources.

- The API will be ran locally on port `:8000`

- The main url prefix of the url will be `/api/v1/notes`

- Therefore generally to hit the API, the url will be: `http://localhost:8000/api/v1/notes`

The complete documentation of Note CRUD request and its example responses can be accessed via:
**[Postman Documentation](https://documenter.getpostman.com/view/31678216/2s9YsT6U5N)**

## Endpoints
### `/api/v1/notes`
Methods:
- POST  : Hitting the endpoint with method **POST** is used to **CREATE A NEW NOTE**. The request should also includes a **[ Request Body]()** containing title and content.

- GET : Hitting the endpoint with method **GET** is used to retrieve the list of notes in the database. This method implements parameter value for pagination and the notes. The parameters are:
  - page (int) : to retrieve data on a certain page from the pagination (default 1)
  - item_per_page (int) : to limit how many notes will be shown per page (default 10)
  - include_deleted (bool) : to specify whether deleted notes shall be included or not (default False)
  - filter_user (bool) : to specify whether the notes in response should include all users' note or only the ones associated to the user (default True)

### `/api/v1/notes/<note_id>`
The endpoint of `<note_id>` can only be accessed by users associated (created) to the note. If not, the return will be an error

Methods:
- GET : Hitting the endpoint with the specified `<note_id>` and method **GET** will retrieve a note corresponding to the `<note_id>`
- PUT: Hitting the endpoint with the specified `<note_id>` and method **PUT** will update a note corresponding to the `<note_id>`. The request should also includes a **[ Request Body]()** containing title and content.
- DELETE: Hitting the endpoint with the specified `<note_id>` and method **DELETE** will delete (soft-delete) a note corresponding to the `<note_id>`

### Request Body
There are 2 endpoints that needed a body:
- `/api/v1/notes/` Method **POST**
- `/api/v1/notes/<note_id>` Method **PUT**

The body structure of the request in JSON will look like this:

```json
{
    "title": "My First Note",
    "content": "Hello, World!"
}
```
The requirements for the values are:
- title: minimum length is 1, maximum is 255
- content: minimum length is 6, maximum is 500