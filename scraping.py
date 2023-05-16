import requests as rq
from bs4 import BeautifulSoup as bs
from misskey_post_note import PostNote as pn
import re
import time


class Scraping():
    def __init__(self,id_list_before):
        self.id_list_before = id_list_before
        self.id_list_after = []
        self.page_no = 1
        self.url = f"https://booth.pm/ja/search/VRChat?page={self.page_no}&sort=new"
        
        
    def add_item(self,item):
        self.id_list_before.append(item)  # 要素をリストに追加
        if len(self.id_list_before) > 150:
            self.id_list_before.pop()

    
    def get_info(self):
        time.sleep(1)
        r = rq.get(self.url)
        print(r.status_code)
        soup = bs(r.content, "html.parser")
        li = soup.select(".item-card__title")
        








