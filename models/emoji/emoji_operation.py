from sqlalchemy.orm import Session
from models.emoji.emoji_model import Emoji

#查询字典
def get_emoji_list(db:Session)->list:
    elist = db.query(Emoji).all()
    return elist