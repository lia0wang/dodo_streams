import pytest

from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

def test_email_invalid():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail&.com", "armStrongCann0n", "Isaac", "Schneider")
    with pytest.raises(InputError):
        auth_register_v1("@xample.com", "armStrongCann0n", "Isaac", "Schneider")  
    with pytest.raises(InputError):
        auth_register_v1("email.example.com", "armStrongCann0n", "Isaac", "Schneider")     
    

def test_email_duplicate():
    clear_v1()
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    with pytest.raises(InputError):
            auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")

def test_password_short():
    clear_v1()
    with pytest.raises(InputError):
            auth_register_v1("11037.666@gmail.com", "arm11", "Issac", "Schneider")

def test_name_first_long():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "MynameisYoshikageKira.Im33yearsold.MyhouseisinthenortheastsectionofMorioh", "Schneider")

def test_name_last_long():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "MynameisYoshikageKira.Im33yearsold.MyhouseisinthenortheastsectionofMorioh")

def test_name_first_short():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "", "Schneider")

def test_name_last_short():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "")

def test_store_valid_users():
    clear_v1()
    assert auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")['auth_user_id'] == 1
    assert auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "Isaac", "Schneider")['auth_user_id'] == 2



