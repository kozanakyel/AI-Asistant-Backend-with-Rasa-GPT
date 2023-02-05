from typing import Dict, List, Union
from database import db
import datetime

ChatJSON = Dict[str, Union[int, str, datetime.datetime]]

class ChatModel(db.Model):    # tells SQLAlchemy that it is something that will be saved to database and will be retrieved from database

  __tablename__ = "chats"

  # Columns
  id = db.Column(db.Integer, primary_key=True)
  #username = db.Column(db.String(80), unique= True)
  text = db.Column(db.String())  # precision: numbers after decimal point
  publish_date = db.Column(db.DateTime(), default=datetime.datetime.now)
  
  username = db.Column(db.String(), db.ForeignKey("users.username"))
  #store = db.relationship("StoreModel")

  def __init__(self, text: str, username: str, publish_date: datetime= datetime.datetime.now()):
    self.text = text
    self.username = username
    self.publish_date = publish_date

  def json(self) -> ChatJSON:
    return {
      "id": self.id,
      "text":self.text,
      "publish_date": self.publish_date, 
      "username": self.username
      }
    
  def __repr__(self):
        return f"<Chat, user:'{self.username}, text: {self.text}'>"


  @classmethod
  def find_all(cls) -> List["ChatModel"]:
    print(cls.query.all())
    return cls.query.all()

  # method to insert or update an item into database
  def save_to_database(self) -> None:
    db.session.add(self)  # session here is a collection of objects that wil be written to database
    db.session.commit()

  def delete_from_database(self) -> None:
    db.session.delete(self)
    db.session.commit()