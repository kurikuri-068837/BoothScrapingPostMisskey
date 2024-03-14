from controller import AppController
import logging
import datetime


def setting_log():
    dt = datetime.datetime.now()
    logging.basicConfig(filename=f'log/logger_{dt.year}-{dt.month}-{dt.day}_{dt.hour}-{dt.minute}-{dt.second}.log', level=logging.DEBUG)
    
    # loggerオブジェクトの宣言
    logger = logging.getLogger("BSMPPLog")
    
    # loggerのログレベル設定(ハンドラに渡すエラーメッセージのレベル)
    logger.setLevel(logging.DEBUG)
    
    # handlerの生成
    stream_handler = logging.StreamHandler()
    
    

    # ログ出力フォーマット設定
    handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(handler_format)
    logger.addHandler(stream_handler)
    
    return logger



if __name__ == "__main__":    
    logger = setting_log()
    logger.debug("StartProcess")
    app = AppController()
    app.start_processing()


