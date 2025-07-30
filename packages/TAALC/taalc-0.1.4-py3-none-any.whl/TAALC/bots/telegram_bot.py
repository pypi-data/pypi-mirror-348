from .worker import Worker
from aiogram import Bot, Dispatcher, types, Router
# from asyncio import sleep, ensure_future, create_task
# from .statistic_bot import StatisticBot
# from .trading_bot import TradingBot
from epure.files import IniFile
from aiogram.filters.command import Command, CommandStart
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, JOIN_TRANSITION
from argparse import ArgumentParser
from aiogram.enums.chat_type import ChatType
from aiogram.types import ChatMemberUpdated


class TelegramBot(Worker):
    bot_token:str
    bot:Bot
    dsp:Dispatcher
    config:IniFile

    def __init__(self, config:IniFile):
        self.bot_token = config.bot_token
        self.config = config
        self.bot = Bot(self.bot_token)        
        self.dsp = Dispatcher()
        # self.dsp.message(self.init_user_chat, commands=['start'])           
        self.dsp.message()(self.message_handler)        
        self.dsp.message(CommandStart())(self.init_user_chat)

        router = Router()
        
        self.dsp.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))(self.new_member)
        # self.dsp.register_message_handler(self.trade, commands=['trade'])
        # self.dsp.register_message_handler(self.stats, commands=['stats'])
        # self.dsp.register_message_handler(self.stop, commands=['stop'])
        # self.dsp.register_message_handler(self.message_handler)        
  

    
    # @dsp.message(Command("start"))
    async def init_user_chat(self, message: types.Message):
        # self.start_stats(self.bot)        
        await message.reply("Добро пожаловать на сервер шизофрения :)))000")

    async def message_handler(self, message: types.Message):
        if message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            bot_id = self.bot.id
            if message.text and 'марат' in message.text.lower():
                if 'пиво' in message.text.lower():
                    await message.reply(f"где сходка?")
                else:
                    await message.reply(f"{message.from_user.first_name} - шлюха")
            elif message.reply_to_message.from_user.id == bot_id:
                await message.reply(f"мамку ебал")
                
        else:
            await message.answer("пососи потом проси")
            # await message.answer(f'На колени, животное, <b>ты</b>!\n'+
            #                'Прочитай наши правила, и потом не говори, что ты не знал, петух:\n'+
            #                '<a href="https://t.me/polysap_rules/2">Правила полисап</a>', parse_mode="HTML")
        # await dp.bot.send_message(dp.chat.id, 'собачка')

    async def new_member(self, event: ChatMemberUpdated):
        await event.answer(f'На колени, животное, <b>{event.new_chat_member.user.first_name}</b>!\n'+
                           'Прочитай наши правила, и потом не говори, что ты не знал, петух:\n'+
                           '<a href="https://t.me/polysap_rules/2">Правила полисап</a>', parse_mode="HTML")
        # await event.answer(f"<b>Hi, {event.new_chat_member.user.first_name}!</b>",
        #             parse_mode="HTML")
    # async def handle_group_message(self, message: types.Message):
    #     if "бот" in message.text.lower():
    #         await message.reply("я здесь, не ори :)")


        
    async def start(self):
        await self.dsp.start_polling(self.bot, skip_updates=True)

    # async def init_user_chat(self, message):
    #     await message.reply("Добро пожаловать на сервер шизофрения :)))000")

    # async def trade(self, message):
    #     # answer = await dp.bot.send_message(dp.chat.id, 'введите логины и пароли:')
    #     bot = TradingBot(self.config)
    #     bot.start()

    # def start_stats(self, bot):
    #     if not (hasattr(self,'statistic_bot') and self.statistic_bot):
    #         self.statistic_bot = StatisticBot(self.config, bot)
    #     self.statistic_bot.start()

    # async def stats(self, message):
    #     await message.reply("статистика запускается...")
    #     self.start_stats(message.bot)
    #     await message.reply("статистика запущена")

    async def stop(self, message):
        if hasattr(self, "statistic_bot") and not self.statistic_bot == None:
            self.statistic_bot.stop()
            await message.reply("статистика остановлена")
        else:
            await message.reply("ты пес обоссаный")




    def create_parser() -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument("--token", help="Telegram Bot API Token")
        parser.add_argument("--chat-id", type=int, help="Target chat id")
        parser.add_argument("--message", "-m", help="Message text to sent", default="Hello, World!")

        return parser