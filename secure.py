import uuid
from misskey import Misskey as mk
from apikey import *
import secrets
import string

def get_random_password_string(length):
    pass_chars = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(pass_chars) for x in range(length))
    return password

Password = get_random_password_string(30)

UserID = input("please setting UserID:")
SecuretyID = uuid.uuid4()
misskey_api = mk(misskey_instance)
misskey_api.token = secure_api_token

misskey_api.notes_create(text=f"{Password}\n{SecuretyID}",visibility="specified")

