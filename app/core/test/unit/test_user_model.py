import pytest
from core.models import User

@pytest.mark.django_db
def test_user_create():

    user = User.objects.create(
        name = 'Test User',
        email = 'test@test.com',
        password= 'test'
    )

    assert user.id == 1
    assert user.name == "Test User"
    assert user.email is not '?'