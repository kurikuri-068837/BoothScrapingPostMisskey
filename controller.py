from scraping import Scraping
from misskey_post_note import PostNote
import threading
import time
import pandas as pd
import logging
#from secure import * #GCP以降に伴い使用中止
import sys

class AppController():
    
    def __init__(self) -> None:
        self.logger = logging.getLogger("BSMPPLog").getChild("controller")
        self.ProcessingFrag = False
        self.StoppableFrag = False
        self.cycle_time = 600
        
        
        
        
        
    def start_processing(self):
        self.load_data()
        self.ProcessingFrag = True
        self.StoppableFrag = False
        other_process_thread = threading.Thread(target=self.scraping_process)
        other_process_thread.start()
        
    
    def stop_processing(self):
        self.ProcessingFrag = False
        timer_start = time.time()
        print("prease wait...")
        while not self.StoppableFrag:
            time.sleep(2)
            print(time.time()-timer_start)
        #TODO:スクレイピング、misskeyのポスト終了処理、処理済みリストの保存処理
        self.save_data()
        print("save ok")       
    
    def pause_processing(self):
        self.ProcessingFrag = False
        
        #TODO:スクレイピング、misskeyのポストの中断処理
        pass
    
    def resume_processing(self,):
        self.ProcessingFrag = True
        self.StoppableFrag = False
        self.scraping_process()
        pass
    
    def normarmination_processing(self):
        
        
        print("Close GUI")
        
        pass
    
    def load_data(self):
        try:
            self.processed_id_list = list(pd.read_csv("processed_id_list.csv").values[:,0])
                
        except:
            self.processed_id_list = []
        logging.log
            
    def save_data(self):
        processed_id_list = self.sp.get_processed_id_list()
        processed_id_list_df = pd.DataFrame(processed_id_list)
        processed_id_list_df.to_csv("processed_id_list.csv",index=False)
        
    def scraping_process(self):
        self.sp = Scraping(self.processed_id_list)
        pn = PostNote()
        while self.ProcessingFrag:
            self.StoppableFrag = False
            if self.check_process_time():
                print("start scraping process")
                scheduled_posts = self.sp.process()
                
                if scheduled_posts != {}:
                    print("start post process")
                    postnote_thread = threading.Thread(target=pn.post,args=(scheduled_posts,))
                    postnote_thread.start()
            
            
            
            self.StoppableFrag = True
            for i in range(self.cycle_time):
                if self.judge_weekday_daytime(): # 日中の昼間だった場合は実行スパンを30分おきにする
                    time.sleep(1*3)
                else:
                    time.sleep(1)
                if not self.ProcessingFrag:
                    if scheduled_posts != {}:
                        postnote_thread.join()
                        print("Change ProcessingFrag")
            
            if scheduled_posts != {}:
                postnote_thread.join()
            print("end posted process")
        
    #曜日による処理の違いを実装するための処理
    def judge_weekday_daytime(self):
        self.get_hmm()
        if 0 <= self.day_of_week <= 4:
            # 月曜日から金曜日までの場合
            if (9 <= self.hour < 11) or (13 <= self.hour < 17) or (self.hour == 11 and self.minute <= 20):
                # 9時から12時、13時から17時までの間は日中のスパンを延長する
                return True
        return False
        

    #曜日による処理の違いを実装するための処理
    def check_process_time(self):
        self.get_hmm()
        if 23 <= self.hour or 0 <= self.hour < 6 or (self.hour == 6 and self.minute <= 30 ) or (self.hour==22 and self.minute >=30):
            print("夜間のため、プロセスを実行しません(停止時間:22時半~6時半まで)")
            self.save_data()
            #sys.exit()
            return False
        return True
    
    def get_hmm(self):
        current_time = time.gmtime()
        self.day_of_week = current_time.tm_wday  # 0: 月曜日, 1: 火曜日, ... , 6: 日曜日
        self.hour = (current_time.tm_hour + 9) % 24 #GMTから日本時刻への変換（これでサーバー時刻による処理時間のずれを修正）
        self.minute = current_time.tm_min