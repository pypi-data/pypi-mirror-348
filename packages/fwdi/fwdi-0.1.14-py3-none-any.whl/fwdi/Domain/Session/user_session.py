from datetime import datetime
from uuid import uuid4

class UserSession():
    def __init__(self):
        self.id:uuid4=uuid4()
        self.in_work:bool = False
        self.modify:datetime = datetime.now()
        self.user_data:dict = {}