import pytest

from src.auth import auth_register_vl
from src.error import InputError

def test_email_invalid():
    with pytest.raises(InputError):
        auth_register_vl("11037.666@gmail&.com", "armStrongCann0n", "Isaac", "Schneider")

def test_email_double():
    auth_register_vl("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    with pytest.raises(InputError):
            auth_register_vl("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")

def test_password_short():
    with pytest.raises(InputError):
            auth_register_vl("11037.666@gmail.com", "arm11", "Issac", "Schneider")

def test_name_first_long():
    with pytest.raises(InputError):
        auth_register_vl("11037.666@gmail.com", "arm11", "MynameisYoshikageKira.Im33yearsold.MyhouseisinthenortheastsectionofMorioh", "Schneider")

def test_name_last_long():
    with pytest.raises(InputError):
        auth_register_vl("11037.666@gmail.com", "arm11", "Isaac", "MynameisYoshikageKira.Im33yearsold.MyhouseisinthenortheastsectionofMorioh")

def test_valid_user():
   auth_register_vl("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")

    