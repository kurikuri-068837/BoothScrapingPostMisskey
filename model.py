from sqlalchemy import Column, Integer, String, DateTime,Boolean
from setting import Engine
from setting import Base

#各モデル

class BoothItemInfo(Base):
    __tablename__="booth_item_info"
    __table_args__={
        "comment":"Boothからスクレイピングしたデータを蓄積"
    }
    
    item_id=Column("item_id",Integer,primary_key=True)
    ite_name=Column("item_name",String(150),nullable=False)
    shop_name=Column("shop_name",String(100),nullable=False)
    category_no=Column("category_no",Integer,nullable=True)
    current_at=Column("current_at",DateTime,nullable=False)

class MisskeyPost(Base):
    __tablename__="misskey_post"
    __table_args__={
        "comment":"item_idをキーとしてmisskeyへ投稿した情報を記録"
    }
    
    item_id=Column("item_id",Integer,primary_key=True)
    note_id=Column("note_id",Integer,primary_key=True)
    poted_id=Column("poted_id",DateTime,nullable=False)
    delete_flag=Column("delete_flag",Boolean,nullable=False)

class Category(Base):
    __tablename__="category"
    __table_args__={
        "comment":""
    }
    
    category_no=Column("category_no",Integer,nullable=False)
    category_name=Column("category_name",String(13),nullable=False)

class PoplarModelsShop(Base):
    __tablename__="poplar_models_shop"
    __table_args__={
        "comment":"white_listに入っているショップがアバターを出品した際の検知に使用"
    }
    
    shop_name=Column("shop_name",String(100),primary_key=True)

Base.metadata.create_all(bind=Engine)