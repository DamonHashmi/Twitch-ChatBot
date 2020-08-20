import twitchio
from irc.bot import SingleServerIRCBot
# from profanity_filter import ProfanityFilter
from requests import get
from lib import db, cmds, react
from check import check_profanity

# from profanity_filter import ProfanityFilter


NAME = "hashmidamon"
OWNER = "hashmidamon"


class Bot(SingleServerIRCBot):

    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = OWNER
        self.CLIENT_ID = "7ngs9r8jvognfar513820c7kpl37je"
        self.TOKEN = "qgeitqger4vmbt00ym166muwikx8y6"
        self.CHANNEL = f"#{OWNER}"
        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": 'application/vnd.twitchtv.v5+json'}
        resp = get(url, headers=headers).json()

        print(resp)
        self.channel_id = resp["users"][0]["_id"]

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)
        print(self.channel_id)

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")
        cxn.join(self.CHANNEL)
        db.build()
        self.send_message_on_Start("Bitch I am Now online!")

    @db.with_commit
    def on_pubmsg(self, cxn, event):

        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]
        print(str(message))

        if user['name'] != NAME:
            print(user['name'])
            react.process(bot, user, message)
            cmds.process(bot, user, message)

        # print(f"Message from {user['name']}: {message}")

    def send_message(self, message):
        print(str(message))
        self.connection.privmsg(self.CHANNEL, message)
        print(message)

    def send_message_on_Start(self, message):

        self.connection.privmsg(self.CHANNEL, message)


if __name__ == "__main__":
    bot = Bot()
    bot.start()
