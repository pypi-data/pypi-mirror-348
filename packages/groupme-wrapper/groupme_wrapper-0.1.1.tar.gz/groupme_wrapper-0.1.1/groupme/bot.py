import requests
from typing import Optional, List, Union
from .attachments import Location, GroupMeImage


class GroupMeBot:
    """
    A class representing a GroupMe bot.
    """

    def __init__(
        self,
        access_token: str,
        bot_id: str,
        name: str,
        group_id: str,
        group_name: str,
        dm_notification: bool,
        active: bool,
        avatar_url: str,
        callback_url: str,
    ):
        """
        Initializes the `GroupMeBot` with the given bot ID.
        Do not call yourself, use `GroupMeBot.create_bot()` or `get_bot()` instead.

        :param access_token: The access token for the GroupMe API.
        :param bot_id: The ID of the bot.
        :param name: The name of the bot.
        :param group_id: The ID of the group the bot is in.
        :param dm_notification: I'll be real, no clue what this one does.
        :param active: Whether the bot is active.
        :param avatar_url: The URL of the bot's avatar.
        :param callback_url: The URL to send callbacks to.
        """
        self.access_token = access_token
        self.bot_id = bot_id
        self.name = name
        self.group_id = group_id
        self.group_name = group_name
        self.dm_notification = dm_notification
        self.active = active
        self.avatar_url = avatar_url
        self.callback_url = callback_url

    def __repr__(self):
        return f"GroupMeBot({self.bot_id})"

    def __str__(self):
        return f"GroupMeBot({self.bot_id}, {self.name})"

    def send_message(
        self, message: str, attachments: List[Union[Location, GroupMeImage]] = None
    ):
        """
        Sends a message using the bot.

        :param message: The message to send.
        :param attachments: A list of attachments to include with the message. Must be of type `Location` or `GroupMeImage`.
        :raises Exception: If the message fails to send.
        """

        payload = {
            "bot_id": self.bot_id,
            "text": message,
        }
        if attachments:
            payload["attachments"] = [attachment.dict() for attachment in attachments]

        res = requests.post(
            "https://api.groupme.com/v3/bots/post?token=" + self.access_token,
            json=payload,
        )
        if res.status_code >= 300:
            raise Exception(f"Failed to send message: {res.status_code} {res.text}")

    @classmethod
    def create_bot(
        cls,
        access_token: str,
        name: str,
        group_id: str,
        avatar_url: str = None,
        callback_url: str = None,
        dm_notification: bool = False,
        active: bool = True,
    ):
        payload = {
            "name": name,
            "group_id": group_id,
            # "dm_notification": dm_notification,
            # "active": active
        }
        # if avatar_url is not None:
        #     payload["avatar_url"] = avatar_url
        # if callback_url is not None:
        #     payload["callback_url"] = callback_url

        res = requests.post(
            "https://api.groupme.com/v3/bots?token=" + access_token,
            json={"bot": payload},
        )

        if res.status_code >= 300:
            raise Exception(f"Failed to create bot: {res.status_code} {res.text}")

        bot = res.json()
        return cls(
            access_token,
            bot["response"]["bot"]["bot_id"],
            name,
            group_id,
            bot["response"]["bot"]["group_name"],
            dm_notification,
            active,
            avatar_url,
            callback_url
        )


def get_bots(access_token):
    res = requests.get("https://api.groupme.com/v3/bots?token=" + access_token)

    if res.status_code >= 300:
        raise Exception(f"Failed to get bots: {res.status_code} {res.text}")

    return [
        GroupMeBot(
            access_token,
            bot["bot_id"],
            bot["name"],
            bot["group_id"],
            bot["group_name"],
            bot["dm_notification"],
            bot["active"],
            bot["avatar_url"],
            bot["callback_url"]
        )
        for bot in res.json()["response"]
    ]


def get_bot(access_token, bot_id):
    bots = get_bots(access_token)
    if len(bots) == 0:
        raise Exception("No bots found.")

    bot = next((bot for bot in bots if bot.bot_id == bot_id), None)
    if bot is None:
        raise Exception(f"Bot with ID {bot_id} not found.")
    return bot
