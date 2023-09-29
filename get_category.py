# 後で削除すること
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import csv


class Scraping():
    def __init__(self):
        self.booth_scraping_limit = 500 # スクレピングするページ数上限を指定（負荷軽減と万が一の時の保険）
        self.item_dict_mem = {}
        self.NotReadNextPageFrag = False
        self.page_no = 1
        
        
    def get_info(self):
        cookie = {'adult': 't'} #年齢確認用のcookie確認
        r = rq.get(f"https://booth.pm/ja/items?adult=include&page={self.page_no}&sort=new&tags%5B%5D=VRChat", cookies=cookie)
        soup = bs(r.content, "html.parser")
        item_category_name = soup.select('.item-card__category > a')
        item_category_no   = soup.select('div.u-mt-400 > ul > li')
        return item_category_name,item_category_no
        

    def process(self):
        self.NotReadNextPageFrag = False
        self.page_no = 1
        self.scheduled_posts = {}
        
        # CSVファイルを書き込みモードで開く
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            while not self.NotReadNextPageFrag:
                category_name, category_no = self.get_info()
                
                for i in range(60):
                    # CSVファイルに行を書き込む
                    csv_writer.writerow([category_no[i].get("data-product-category"), category_name[i].get_text()])
                    
                if self.page_no == self.booth_scraping_limit:
                    break  # スクレピングするページ数を制限（負荷軽減と万が一の時の保険）
                
                time.sleep(5) # アクセスサイクル:5秒
                self.page_no += 1


        
    def add_processed_item_list(self,target_list,item):
        target_list.insert(0,item)  # 要素をリストに追加
        if len(target_list) > 900:
            target_list.pop()
        return target_list

    def update_save_data(self):
        self.processed_id_list = []
        processed_id_list_df = pd.DataFrame(self.processed_id_list)
        processed_id_list_df.to_csv("processed_id_list.csv",index=False)
        print("save ok")
            
    def remove_duplicates_and_sort(self):
        # 既存のCSVファイルを読み込み、category_noの重複を削除してoutput2.csvに数値順に並び替えて出力する
        
        # 既存のCSVファイルを読み込む
        with open('output.csv', 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            # 重複を除去するためのセットを作成し、すべての行をリストに保存
            unique_category_no_set = set()
            rows_to_write = []
            
            for row in csv_reader:
                category_no = row[0]  # category_noは行の最初の要素
                if category_no not in unique_category_no_set:
                    # まだセットに含まれていない場合、セットに追加し、行を保存
                    unique_category_no_set.add(category_no)
                    rows_to_write.append(row)
        
        # 数値順にソート
        rows_to_write.sort(key=lambda x: int(x[0]))  # category_noを整数として比較
        
        # 新しいCSVファイルに書き込む
        with open('output2.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in rows_to_write:
                csv_writer.writerow(row)

# 関数を呼び出して実行

        

if __name__ == "__main__":
    sp = Scraping()
    #sp.process()
    sp.remove_duplicates_and_sort()
    
    