from bots.telegram_bot import TelegramBot
from epure.files import IniFile
import asyncio

if __name__ == '__main__':
    config = IniFile('./pyt/pyconfig.ini')
    bot = TelegramBot(config)
    asyncio.run(bot.start())