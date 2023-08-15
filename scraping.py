import requests as rq
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import threading
from misskey_post_note import PostNote
import logging

class Scraping():
    def __init__(self,processed_id_list:list):
        self.logger = logging.getLogger("BSMPPLog.controller").getChild("model_scraping")
        self.processed_id_list = processed_id_list
        self.item_dict_mem = {}
        self.NotReadNextPageFrag = False
        self.page_no = 1
        self.updatecsv = threading.Thread(target=self.update_save_data)
        
        
        
    def add_processed_item_list(self,target_list,item):
        target_list.insert(0,item)  # 要素をリストに追加
        
        if len(target_list) > 900:
            target_list.pop()
        return target_list
    
    
    def get_info(self):
        time.sleep(3)
        cookie = {'adult': 't'} #年齢確認用のcookie確認
        r = rq.get(f"https://booth.pm/ja/items?adult=include&page={self.page_no}&sort=new&tags%5B%5D=VRChat", cookies=cookie)
        print(f"https://booth.pm/ja/items?adult=include&page={self.page_no}&sort=new&tags%5B%5D=VRChat")
        self.now_url_and_status_code = f"status:{r.status_code}  https://booth.pm/ja/items?adult=include&page={self.page_no}&sort=new&tags%5B%5D=VRChat"
        self.logger.debug(f"{self.now_url_and_status_code}")
        soup = bs(r.content, "html.parser")

        item_id = soup.select('.item-card__wrap')
        shop_name = soup.select(".item-card__shop-name")
        item_name = soup.select(".item-card__title")
        item_url = soup.select('div.item-card__summary > div.item-card__title > a')
        return item_id,shop_name,item_name,item_url
        
    def process(self):
        self.NotReadNextPageFrag = False
        self.page_no = 1
        self.scheduled_posts = {}
        while not self.NotReadNextPageFrag:
            
            item_id,shop_name,item_name,item_url = self.get_info()
            #print(item_id)
            for i in range(60):
                if not item_id[i].get('id') in self.processed_id_list: # 過去に投稿したものと重複するかの確認
                    print(item_id[i].get('id'))
                    item_dict = {item_id[i].get('id'):[shop_name[i].get_text(),item_name[i].find('a').text,item_url[i].get('href')]}
                    self.scheduled_posts = item_dict | self.scheduled_posts  # 辞書の結合
                    
                    self.processed_id_list = self.add_processed_item_list(target_list=self.processed_id_list,item=item_id[i].get('id'))
                    
                    
                elif item_id[i].get('id') in self.processed_id_list and self.page_no == 1 and i == 0:
                    self.logger.info('NothingPostTarget')
                    self.NotReadNextPageFrag = True
                    break
                else:
                    self.NotReadNextPageFrag = True
                    break
            if self.page_no == 10 : break # 10ページ目よりも後ろは見ないようにする（負荷軽減と万が一の時の保険）
            
            time.sleep(5) #負荷軽減のためアクセスサイクルを5秒に変更
            self.page_no+=1
        self.update_save_data()
        time.sleep(10)
        
        print("save ok")
        return self.scheduled_posts
            
            
    def watch_now_processing_url(self):
        return self.now_url_and_status_code
    
    def get_processed_id_list(self):
        return self.processed_id_list
    
    def update_save_data(self):
        processed_id_list_df = pd.DataFrame(self.processed_id_list)
        processed_id_list_df.to_csv("processed_id_list.csv",index=False)
        
        
        
        
        
if __name__ == "__main__":
    df = pd.read_csv("processed_id_list.csv")
    processed_id_list = list(df.values[:,0])
    
    def check_process_time():
        current_time = time.gmtime()
        hour = (current_time.tm_hour + 9) % 24 #GMTから日本時刻への変換（これでサーバー時刻による処理時間のずれを修正）
        minute = current_time.tm_min

        if 23 <= hour or 0 <= hour < 6 or (hour == 6 and minute <= 30 ):
            
            print("夜間のため、プロセスを実行しません(停止時間:23時~6時半まで)")
            if hour == 23:
                wait_sec = 7*3600
                time.sleep(wait_sec)
            return False
        return True
    
    sp = Scraping(processed_id_list)
    pn = PostNote()
    while True:
        if check_process_time():
            print("enter")
            scheduled_posts = sp.process()
            
            if scheduled_posts != {}:
                print("post process")
                postnote_thread = threading.Thread(target=pn.post,args=(scheduled_posts,))
                postnote_thread.start()
                print("post end")
        time.sleep(600)







