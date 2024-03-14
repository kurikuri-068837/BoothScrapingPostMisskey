from misskey import Misskey as mk
from apikey import *
import time


class PostNote():
    def __init__(self):
        
        self.misskey_api = mk(misskey_instance)
        self.misskey_api.token = misskey_api_token
        self.max_attempts = 10 #最大失敗回数
        
    def post(self,post_schedule):
        
        for data in post_schedule.values():
            attempts = 0 # 試行回数カウンタ
            while attempts < self.max_attempts:
                try:
                    print(f"{data[1]} - {data[0]}\n{data[2]}")
                    #self.misskey_api.notes_create(text=f"{data[1]} - {data[0]}\n{data[2]}")
                    raise Exception
                    #TODO 改修中につき事故防止のコメントアウト 本番環境テストの際は使用
                    break
                except Exception as e:
                    print(f"こちらのエラーが発生しました：{e}")
                    print(f"5分後再度実行を行います")
                    print(f"残り再実行可能回数： {self.max_attempts-attempts-1} 回")
                    attempts += 1
                    time.sleep(3)
            if attempts == self.max_attempts:
                raise RuntimeError("エラーが何度も発生しているため実行を停止しました")
            
            time.sleep(15)
        
if __name__ == "__main__":
    pn = PostNote()
    s_name = "test_shop"
    p_name = "testtest"
    url = "https://misskey.io/@vrcboothinfobot"
    
    pn.post({"aa":[s_name,p_name,url]})
