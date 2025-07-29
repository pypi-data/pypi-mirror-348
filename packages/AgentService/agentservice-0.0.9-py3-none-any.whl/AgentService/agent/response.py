
import enum
from AgentService.dtypes.message import Tool


class AgentResponseType(enum.Enum):
    tools = "tools"
    answer = "answer"


class AgentResponse:
    def __init__(self, type: AgentResponseType, content: str | list[Tool]):
        self.type = type
        self.content = content

    def __str__(self):
        return "AgentResponse(type=" + self.type.value + ", content=" + str(self.content) + ")"
