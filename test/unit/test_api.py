import pytestw
from app.models import Users

@pytest.fixture(scope='module')
def user():
    user = Users(username='rizzo')
    return user

def test_new_user(user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    password = 'cubs2020'
    user.hash_password(password)
    user.expiration = 60
    user.ssh_key = '/path/to/key'
    user.email_addr = 'rizzo@cubs.com'
    user.is_admin = bool(True)

    assert user.username == 'rizzo'
    assert user.expiration == 60
    assert user.ssh_key == '/path/to/key'
    assert user.email_addr == 'rizzo@cubs.com'
    assert user.is_admin == True
