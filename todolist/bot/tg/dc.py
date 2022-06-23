from dataclasses import dataclass, field
from datetime import datetime

import marshmallow
import marshmallow_dataclass

from typing import List, Optional


class BaseMeta:
    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Chat(BaseMeta):
     id: int 
     first_name:  Optional[str]
     last_name:  Optional[str]
     

@dataclass
class From(BaseMeta):
    id: int
    is_bot: bool
    
    first_name:  Optional[str]
    last_name: Optional[str]
    language_code: Optional[str]
    username: Optional[str]
  

@dataclass
class Message(BaseMeta):
    message_id: int
    from_: From
    chat: Chat
    date: int
    text: str
 
   
@dataclass 
class Result(BaseMeta):
    update_id: int
    message: Message
    
   

@dataclass
class GetUpdatesResponse(BaseMeta):
    ok: bool
    result: List[Result] = field(default_factory=list)
  

@dataclass
class SendMessageResult(BaseMeta):
    message_id: int
    date: int
    text: str
    chat: Chat
    from_: From
   

@dataclass
class SendMessageResponse(BaseMeta):
    ok: bool
    result: SendMessageResult
    

GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)()
SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)()
