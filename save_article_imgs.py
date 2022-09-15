import asyncio
import aiohttp
import aiomysql
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


async def save_user_img(user_id, pool, semaphore):
    async with semaphore:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                async with aiohttp.ClientSession() as session:

                    img_index = 0;

                    for article_id, img_urls in data[user_id].items():
                        article_img_paths = []
                        for url in img_urls:
                            img_name = str(img_index) + url[-4:]
                            img_path = "ArticleImages/" + str(user_id) + "/" + img_name
                            try:
                                with open(img_path, 'wb') as f:
                                    f.write(await request(session, url))
                            except aiohttp.client_exceptions.InvalidURL:
                                with open(img_path, 'wb') as f:
                                    f.write(await request(session, url[5:]))

                            print(user_id, article_id, img_index)

                            await cursor.execute("insert into image (name, user_id, path) values (%s, %s, %s)", (img_name, user_id, img_path))

                            article_img_paths.append(img_path)
                            img_index += 1

                            
                        await cursor.execute("update bilibili_article set img_paths=%s where id=%s", ("[" + ', '.join(article_img_paths) + "]", article_id))
                        await conn.commit()
        

async def main():

    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='xxxxxxxxx',
                                      db='Enclusiv', loop=loop, minsize=5, maxsize=150)

    semaphore = asyncio.Semaphore(100)

    tasks = [save_user_img(user_id, pool, semaphore) for user_id in data.keys()]
    await asyncio.gather(*tasks)


data = eval(open("new_data.txt", "r").read())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(1))
loop.close()
