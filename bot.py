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


from dirscan import listdir, listdir_countfile, create_dir, listdir_user, listdir_returnpath_user
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

directory = 'user_files/'

#Отправляет список команд в ответ на /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if (os.path.exists(directory) == False):
        os.mkdir(directory)
    await message.reply('Привет!\nС помощью команды /help, ты сможешь узнать список доступных команд!')

#Отправляет список команд в ответ на /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
                    '/all - посомотреть список всех отчётов, доступных для просмотра, доступных вам. ',
                    message.from_user.username, sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

#Отправляет список файлов доступных для отправки определённому пользователю
@dp.message_handler(commands=['all'])
async def process_alle_command(message: types.Message):

    name = message.from_user.username
    diruser = directory + name

    if(create_dir(directory, name) == 0): 
        msg = text('Репозитрий для вас создан!',
            'У вас пока нет файлов для просмотра, начните пользоваться системой !\n',
            'Нажимайте кнопку "Синхронизировать с telegram"')
        await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        if(listdir_user(diruser)):
            msg = text('Файлы доступные для просмотра:\n', listdir_user(diruser) , 'Выберите номер интересующего вас файла.' , sep='\n')
            await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
        else:
            msg = text('Вы авторизированы в системе!', 'У вас пока нет файлов для просмотра.' , sep='\n')
            await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

#Отправка файлов определённому пользователю
@dp.message_handler()
async def filter(msg: types.Message):

    di = msg.text                       #Записывает текст сообщения
    name = msg.from_user.username       #Имя пользователя
    dirname = directory + name + '/'    #Путь к папке пользователя

    if(di.isdigit()):
        tmp = int(msg.text)
        if (0 < tmp <= listdir_countfile(dirname)):
            
            user_id = msg.from_user.id

            await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT) #Уведомление об отправки файла
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
                        '\nЯ просто напомню,', 'что есть',
                        'команда', code('/help'), emojize(':ok_hand:')) 
        await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

#Отправка файлов#
# @dp.message_handler()
# async def filter(msg: types.Message):
#     di = msg.text
#     if(di.isdigit()):
#         tmp = int(msg.text)
#         if (0 < tmp <= listdir_countfile(directory)):
#             user_id = msg.from_user.id
#             await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT) #Уведомление об отправки файла
#             await asyncio.sleep(1)  # скачиваем файл и отправляем его пользователю
#             p = open(listdir_returnpath(directory, tmp), 'rb')
#             await bot.send_document(user_id, p,
#                                     caption='Этот файл специально для тебя!')
#         else:
#             p = text('У меня такого файла нет :(', 'Вот список файлов доступных для тебя:' , msg.from_user.username , listdir(directory) , 'Выбери номер интересующего файла.' , sep='\n')
#             await msg.reply(p, parse_mode=ParseMode.MARKDOWN)
#     else:
#         message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
#                         '\nЯ просто напомню,', 'что есть',
#                         code('команда'), '/help', emojize(':ok_hand:')) 
#     await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp)