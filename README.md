# casting-agency

This is casting agency's API server.

## How to install

### Requirements

This is based on `Python 3.9.1`. 

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
