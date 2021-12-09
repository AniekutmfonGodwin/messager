from enum import Enum
from uuid import uuid4



class BaseEnum(Enum):

    @classmethod
    def choices(cls):
        return [(i.value,i.name ) for i in cls]

    @classmethod
    def dict(cls):
        
        return [{"id":uuid4(),"value":i.value,"name":i.name } for i in cls]



class MessageStatus(BaseEnum):
    
    READ = "READ"
    SEND = "SEND"
    