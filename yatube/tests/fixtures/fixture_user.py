import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='Test user', password='1234567')


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client
