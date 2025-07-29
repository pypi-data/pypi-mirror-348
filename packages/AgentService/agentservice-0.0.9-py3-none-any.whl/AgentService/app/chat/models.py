
from pydantic import BaseModel, Field


class ToolAnswer(BaseModel):
    id: str
    name: str
    text: str


class SendMessage(BaseModel):
    chat_id: str
    text: str = None
    context: dict = {}
    tool_answers: list[ToolAnswer] = []


class ChatStatus(BaseModel):
    chat_id: str
