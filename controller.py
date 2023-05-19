from scraping import Scraping
from misskey_post_note import PostNote
import threading
from gui import AppGUI
import time

class AppController():
    
    def __init__(self) -> None:
        self.mainloop = threading.Thread(target=lambda : AppGUI(self),)
        self.mainloop.start()
        #print(self.gui)
        
    def start_processing(self):
        #TODO:ここにスクレイピング等の処理
        #while True:
            #time.sleep(2)
            #self.gui.log_entry("test")
        pass
    
    def stop_processing(self):
        #TODO:スクレイピング、misskeyのポスト終了処理、処理済みリストの保存処理
        pass        
    
    def pause_processing(self):
        #TODO:スクレイピング、misskeyのポストの中断処理
        pass
    
    def resume_processing(self):
        pass
        
    
    


