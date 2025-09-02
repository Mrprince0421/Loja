from jwt import decode

from security import create_access_token
from settings import Settings


def test_jwt():
    settings = Settings()
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded