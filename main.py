from os import listdir
from os.path import isfile, join

import requests
import bs4
from random import randint

from aiogram import Bot, Dispatcher
from aiogram.types import InputMediaPhoto, FSInputFile

import asyncio

ksusha_id = 165248174

bot = Bot('7699554251:AAGLVJl44I9EHxajPKnTnkZpZ3dO5PypPqo')
dp = Dispatcher()


async def get_poem():
    page = randint(0, 120)
    poem_num = randint(0, 9)
    if page == 0:
        url = 'https://pozdravok.com/pozdravleniya/prazdniki/den-svyatogo-valentina/'
    else:
        url = f'https://pozdravok.com/pozdravleniya/prazdniki/den-svyatogo-valentina/{page}.htm'
    response = requests.get(url)
    bs = bs4.BeautifulSoup(response.text, "lxml")
    texts = bs.find_all('p', {'class': 'sfst'})
    if len(texts) >= poem_num + 1:
        return texts[poem_num].get_text(separator='\n')  # noqa
    return texts[0].get_text(separator='\n')  # noqa


async def send_notification(text):
    await bot.send_message(ksusha_id, text=text)


async def main():
    mypath = './images'
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    media = [InputMediaPhoto(media=FSInputFile(path=f'./images/{file}')) for file in files]
    media1 = media[:10]
    media2 = media[10:]
    while True:
        try:
            await bot.send_media_group(chat_id=ksusha_id,
                                       media=media1)
            await bot.send_media_group(chat_id=ksusha_id,
                                       media=media2)
            await send_notification(await get_poem())
            print('Стих отправлен')
            await asyncio.sleep(3600)
        except Exception as e:  # noqa
            print(e)


if __name__ == '__main__':
    asyncio.run(main())
