from typing import Optional

from pydantic import BaseModel


class Lead(BaseModel):
    id: Optional[str] = None
    email : Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None
