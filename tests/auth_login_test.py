import pytest
from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1


def test_valid_login():
    clear_v1()

    u_id = auth_register_v1(
        "JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    u_id2 = auth_register_v1("testA@gmail.com", "testA2021", "John", "smith")
    u_id3 = auth_register_v1("StandUser@gmail.com",
                             "StandPower", "Generic", "name")
    u_id4 = auth_register_v1("11037.666@gmail.com",
                             "armStrongCann0n", "Isaac", "Schneider")
    # changed the comparision as we cannot assume that u_id is generated
    # in a numerical increasing order starting from 1.
    assert auth_login_v1("StandUser@gmail.com", "StandPower") == u_id3
    assert auth_login_v1("JoJo@gmail.com", "HermitPurple") == u_id
    assert auth_login_v1("testA@gmail.com", "testA2021") == u_id2
    assert auth_login_v1("11037.666@gmail.com", "armStrongCann0n") == u_id4


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
