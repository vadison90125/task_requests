import pytest


@pytest.fixture(scope='function')
def base_url():
    yield 'https://jsonplaceholder.typicode.com'
