import requests as rq
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

class Scraping():
    def __init__(self,processed_id_list:list):
        self.booth_scraping_limit = 4 # スクレピングするページ数上限を指定（負荷軽減と万が一の時の保険）
        self.processed_id_list = processed_id_list
        self.item_dict_mem = {}
        self.NotReadNextPageFrag = False
        self.page_no = 1
        
        
    def get_info(self):
        cookie = {'adult': 't'} #年齢確認用のcookie確認
        r = rq.get(f"https://booth.pm/ja/items?adult=include&page={self.page_no}&sort=new&tags%5B%5D=VRChat", cookies=cookie)
        self.now_url_and_status_code = f"status:{r.status_code}  https://booth.pm/ja/items?adult=include&page={self.page_no}&sort=new&tags%5B%5D=VRChat"
        soup = bs(r.content, "html.parser")
        item_info = soup.select('div.u-mt-400> ul > li')
        shop_name = soup.select(".item-card__shop-name")
        item_name = soup.select(".item-card__title")
        item_url = soup.select('div.item-card__summary > div.item-card__title > a')
        return item_info,shop_name,item_name,item_url
        
    def process(self):
        self.NotReadNextPageFrag = False
        self.page_no = 1
        self.scheduled_posts = {}
        while not self.NotReadNextPageFrag:
            
            item_info,shop_name,item_name,item_url = self.get_info()
            #print(item_id)
            for i in range(60): # 1ページ当たり60商品のため
                if not item_info[i].get('data-product-id') in self.processed_id_list: # 過去に投稿したものと重複するかの確認
                    print(item_info[i].get('data-product-id'))
                    item_dict = {item_info[i].get('data-product-id'):[shop_name[i].get_text(),item_name[i].find('a').text,item_url[i].get('href')]}
                    self.scheduled_posts = item_dict | self.scheduled_posts  # 辞書の結合
                    
                    self.processed_id_list = self.add_processed_item_list(target_list=self.processed_id_list,item=item_info[i].get('data-product-id'))
                    
                    
                elif item_info[i].get('data-product-id') in self.processed_id_list and self.page_no == 1 and i == 0:
                    self.NotReadNextPageFrag = True
                    break
                else:
                    self.NotReadNextPageFrag = True
                    break
            if self.page_no == self.booth_scraping_limit : break  # スクレピングするページ数を制限（負荷軽減と万が一の時の保険）
            
            time.sleep(5) # アクセスサイクル:5秒
            self.page_no+=1
        return self.scheduled_posts

        
    def add_processed_item_list(self,target_list,item):
        target_list.insert(0,item)  # 要素をリストに追加
        if len(target_list) > 900:
            target_list.pop()
        return target_list

    def update_save_data(self):
        processed_id_list_df = pd.DataFrame(self.processed_id_list)
        processed_id_list_df.to_csv("processed_id_list.csv",index=False)
        print("save ok")



if __name__ == "__main__":
    sp = Scraping(list(pd.read_csv("processed_id_list.csv").values[:,0]))
    a,b,c,d = sp.get_info()
    print(a[0].get('data-product-id')) # アイテムid
    print(a[0].get('data-product-category')) # カテゴリid（3桁）






