# casting-agency

This is casting agency's API server.
Temporaily, this is deployed 'http://casting-agency-jnsp.herokuapp.com/'

## Endpoints

GET `/login`

Redirect to login page of Auth0.com.

GET `/movies`

Get movies. Required permission `view:movies`.

POST `/movies`

Add new movie. Required permission `add:movies`. New movie data should be json body.

PATCH `/movies/<id>`

Modify movie of `<id>`. Required permission `modify:movies`. Modified movie data should be json body.

DELETE `/movies/<id>`

Remove movie of `<id>`. Required permission `delete:movies`.

GET `/actors`

Get actors. Required permission `view:actors`.

POST `/actors`

Add new actor. Required permission `add:actors`. New actor data should be json body.

PATCH `/actors/<id>`

Modify actor of `<id>`. Required permission `modify:actors`. Modified actor data should be json body.

DELETE `/actors/<id>`

Remove actor of `<id>`. Required permission `delete:actors`.

### Role and Permissions

There are 3 Roles, and each roles has its own permissions.

* Casting Assistant: `view:movies`, `view:actors`
* Casting Director: Casting Assistant's + `add:actors`, `delete:actors`, `modify:actors`, `modify:movies`
* Executive Producer: Casting Director's + `add:movies`, `delete:movies`

## How to install

This project is based on `Python 3.9.1`. Just clone this to use it.

```bash
git clone https://github.com/jnsp/casting-agency.git
```

### Requirements

#### For development

Note: If you want to do pytest, install `requirements/dev.txt` requirements like below.

```bash
pip install -r requirements/dev.txt
```

#### For production

```bash
pip install -r requirements/prod.txt
```

#### For Heroku deployment

```bash
pip install -r requirements/heroku.txt
```

OR

```bash
pip install -r requirements.txt
```

### Environment variables

This project uses `.env` file for sensitive inforamation.
`.env` file has to be in the root directory of this project.
`.env` file includes variables like below

```
AUTH0_DOMAIN=[auth0 domain]
API_AUDIENCE=[auth0 api audience]
ALGORITHM=[auth algorithm]
APP_URL=[app url after deployment]
CLIENT_ID=[auth0 client id]
TEST_CLIENT_ID=[auth0 test client id]
TEST_CLIENT_SECRET=[auth0 test client secret]
CASTING_ASSISTANT_TOKEN=[casting assitant's jwt for test]
CASTING_DIRECTOR_TOKEN=[casting director's jwt for test]
EXECUTIVE_PRODUCER_TOKEN=[executive producer's jwt for test]
```

## How to run server

In development mode, you can run server with localhost.

```bash
export FLASK_APP=ca.py
export FLASK_ENV=development
flask run
```


## How to deploy to Heroku

### Add DB server to Heroku

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This command adds database in Heroku and env variable `DATABASE_URL`. You can check the `DATABASE_URL` with the commaind like below.

```bash
heroku config
```

### Set environment variable

Heroku needs env variable but `.env` can't be pushed. Set env variable with heroku cli.

```bash
heroku config:set AUTH_DOMANI=[auth0 domain]
```

You need to set 7 variables manually.

```
FLASK_APP=ca.py
FLASK_CONFIG=heroku
AUTH0_DOMAIN=[auth0 domain]
API_AUDIENCE=[auth0 api audience]
ALGORITHM=[auth algorithm]
APP_URL=[app url after deployment]
CLIENT_ID=[auth0 client id]
```

### Push repository to Heroku

After Heroku cli settings, just git push to the heroku repository.

```bash
git push heroku
```

### DB upgrade

```bash
heroku run flask db upgrade
```

## How to test

You can test this project with `pytest`.

```bash
pytest -v
```

There are five test files here.

* `test_api.py`: unit tests for api endpoints
* `test_auth.py`: unit tests for authentication and authorization with fake JWT
* `test_basic.py`: unit tests for app factory
* `test_heroku.py`: functional tests for real endpoints after Heroku deployment
* `test_models.py`: unit tests for data models

Note: `test_heroku` is only able to be tested after deployment and `.env` file has `CASTING_ASISTANT_TOKEN`, `CASTING_DIRECTOR_TOKEN`, and `EXECUTIVE_PRODUCER_TOKEN`.
