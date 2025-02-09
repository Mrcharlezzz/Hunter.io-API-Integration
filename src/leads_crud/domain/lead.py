from pydantic import BaseModel


class Lead(BaseModel):
    id: str = None
    email : str = None
    first_name: str = None
    last_name: str = None
    position: str = None
    company: str = None
