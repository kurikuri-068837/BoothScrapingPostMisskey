import requests as rq
from bs4 import BeautifulSoup as bs
import time


class Scraping():
    def __init__(self,id_list_before:list):
        self.id_list_before = id_list_before
        self.id_list_after = []
        self.item_dict_mem = {}
        self.NotReadNextPageFrag = False
        self.scheduled_posts = {}
        
        
    def add_processed_item_list(self,item):
        self.id_list_before.insert(0,item)  # 要素をリストに追加
        if len(self.id_list_before) > 270:
            self.id_list_before.pop()
    
    
    def get_info(self,page_no):
        time.sleep(3)
        self.page_no = str(page_no)
        r = rq.get(f"https://booth.pm/ja/search/VRChat?page={self.page_no}&sort=new")
        self.now_url_and_status_code = f"status:{r.status_code}  https://booth.pm/ja/search/VRChat?page={self.page_no}&sort=new"
        soup = bs(r.content, "html.parser")
        item_id = soup.select('.item-card__wrap')
        shop_name = soup.select(".item-card__shop-name")
        item_name = soup.select(".item-card__title")
        item_url = soup.select('div.item-card__summary > div.item-card__title > a')
        
        return item_id,shop_name,item_name,item_url
        
    def process(self):
        page_count = 1
        
        while not self.NotReadNextPageFrag:
            
            item_id,shop_name,item_name,item_url = self.get_info(page_no=page_count)
            for i in range(60):
                if not item_id[i].get('id') in self.id_list_before: # 過去に投稿したものと重複するかの確認
                    item_dict = {item_id[i]:[shop_name[i],item_name[i],item_url[i]]}
                    self.scheduled_posts = self.scheduled_posts | item_dict # 辞書の結合
                    self.add_processed_item_list(item=item_id[i])
                    
                else:
                    self.NotReadNextPageFrag = True
                    break
            if page_count == 4 : break # 3ページ目よりも後ろは見ないようにする（負荷軽減と万が一の時の保険）
            time.sleep(1)
            page_count+=1
            
            
    def watch_now_processing_url(self):
        return self.now_url_and_status_code
    
    def get_processed_item_list(self):
        return self.id_list_before
        
        
if __name__ == "__main__":
    sp = Scraping(id_list_before=[])
    sp.process()







