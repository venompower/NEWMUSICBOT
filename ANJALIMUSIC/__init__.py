from ANJALIMUSIC.core.bot import ANJALI
from ANJALIMUSIC.core.dir import dirr
from ANJALIMUSIC.core.git import git
from ANJALIMUSIC.core.userbot import Userbot
from ANJALIMUSIC.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = ANJALI()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
