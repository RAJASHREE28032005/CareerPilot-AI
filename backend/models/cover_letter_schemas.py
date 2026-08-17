from pydantic import BaseModel


class CoverLetter(BaseModel):
    recipient: str
    subject: str
    greeting: str
    body: str
    closing: str