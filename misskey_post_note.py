from misskey import Misskey as mk
from apikey import *
import time

class PostNote():
    def __init__(self):
        self.misskey_api = mk(misskey_instance)
        self.misskey_api.token = misskey_api_token
        
    def post(self,shop_name,product_name,url):
        self.misskey_api.notes_create(text=f"【{shop_name}】 {product_name}\n{url}")
        
if __name__ == "__main__":
    pn = PostNote()
    s_name = "test_shop"
    p_name = "testtest"
    url = "https://misskey.io/@vrcboothinfobot"
    
    pn.post(s_name,p_name,url)