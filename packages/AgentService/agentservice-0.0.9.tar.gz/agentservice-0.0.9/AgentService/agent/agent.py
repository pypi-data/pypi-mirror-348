
from loguru import logger
from uuid import uuid4
from openai import AsyncOpenAI

from .agent_tool import AgentTool
from .response import AgentResponse, AgentResponseType

from AgentService.db import Db
from AgentService.dtypes.db import method as dmth
from AgentService.dtypes.chat import Chat, ChatStatus
from AgentService.dtypes.message import Message, MessageType, ToolAnswer


class Agent:
    model: str = "gpt-4.1-nano"
    temperature: float = 1.0
    max_tokens: int = 2048
    top_p: float = 1.0

    system_prompt: str = "You are a helpful assistant"
    prompt: str = "{text}"

    is_one_shot: bool = False

    def __init__(
        self,
        openai_key: str,
        tools: list[AgentTool] = None,
    ):

        self.log = logger.bind(classname=self.__class__.__name__)
        self.db = Db()
        self.client = AsyncOpenAI(api_key=openai_key)

        self.tools = tools if tools else []
        self.tools_schema = [{"type": "function", "function": tool.to_schema} for tool in self.tools]

    async def __system_prompt(self, context: dict) -> str:
        return self.system_prompt.format(**context)

    async def __prompt(self, text: str, context: dict) -> str:
        return self.prompt.format(text=text, **context)

    async def __generate(self, chat: Chat) -> AgentResponse:
        chat.status = ChatStatus.generating
        await self.db.ex(dmth.UpdateOne(Chat, chat, to_update="status"))

        messages: list[Message] = await self.db.ex(dmth.GetMany(Message, chat_id=chat.id))
        gpt_messages = list(map(lambda x: x.gpt_dump, messages))

        if len(self.tools_schema):
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=gpt_messages,
                tools=self.tools_schema,
                tool_choice="auto"
            )

        else:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=gpt_messages
            )

        message = response.choices[0].message
        if message.tool_calls:
            return AgentResponse(
                type=AgentResponseType.tools,
                content=[
                    AgentTool(
                        id=tool_call.id,
                        name=tool_call.function.name,
                        arguments=tool_call.function.arguments
                    )
                    for tool_call in message.tool_calls
                ]
            )

        return AgentResponse(
            type=AgentResponseType.answer,
            content=message.content
        )

    async def generate(self, chat: Chat) -> AgentResponse:
        try:
            return await self.__generate(chat)

        except Exception as err:
            self.log.exception(err)

            return AgentResponse(
                type=AgentResponseType.answer,
                content=str(err)
            )

    async def get_chat(self, chat_id: str, context: dict = {}) -> Chat:
        chat: Chat = await self.db.ex(dmth.GetOne(
            Chat,
            chat_id=chat_id,
            status={
                "$in": [ChatStatus.created.value, ChatStatus.idle.value, ChatStatus.tools.value]
            }
        ))
        if not chat:
            chat = Chat(
                id=uuid4().hex,
                chat_id=chat_id,
                status=ChatStatus.created,
                data=context
            )
            await self.db.ex(dmth.AddOne(Chat, chat))

        system_message: Message = await self.db.ex(dmth.GetOne(Message, chat_id=chat.id, type=MessageType.system.value))
        if not system_message:
            system_message = Message(
                id=uuid4().hex,
                chat_id=chat.id,
                text=await self.__system_prompt(context),
                type=MessageType.system
            )
            await self.db.ex(dmth.AddOne(Message, system_message))

        return chat

    async def proccess_answer(self, answer: AgentResponse, chat: Chat) -> AgentResponse:
        if answer.type == AgentResponseType.tools:
            bot_message = Message(
                id=uuid4().hex,
                chat_id=chat.id,
                type=MessageType.tools,
                tools=answer.content
            )
            chat.status = ChatStatus.tools

        elif answer.type == AgentResponseType.answer:
            bot_message = Message(
                id=uuid4().hex,
                chat_id=chat.id,
                type=MessageType.assistant,
                text=answer.content
            )
            chat.status = ChatStatus.finished if self.is_one_shot else ChatStatus.idle

        else:
            raise ValueError("wrong answer type")

        await self.db.ex(dmth.AddOne(Message, bot_message))
        await self.db.ex(dmth.UpdateOne(Chat, chat, to_update="status"))

        return answer

    async def skip_tools(self, chat) -> str:
        messages: list[Message] = await self.db.ex(dmth.GetMany(Message, chat_id=chat.id))
        last_message: Message = messages[-1]

        if not last_message.tools:
            chat.status = ChatStatus.idle
            await self.db.ex(dmth.UpdateOne(Chat, chat, to_update="status"))
            return chat

        new_messages = [
            Message(
                id=uuid4().hex,
                chat_id=chat.id,
                type=MessageType.tool_answer,
                tool_answer=ToolAnswer(
                    id=tool.id,
                    name=tool.name,
                    text="Tool call skipped."
                )
            )
            for tool in last_message.tools
        ] + [
            Message(
                id=uuid4().hex,
                chat_id=chat.id,
                type=MessageType.assistant,
                text="skip"
            )
        ]
        await self.db.ex(dmth.AddMany(Message, new_messages))

        return chat

    async def answer_text(self, chat_id: str, text: str, context: dict = {}) -> AgentResponse:
        chat = await self.get_chat(chat_id, context)
        if chat.status == ChatStatus.tools:
            chat = await self.skip_tools(chat)

        user_message = Message(
            id=uuid4().hex,
            chat_id=chat.id,
            text=await self.__prompt(text, context),
            type=MessageType.user
        )
        await self.db.ex(dmth.AddMany(Message, user_message))

        answer = await self.generate(chat=chat)
        await self.proccess_answer(answer, chat)

        return answer

    async def answer_tools(self, chat_id: str, tool_answers: list[ToolAnswer] = None) -> AgentResponse:
        chat = await self.get_chat(chat_id)

        if chat.status != ChatStatus.tools:
            return AgentResponse(type=AgentResponseType.answer, content="No tools to answer")

        new_messages = []
        for tool_answer in tool_answers:
            new_messages.append(Message(
                id=uuid4().hex,
                chat_id=chat.id,
                type=MessageType.tool_answer,
                tool_answer=tool_answer
            ))
        await self.db.ex(dmth.AddMany(Message, new_messages))

        answer = await self.generate(chat=chat)
        await self.proccess_answer(answer, chat)

        return answer

    async def answer(self, chat_id: str, text: str = None, context: dict = {}, tool_answers: list[ToolAnswer] = None) -> AgentResponse:
        if text:
            return await self.answer_text(chat_id, text, context)

        elif len(tool_answers):
            return await self.answer_tools(chat_id, tool_answers)

        else:
            raise ValueError("Need text or tool answers to answer")
