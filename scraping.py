import requests as rq
from bs4 import BeautifulSoup as bs
import time


class Scraping():
    def __init__(self,processed_id_list:list):
        self.processed_id_list = processed_id_list
        self.item_dict_mem = {}
        self.NotReadNextPageFrag = False
        self.scheduled_posts = {}
        self.page_no = 1
        
        
    def add_processed_item_list(self,item):
        self.processed_id_list.insert(0,item)  # 要素をリストに追加
        if len(self.processed_id_list) > 270:
            self.processed_id_list.pop()
    
    
    def get_info(self):
        time.sleep(3)
        r = rq.get(f"https://booth.pm/ja/search/VRChat?page={self.page_no}&sort=new")
        print(f"https://booth.pm/ja/search/VRChat?page={self.page_no}&sort=new")
        self.now_url_and_status_code = f"status:{r.status_code}  https://booth.pm/ja/search/VRChat?page={self.page_no}&sort=new"
        soup = bs(r.content, "html.parser")
        item_id = soup.select('.item-card__wrap')
        shop_name = soup.select(".item-card__shop-name")
        item_name = soup.select(".item-card__title")
        item_url = soup.select('div.item-card__summary > div.item-card__title > a')
        return item_id,shop_name,item_name,item_url
        
    def process(self):
        
        while not self.NotReadNextPageFrag:
            
            item_id,shop_name,item_name,item_url = self.get_info()
            print(shop_name[0].get_text(),item_name[0].find('a').text,item_url[0].get('href'))
            for i in range(60):
                if not item_id[i].get('id') in self.processed_id_list: # 過去に投稿したものと重複するかの確認
                    item_dict = {item_id[i].get('id'):[shop_name[i].get_text(),item_name[i].find('a').text,item_url[i].get('href')]}
                    self.scheduled_posts = self.scheduled_posts | item_dict # 辞書の結合
                    self.add_processed_item_list(item=item_id[i].get('id'))
                    
                else:
                    self.NotReadNextPageFrag = True
                    break
            if self.page_no == 4 : break # 3ページ目よりも後ろは見ないようにする（負荷軽減と万が一の時の保険）
            print("TEST")
            time.sleep(3)
            
            self.page_no+=1
        return self.scheduled_posts
            
            
    def watch_now_processing_url(self):
        return self.now_url_and_status_code
    
    def get_processed_id_list(self):
        return self.processed_id_list
        
        
if __name__ == "__main__":
    sp = Scraping(processed_id_list=[])
    sp.process()







