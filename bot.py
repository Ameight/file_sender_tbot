import asyncio
import logging
import os

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher, filters
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile


from dirscan import listdir, listdir_returnpath, listdir_countfile
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

directory = 'tmp/'


#Отправляет список команд в ответ на /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nС помощью команды /help, '
                        'ты сможешь усзнать список доступных команд!')

#Отправляет список команд в ответ на /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/all - посомотреть список всех отчётов, доступных для просмотра', '/пук', '/пук', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

#Отправляет список файлов доступных для отправки обратно
@dp.message_handler(commands=['all'])
async def process_help_command(message: types.Message):
    msg = text('Файлы доступные для просмотра:\n', listdir(directory) , 'Выберите номер интересующего вас файла.' , sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

#Отправка файлов
@dp.message_handler(commands=['doc'])
async def process_file_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT) #Уведомление об отправки файла
    await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю
    p = open(listdir_returnpath(directory, 7), 'rb')
    await bot.send_document(user_id, p,
                            caption='Этот файл специально для тебя!')

#Отправляет твоё же сообщение
#@dp.message_handler()
#async def echo_message(msg: types.Message):
#    await bot.send_message(msg.from_user.id, msg.text)

#Отправка файлов
@dp.message_handler()
async def filter(msg: types.Message):
    tmp = int(msg.text)
    if (0 < tmp <= listdir_countfile(directory)):
        user_id = msg.from_user.id
        await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT) #Уведомление об отправки файла
        await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю
        p = open(listdir_returnpath(directory, tmp), 'rb')
        await bot.send_document(user_id, p,
                                caption='Этот файл специально для тебя!')
    else:
        p = text('У меня такого файла нет :(', 'Вот список файлов доступных для тебя:' , listdir(directory) , 'Выбери номер интересующего файла.' , sep='\n')
        await msg.reply(p, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        '\nЯ просто напомню,', 'что есть',
                        code('команда'), '/help', emojize(':ok_hand:')) 
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

#@dp.message_handler()
#async def filter(msg: types.Message):
#    tmp = msg.text
#    if (0 < int(tmp) <= listdir_countfile(directory)):
#        await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)


