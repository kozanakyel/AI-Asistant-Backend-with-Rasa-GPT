from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from json import JSONEncoder
import datetime
import json

from models.chat import ChatModel

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


ERROR_INSERTING_ITEM = "Sorry! An error occured inserting the chat!"
LOGIN_TO_VIEW_DATA = "Please first login to view more data!"

chat_parser = reqparse.RequestParser()
chat_parser.add_argument("text",
    type=str,
    required=True,
    help= "Question or text required"
  )
chat_parser.add_argument("username",
    type=str,
    required=True,
    help= "required username"
  )

class Chat(Resource):
  
  # TO GET ITEM WITH NAME
  @classmethod
  @jwt_required()
  def get(cls):
       
    return {"message": "Not allowed only one chat messages"}, 401

  # TO POST AN ITEM
  @classmethod
  @jwt_required(fresh=True)
  def post(cls):
    # if there already exists an item with "name", show a messege, and donot add the item
    
    data = chat_parser.parse_args()
    # data = request.get_json()   # get_json(force=True) means, we don't need a content type header
    chat = ChatModel(**data)

    try:
      chat.save_to_database()
    except:
      return {"message": ERROR_INSERTING_ITEM}, 500
    
    return chat.json(), 201  # 201 is for CREATED status


class ChatList(Resource):
  @classmethod
  @jwt_required(optional=True)
  def get(cls):
    user_id = get_jwt_identity()
    chats = [chat.json() for chat in ChatModel.find_all()]
    #chats = DateTimeEncoder().encode(chats)
    
    print(f"chat json?: {chats[2]['text']}")
    # if user id is given, then display full details
    if user_id:
      result = {"chats": chats}
      result = json.dumps(result, indent=4, cls=DateTimeEncoder)
      print(result)
      return result, 200

    # else display only item name
    return {
      "chats": f"Chat history text size is: {len(chats)}",
      "message": LOGIN_TO_VIEW_DATA
    }, 200