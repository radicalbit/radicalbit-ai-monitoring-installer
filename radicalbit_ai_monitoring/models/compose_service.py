from pydantic import BaseModel

from typing import Optional


class ComposeService(BaseModel):
    name: str
    image: str
    tag: str
    ports: Optional[list] = None
    volumes: Optional[list] = None
    environment: Optional[list] = None
    command: Optional[list] = None
