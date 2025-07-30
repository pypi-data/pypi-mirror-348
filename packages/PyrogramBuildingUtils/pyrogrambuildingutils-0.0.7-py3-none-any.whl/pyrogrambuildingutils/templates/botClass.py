import inspect
import logging
import os
from types import MethodType
from typing import Any, Callable, Dict, Generator, List, Optional, overload

from dotenv import load_dotenv
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message

from src.utils.utils import Utils


async def _is_admin(_, __, m: Message) -> bool:
    return bool(
        m.from_user.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
        or m.chat.id == m.from_user.id
    )


admin = filters.create(_is_admin)


class Bot(Client):
    @Utils.init_time_measure()
    def __init__(self, *, logger_name: str = "pyrogram.bot"):
        load_dotenv()
        self.logger = logging.getLogger(logger_name)
        super().__init__(
            name=os.environ["BOT_NAME"],
            api_id=os.environ["API_ID"],
            api_hash=os.environ["API_HASH"],
            bot_token=os.environ["BOT_TOKEN"],
        )
        self.build_command_handlers()

    @overload
    def build_command_help(self, *, func_name: str) -> Dict[str, str]: ...
    @overload
    def build_command_help(
        self, *, func: Callable[..., Any] | MethodType
    ) -> Dict[str, str]: ...

    def build_command_help(
        self, *, func: Callable | MethodType | None = None, func_name: str | None = None
    ) -> Dict[str, str]:
        """
        Возвращает справку по команде на основе имени функции или ссылки на неё.
        """
        # Получаем имя функции
        name_raw = func_name or (
            func.__name__.replace("_admin", "")
            if func and hasattr(func, "__name__")
            else "Без имени"
        )
        display_name = ", ".join(name_raw[8:].split("_"))  # Убираем "command_"

        # Ищем метод с этим именем
        for _name, _func in self.get_methods():
            if _name == f"command_{name_raw}":
                doc = _func.__doc__ or "Без описания"
                return {"name": display_name, "doc": doc}

        # Если не нашли — использовать doc из func напрямую
        doc = (
            func.__doc__
            if func and hasattr(func, "__doc__") and func.__doc__
            else "Без описания"
        )
        return {"name": display_name, "doc": doc}

    def get_methods(
        self,
    ) -> Generator[tuple[str, MethodType | Callable[..., Any]], None, None]:
        for name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            if not name.startswith("command_"):
                continue
            if not inspect.iscoroutinefunction(func):
                continue
            yield name, func

    def build_command_handlers(self):
        """This function needed for collect functions in use for command handlers
        :obj:~pyrogram.handlers.message_handler.MessageHandler

        Usage:
            Create a function with a name starting with "command" and then you need to list
            the arguments for the commands that will be used to call your function
        Examples:
            >>> @staticmethod
            async def command_start(self, client: pyrogram.client.Client, message: pyrogram.types.Message) -> None:
                "Simple start command"
                await message.reply_text("Im working!")
        """
        for name, func in self.get_methods():
            commands = name.split("_")[1:]
            is_admin = False

            if commands and commands[-1] == "admin":
                is_admin = True
                commands = commands[:-1]

            filter_expr = filters.command(commands) if commands else filters.text

            if is_admin:
                filter_expr &= admin

            handler = MessageHandler(func, filter_expr)
            self.add_handler(handler)

    async def command_help_start(self, _: Client, message: Message) -> None:
        """Help command"""

        @overload
        def get_help(self: Bot) -> List[Dict[str, str]]: ...
        @overload
        def get_help(self: Bot, *, command: Optional[str]) -> Dict[str, str]: ...
        def get_help(
            self: Bot, *, command: Optional[str] = None
        ) -> Dict[str, str] | List[Dict[str, str]]:
            """
            Возвращает справку по одной или всем командам.

            Args:
                command (str, optional): Название команды (без префикса `command_`).

            Returns:
                Union[List[Dict[str, str]], Dict[str, str]]: Справка по одной или всем командам.
            """
            if command:
                func_name = f"command_{command}"
                return self.build_command_help(func_name=func_name)

            help_list: List[Dict[str, str]] = []
            for _, func in self.get_methods():
                help_info = self.build_command_help(func=func)
                help_list.append(help_info)

            return help_list

        args = message.content.split(" ")
        if len(args) > 1:

            result = get_help(self, command=args[1])
            text = f"{result["name"]} - {result["doc"]}"
        else:
            text: str = "```Команды:"
            for command in get_help(self):
                text += f"\n{command["name"]} - {command["doc"]}"
            text += "```"

        await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    async def command_echo(self, _: Client, message: Message) -> None:
        """ECHO Echo echo ᵉᶜʰᵒ"""
        await message.reply_text(" ".join(message.text.markdown.split(" ")[1:]))

    async def command_sayMyName_admin(self, _: Client, message: Message):
        """Commands for saying user`s full name (its really needed?)"""
        user = message.from_user
        full_name = " ".join(filter(None, [user.first_name, user.last_name]))
        await message.reply_text(f"Your name is {full_name}")
