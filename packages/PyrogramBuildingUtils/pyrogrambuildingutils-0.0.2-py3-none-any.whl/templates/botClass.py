import os

from dotenv import load_dotenv
from pyrogram.client import Client

from src.utils.utils import Utils


class Bot(Client):
    @Utils.init_time_measure()
    def __init__(
        self,
    ):
        load_dotenv()

        super().__init__(
            name=os.environ["BOT_NAME"],
            api_id=os.environ["API_ID"],
            api_hash=os.environ["API_HASH"],
            bot_token=os.environ["BOT_TOKEN"],
        )
