
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

    async def answer_tool(self, event: ToolEvent, function: typing.Callable):
        resp = await function(event)

    async def send(self, chat_id: str, text: str = None, context: dict = {}):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.endpoint}/chat",
                data=SendMessageRequest(
                    chat_id=chat_id,
                    text=text,
                    context=context
                ).to_dict()
            ) as resp:
                return await resp.json()
