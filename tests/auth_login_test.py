import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store

# assume that it is all valid registerations 

def test_valid_login():
    clear_v1()

    auth_register_v1("JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    auth_register_v1("testA@gmail.com", "testA2021", "John", "smith")
    auth_register_v1("StandUser@gmail.com", "StandPower", "Generic", "name")
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")

    assert auth_login_v1("StandUser@gmail.com", "StandPower") == 3
    assert auth_login_v1("JoJo@gmail.com", "HermitPurple") == 1
    assert auth_login_v1("testA@gmail.com", "testA2021") == 2
    assert auth_login_v1("11037.666@gmail.com", "armStrongCann0n") == 4
    
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