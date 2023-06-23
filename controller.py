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
        #TODO:ここにスクレイピング等の処理
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
                print("enter")
                scheduled_posts = self.sp.process()
                
                if scheduled_posts != {}:
                    print("post process")
                    postnote_thread = threading.Thread(target=pn.post,args=(scheduled_posts,))
                    postnote_thread.start()
                    print("post end")
            
            
            self.StoppableFrag = True
            
            for i in range(self.cycle_time):
                if self.judge_weekday_daytime(): # 日中の昼間だった場合は実行スパンを30分おきにする
                    time.sleep(1*3)
                else:
                    time.sleep(1)
                if not self.ProcessingFrag:
                    postnote_thread.join()
                    print("a")
            postnote_thread.join()
        
        
    def judge_weekday_daytime(self):
        current_time = time.localtime()
        day_of_week = current_time.tm_wday  # 0: 月曜日, 1: 火曜日, ... , 6: 日曜日
        hour = current_time.tm_hour
        minute = current_time.tm_min
        
        if 0 <= day_of_week <= 4:
            # 月曜日から金曜日までの場合
            if (9 <= hour < 11) or (13 <= hour < 17) or (hour == 11 and minute <= 20 ):
                # 9時から12時、13時から17時までの間は日中のスパンを延長する
                return True
        return False
        
    # GCP移行に伴い使用中止
    def CUI_Controller(self):
        while True:
            command = input("process - start/stop: ")
            if command == "stop":
                self.ProcessingFrag = False
                self.stop_processing()
                break
            # 特定のコマンドに対する処理を記述する
            if command == "start":
                # 別のプロセスを実行
                self.start_processing()
            else:
                print("無効なコマンドです。")
                
        input("プログラムを終了します。(please Enter)")


    def check_process_time(self):
        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min
        
        if 23 <= hour or 0 <= hour < 6 or (hour == 6 and minute <= 30 ) or (hour==22 and minute >=30):
            
            print("夜間のため、プロセスを実行しません(停止時間:22時半~6時半まで)")
            self.save_data()
            sys.exit()
        return True

    
    
    
