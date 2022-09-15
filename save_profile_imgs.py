import asyncio
import aiohttp
import aiomysql
import pymysql
from aiohttp import client_exceptions


async def request(session, url):
    while True:
        try:
            async with session.get(url) as response:
                return await response.read()
        except (client_exceptions.ServerDisconnectedError, client_exceptions.ClientOSError,
                client_exceptions.ClientPayloadError, asyncio.exceptions.TimeoutError):
            print('network error!')
            await asyncio.sleep(1)


async def save_img(data, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:  # 创建一个session用于发起请求
            with open("ProfilePictures/" + str(data[0]) + data[1][-4:], 'wb') as f:
                f.write(await request(session, data[1]))
                print(data[0])


async def main():

    semaphore = asyncio.Semaphore(100)

    tasks = [save_img(data, semaphore) for data in img_data]
    await asyncio.gather(*tasks)


db = pymysql.connect(host='localhost', user='root',
                     password='xxxxxxxxx', port=3306, db='Enclusiv')

cursor = db.cursor()

sql = "select user.id, t.profile_img_url from user, (select DISTINCT author, profile_img_url from bilibili_article) as t where user.name = t.author"

cursor.execute(sql)

img_data = cursor.fetchall()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(1))
loop.close()
