from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sql.setting.setting import Engine,Base

class PoplarModelsShop(Base):
    __tablename__="poplar_models_shop"
    __table_args__={
        "comment":"white_listに入っているショップがアバターを出品した際の検知に使用"
    }
    
    shop_name=Column("shop_name",String(100),primary_key=True)

Base.metadata.create_all(bind=Engine)