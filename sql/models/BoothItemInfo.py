from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sql.setting.setting import Engine,Base

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

Base.metadata.create_all(bind=Engine)