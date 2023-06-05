from misskey import Misskey as mk
from apikey import *


misskey_api = mk(misskey_instance)
misskey_api.token = secure_api_token
