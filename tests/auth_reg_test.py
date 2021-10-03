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
    auth_register_v1("11037@gmail.com", "123456", "Issac", "Schneider")
    with pytest.raises(InputError):
            auth_register_v1("11037.6@gmail.com", "", "Issac", "Schneider")
    with pytest.raises(InputError):
            auth_register_v1("11037.66@gmail.com", "1", "Issac", "Schneider")
    with pytest.raises(InputError):
            auth_register_v1("11037.666@gmail.com", "12", "Issac", "Schneider")
    with pytest.raises(InputError):
            auth_register_v1("11037.6666@gmail.com", "12345", "Issac", "Schneider")

def test_name_first_long():
    clear_v1()

    # Name of maximum length with 50 characters
    max_len_name = "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenor"
    # Name of beyond maximum length of 51 characters 
    beyond_max_name = "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort"
    beyond_max_name_plus = max_len_name + beyond_max_name

    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", max_len_name, "Schneider")
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", beyond_max_name, "Schneider")
    with pytest.raises(InputError):
        auth_register_v1("11037.6666@gmail.com", "armStrongCann0n", beyond_max_name_plus, "Schneider")

def test_name_last_long():
    clear_v1()

    # Name of maximum length with 50 characters
    max_len_name = "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenor"
    # Name of beyond maximum length of 51 characters
    beyond_max_name = "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort"
    beyond_max_name_plus = max_len_name + beyond_max_name

    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "Isaac", max_len_name)
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", beyond_max_name)
    with pytest.raises(InputError):
        auth_register_v1("11037.6666@gmail.com", "armStrongCann0n", beyond_max_name_plus, "Schneider")

def test_name_first_short():
    clear_v1()
    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "I", "Schneider")
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "", "Schneider")

def test_name_last_short():
    clear_v1()
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "S")
    with pytest.raises(InputError):
        auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "")

def test_return_values():
    clear_v1()
    uid_1 = auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    uid_2 = auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    uid_3 = auth_register_v1("11037.6@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    uid_4 = auth_register_v1("11037.@gmail.com", "armStrongCann0n", "Isaac", "Schneider")

    assert uid_1['auth_user_id'] == 1
    assert uid_2['auth_user_id'] == 2
    assert uid_3['auth_user_id'] == 3
    assert uid_4['auth_user_id'] == 4


