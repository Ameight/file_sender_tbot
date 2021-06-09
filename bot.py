import asyncio
import logging
import os

from aiogram import Bot, types
from aiogram.types import message
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher, filters
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile

# FOR FSM
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from fsm_stage import TestStates
# FSM

from dirscan import listdir, listdir_countfile, create_dir, listdir_user, listdir_returnpath_user
from config import TOKEN


from DB_connector import get_files_user

bot = Bot(token=TOKEN)
# FOR FSM
dp = Dispatcher(bot, storage=MemoryStorage())
# FOR FSM

directory = 'user_files/'

#Отправляет список команд в ответ на /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if (os.path.exists(directory) == False):
        os.mkdir(directory)
    await message.reply('Привет!\nС помощью команды /help, ты сможешь узнать как пользоваться ботом и список доступных команд!')

#Отправляет список команд в ответ на /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text('Доброго времени суток!',
                        'Если ты пользовался системой сбора данных, с которой я связан, '
                        'то я проверю есть ли у меня для тебя доступные отчёты, '
                        'которые ты составлял ранее, просто введи команду ' + code('/all'),
                        '/all - посмотреть список всех отчётов, доступных для просмотра, доступных вам.',
                        'Если ты только запустил меня, то перед работой с системой нажми на кнопку ' + bold("Синхронизировать с Telegram"),
                        'Введи там свой никнейм в Telegram: ' + bold(message.from_user.username),
                        sep='\n\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

#Отправляет список файлов доступных для отправки определённому пользователю
@dp.message_handler(state = '*', commands=['all'])
async def process_all_command(message: types.Message):

    name = message.from_user.username
    diruser = directory + name
    state = dp.current_state(user=message.from_user.id)

    if(create_dir(directory, name) == 0): 
        msg = text('Репозитрий для вас создан!',
            'У вас пока нет файлов для просмотра, начните пользоваться системой !\n',
            'Нажимайте кнопку "Синхронизировать с telegram"')
        await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        get_files_user(diruser + '/', name)
        if(listdir_user(diruser)):
            msg = text('Файлы доступные для просмотра:\n', listdir_user(diruser) , 'Выберите номер интересующего вас файла.' , sep='\n')
            await state.set_state(TestStates.all()[1])
            await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
        else:
            msg = text('У вас пока нет файлов для просмотра.' , sep='\n')
            await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

#Отправка файлов определённому пользователю
@dp.message_handler(state=TestStates.TEST_STATE_1)
async def filter(msg: types.Message):

    di = msg.text                       # Записывает текст сообщения
    name = msg.from_user.username       # Имя пользователя
    dirname = directory + name + '/'    # Путь к папке пользователя

    state = dp.current_state(user=msg.from_user.id)

    if(di.isdigit()):
        tmp = int(msg.text)
        if (0 < tmp <= listdir_countfile(dirname)):
            
            user_id = msg.from_user.id

            await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT) # Уведомление об отправки файла
            await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю

            p = open(listdir_returnpath_user(dirname, tmp), 'rb')
            await bot.send_document(user_id, p,
                                    caption='Этот файл специально для тебя!')

        else:
            p = text('У меня такого файла нет :(', 'Вот список файлов доступных для тебя:' ,
             msg.from_user.username , listdir(dirname) ,
              'Выбери номер интересующего файла.' , sep='\n')
            await msg.reply(p, parse_mode=ParseMode.MARKDOWN)
    else:
        message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        '\nНапоминаю, что есть команда /help', emojize(':ok_hand:'))
        await state.reset_state()
        await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

# Отправка файлов
@dp.message_handler()
async def repl(msg: types.Message):
        message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        '\nНапоминаю, что есть команда /help', emojize(':ok_hand:')) 
        await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp)