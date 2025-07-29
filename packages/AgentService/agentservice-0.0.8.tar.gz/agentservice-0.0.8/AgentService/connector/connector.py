
import typing
import aiohttp

from .event import ToolEvent
from .event.utils import bind_event, dispatch_event

from AgentService.dtypes.message import SendMessageRequest


class AgentConnector:
    def __init__(
        self,
        endpoint: str,
        key: str = None
    ):

        self.endpoint = endpoint[:-1] if endpoint.endswith("/") else endpoint
        self.key = key

    def bind_tool_output(self, tool_name: str, function: typing.Callable):
        bind_event(ToolEvent, function, tool_name=tool_name)

    async def send(self, request: SendMessageRequest):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.endpoint}/chat",
                data=request.to_dict()
            ) as resp:
                return resp
