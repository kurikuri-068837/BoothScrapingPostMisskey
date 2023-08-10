from misskey import Misskey as mk
from apikey import *
import time
import logging

class PostNote():
    def __init__(self):
        self.logger = logging.getLogger("BSMPPLog.controller").getChild("model_postmisskey")
        self.misskey_api = mk(misskey_instance)
        self.misskey_api.token = misskey_api_token
        
    def post(self,post_schedule):
        self.logger.debug("CallPostProcess")
        for data in post_schedule.values():
            self.misskey_api.notes_create(text=f"{data[1]} - {data[0]}\n{data[2]}")
            self.logger.info(f"Note:{data[1]} - {data[0]}, {data[2]}")
            
            time.sleep(15)
        
if __name__ == "__main__":
    pn = PostNote()
    s_name = "test_shop"
    p_name = "testtest"
    url = "https://misskey.io/@vrcboothinfobot"
    
    pn.post(s_name,p_name,url)
