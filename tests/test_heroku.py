from collections import namedtuple
import os

from dotenv import load_dotenv
import pytest
import requests

load_dotenv()
APP_URL = os.getenv('APP_URL')
Token = namedtuple('Token', ['name', 'body'])
CA_TOKEN = Token('Casting Assistant', os.getenv('CASTING_ASSISTANT_TOKEN'))
CD_TOKEN = Token('Casting Director', os.getenv('CASTING_DIRECTOR_TOKEN'))
EP_TOKEN = Token('Executive Producer', os.getenv('EXECUTIVE_PRODUCER_TOKEN'))


@pytest.fixture
def new_actor_info():
    return {'name': 'NEW_ACTOR', 'age': 20, 'gender': 'X'}


@pytest.fixture
def new_movie_info():
    return {'title': 'NEW_MOVIE', 'release_date': '2021-02-01'}


@pytest.mark.parametrize('token', (CA_TOKEN, CD_TOKEN, EP_TOKEN),
                         ids=lambda t: t.name)
@pytest.mark.parametrize('resource', ('movies', 'actors'))
def test_get(token, resource):
    res = requests.get(f'{APP_URL}/{resource}',
                       headers={'Authorization': f'bearer {token.body}'})
    assert res.status_code == 200


@pytest.mark.parametrize('token', (CD_TOKEN, EP_TOKEN), ids=lambda t: t.name)
def test_add_delete_actors(token, new_actor_info):
    res = requests.post(f'{APP_URL}/actors',
                        headers={'Authorization': f'bearer {token.body}'},
                        json=new_actor_info)
    assert res.status_code == 200

    actor_id = res.json()['actor']['id']
    res = requests.delete(f'{APP_URL}/actors/{actor_id}',
                          headers={'Authorization': f'bearer {token.body}'})
    assert res.status_code == 200


@pytest.mark.parametrize('token', (EP_TOKEN, ), ids=lambda t: t.name)
def test_add_delete_movies(token, new_movie_info):
    res = requests.post(f'{APP_URL}/movies',
                        headers={'Authorization': f'bearer {token.body}'},
                        json=new_movie_info)
    assert res.status_code == 200

    movie_id = res.json()['movie']['id']
    res = requests.delete(f'{APP_URL}/movies/{movie_id}',
                          headers={'Authorization': f'bearer {token.body}'})
    assert res.status_code == 200


@pytest.mark.parametrize('token', (CD_TOKEN, EP_TOKEN), ids=lambda t: t.name)
def test_modify_actor(token, new_actor_info):
    res_add_actor = requests.post(
        f'{APP_URL}/actors',
        headers={'Authorization': f'bearer {EP_TOKEN.body}'},
        json=new_actor_info)
    actor_id = res_add_actor.json()['actor']['id']

    res_modify_actor = requests.patch(
        f'{APP_URL}/actors/{actor_id}',
        headers={'Authorization': f'bearer {token.body}'},
        json={'name': 'MODIFIED_NAME'})

    assert res_modify_actor.status_code == 200
    assert res_modify_actor.json()['actor']['name'] == 'MODIFIED_NAME'

    requests.delete(f'{APP_URL}/actors/{actor_id}',
                    headers={'Authorization': f'bearer {EP_TOKEN.body}'})


@pytest.mark.parametrize('token', (CD_TOKEN, EP_TOKEN), ids=lambda t: t.name)
def test_modify_movie(token, new_movie_info):
    res_add_movie = requests.post(
        f'{APP_URL}/movies',
        headers={'Authorization': f'bearer {EP_TOKEN.body}'},
        json=new_movie_info)
    movie_id = res_add_movie.json()['movie']['id']

    res_modify_movie = requests.patch(
        f'{APP_URL}/movies/{movie_id}',
        headers={'Authorization': f'bearer {token.body}'},
        json={'title': 'MODIFIED_TITLE'})

    assert res_modify_movie.status_code == 200
    assert res_modify_movie.json()['movie']['title'] == 'MODIFIED_TITLE'

    requests.delete(f'{APP_URL}/movies/{movie_id}',
                    headers={'Authorization': f'bearer {EP_TOKEN.body}'})
