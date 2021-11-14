import pytest
from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

def test_invalid_email():

    clear_v1()
    # different upper/lower case
    auth_register_v1("JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    with pytest.raises(InputError):
        auth_login_v1("jojo@gmail.com", "HermitPurple")
    with pytest.raises(InputError):
        auth_login_v1("jojo@gmail.com", "KermittheHermit")
    with pytest.raises(InputError):
        auth_login_v1("jojossds@gmail.com", "HermitPurple")


# assumes email is correct for invalid password
def test_invalid_password():
    clear_v1()
    auth_register_v1("JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    with pytest.raises(InputError):
        auth_login_v1("JoJo@gmail.com", "Hermitpuurple")
