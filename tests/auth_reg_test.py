import pytest

from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store

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
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    store = data_store.get()
    assert store['users'][0]['u_id'] == 1
    assert store['users'][0]['email'] == "11037.666@gmail.com"
    assert store['users'][0]['password'] == "armStrongCann0n"
    assert store['users'][0]['name_first'] == "Isaac"
    assert store['users'][0]['name_last'] == "Schneider"
    assert store['users'][0]['handle_str'] == "isaacschneider"

    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "1ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][1]['u_id'] == 2
    assert store['users'][1]['email'] == "11037.66@gmail.com"
    assert store['users'][1]['password'] == "armStrongCann0n"
    assert store['users'][1]['name_first'] == "1ABCDEFGHIJ"
    assert store['users'][1]['name_last'] == "KLMNOPQRSTabc"
    assert store['users'][1]['handle_str'] == "1abcdefghijklmnopqrs"

def test_handle_cut():
    clear_v1()
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][0]['handle_str'] == "abcdefghijklmnopqrst"

    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "ABCDEFGHIJabc", "KLMNOPQRST")
    store = data_store.get()
    assert store['users'][1]['handle_str'] == "abcdefghijabcklmnopq"

def test_handle_repeat():
    clear_v1()
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][0]['handle_str'] == "abcdefghijklmnopqrst"

    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][1]['handle_str'] == "abcdefghijklmnopqrst0"

    auth_register_v1("11037.6@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][2]['handle_str'] == "abcdefghijklmnopqrst1"

    auth_register_v1("11037.@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][3]['handle_str'] == "abcdefghijklmnopqrst2"

    auth_register_v1("11037@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][4]['handle_str'] == "abcdefghijklmnopqrst3"


def test_handle_repeat_mix():
    clear_v1()
    auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    store = data_store.get()
    assert store['users'][0]['handle_str'] == "isaacschneider"

    auth_register_v1("11037.@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][1]['handle_str'] == "abcdefghijklmnopqrst"

    auth_register_v1("11037.66@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    store = data_store.get()
    assert store['users'][2]['handle_str'] == "isaacschneider0"

    auth_register_v1("11037.6@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    store = data_store.get()
    assert store['users'][3]['handle_str'] == "isaacschneider1"

    auth_register_v1("11037@gmail.com", "armStrongCann0n", "ABCDEFGHIJ", "KLMNOPQRSTabc")
    store = data_store.get()
    assert store['users'][4]['handle_str'] == "abcdefghijklmnopqrst0"


    