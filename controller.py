from scraping import Scraping
from misskey_post_note import PostNote
import threading
from gui import AppGUI

class AppController():
    
    def __init__(self) -> None:
        self.gui = AppGUI(self)
        
    def start_processing(self):
        #TODO:ここにスクレイピング等の処理
        pass
    
    def stop_processing(self):
        #TODO:スクレイピング、misskeyのポスト終了処理、処理済みリストの保存処理
        pass        
    
    def pause_processing(self):
        #TODO:スクレイピング、misskeyのポストの中断処理
        pass
    
    def resume_processing(self):
        pass
        
    
    


