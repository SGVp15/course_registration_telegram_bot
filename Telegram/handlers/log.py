import os

from aiogram import types, F
from aiogram.types import FSInputFile

from Config.config import SELLERS, LOG_FILE, WEBINAR_LOG, LOG_BACKUP
from Telegram.Call_Back_Data import callBackData
from Telegram.config import USERS_ID, ADMIN_ID
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot
from Webinar.API import get_all_registration_url
from Zoom.queue_zoom import get_queue, clear_queue


def is_empty_file(file) -> bool:
    if not os.path.exists(file):
        with open(file=file, mode="w", encoding='utf-8') as f:
            f.write('')
    with open(file=file, mode="r", encoding='utf-8') as f:
        s = f.read()
    return len(s) <= 10


@dp.callback_query((F.data == callBackData.show_queue)
                   & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def show_queue(callback_query: types.callback_query):
    await bot.send_message(chat_id=callback_query.from_user.id, text=get_queue(), reply_markup=inline_kb_main)


@dp.callback_query(F.data.in_({callBackData.get_log, callBackData.get_seller})
                   & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def get_file(callback_query: types.callback_query):
    query = callback_query.data
    file = LOG_FILE
    if query == callBackData.get_seller:
        file = FSInputFile(SELLERS, filename='sellers.txt')
    elif query == callBackData.get_log:
        file = FSInputFile(LOG_FILE, filename='log_file.txt')

    try:
        if is_empty_file(file.path):
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'✅ Файл пустой',
                                   reply_markup=inline_kb_main)
        else:
            await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)
    except UnicodeDecodeError:
        ...


@dp.callback_query((F.data == callBackData.get_registration_webinar)
                   & (F.from_user.id.in_({*ADMIN_ID, *USERS_ID})))
async def get_file_registration_webinar(callback_query: types.callback_query):
    file = WEBINAR_LOG
    get_all_registration_url()
    if is_empty_file(file):
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'Очередь Webinar пустая',
                               reply_markup=inline_kb_main)
    else:
        file = FSInputFile(WEBINAR_LOG, filename='webinar.log')
        await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)


@dp.callback_query((F.data == callBackData.clear_queue) & (F.from_user.id.in_({*ADMIN_ID})))
async def clear_queue_file(callback_query: types.callback_query):
    clear_queue()
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_queue  Ok', reply_markup=inline_kb_main)


@dp.callback_query((F.data == callBackData.clear_log) & (F.from_user.id.in_({*ADMIN_ID})))
async def clear_log_file(callback_query: types.callback_query):
    try:
        with open(file=LOG_FILE, mode="r", encoding='utf-8') as f:
            s = f.read()
        with open(file=LOG_BACKUP, mode="a", encoding='utf-8') as f:
            f.write(s + '\n')
        with open(file=LOG_FILE, mode="w", encoding='utf-8') as f:
            f.write('')
    except Exception:
        ...
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_log Ok', reply_markup=inline_kb_main)
