
import functools
import asyncio
import typing
import aiohttp
from aiogram.loggers import event

from .event import ToolEvent
from .event.utils import bind_event, dispatch_event

from AgentService.agent.response import AgentResponse, AgentResponseType
from AgentService.dtypes.message import SendMessageRequest, Tool, ToolAnswer


class AgentConnector:
    def __init__(
        self,
        endpoint: str,
        key: str = None
    ):

        self.endpoint = endpoint[:-1] if endpoint.endswith("/") else endpoint
        self.key = key

    def bind_tool_output(self, tool_name: str, function: typing.Callable):
        callback = functools.partial(self.answer_tool, function=function)
        bind_event(ToolEvent, callback, tool_name=tool_name)

    async def answer_tool(self, event: ToolEvent, function: typing.Callable) -> ToolAnswer:
        response = await function(data=event.tool.arguments)
        if not response:
            response = "function returned nothing"

        return ToolAnswer(
            id=event.tool.id,
            name=event.tool.name,
            text=response
        )

    async def handle_tools(self, tools: list[Tool]) -> list[ToolAnswer]:
        tool_answers = await asyncio.gather(*[
            dispatch_event(ToolEvent(tool_name=tool.name, tool=tool))
            for tool in tools
        ])

        return tool_answers

    async def request(self, request: SendMessageRequest) -> AgentResponse:
        print(request.to_dict())
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.endpoint}/chat",
                json=request.to_dict(),
                raise_for_status=True
            ) as resp:

                response = await resp.json()
                agent_response = AgentResponse(**response["data"])

                print(agent_response.to_dict())

                return agent_response

    async def send(self, chat_id: str, text: str = None, context: dict = {}, tool_answers: list[ToolAnswer] = []) -> AgentResponse:
        agent_response = await self.request(SendMessageRequest(chat_id=chat_id, text=text, context=context, tool_answers=tool_answers))

        if agent_response.type == AgentResponseType.answer:
            return agent_response

        tool_answers = await self.handle_tools(agent_response.content)

        return await self.send(chat_id, tool_answers=tool_answers)
