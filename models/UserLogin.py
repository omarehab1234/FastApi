from pydantic import BaseModel
from typing import Optional

class UserLog(BaseModel):
    email: str
    password: str