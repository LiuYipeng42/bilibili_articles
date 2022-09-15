import asyncio
import aiohttp
import aiomysql
from aiohttp import client_exceptions
from bs4 import BeautifulSoup
import re


async def request(session, url):
    while True:
        try:
            async with session.get(url) as response:  # 发起请求get请求
                print(url)
                return await response.text(encoding='utf8')
        except (client_exceptions.ServerDisconnectedError, client_exceptions.ClientOSError,
                client_exceptions.ClientPayloadError, asyncio.exceptions.TimeoutError):
            print('network error!')
            await asyncio.sleep(1)


async def parser(html, cursor, conn):
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find(name="h1")

    if title != None:

        title = title.text

        article = ""

        for p in soup.find_all(name="p"):
            article += p.text + '\n'

        img_urls = ['"https:' + i['data-src'] +
                    '"' for i in soup.find_all(name="img")]

        if len(img_urls) != 0:
            img_urls = "[" + ', '.join(img_urls) + "]"
        else:
            img_urls = None

        author = soup.find(attrs={'name': 'author'})['content']

        profile_img = re.findall(
            '"face":"(.*?)"', soup.text)[0].encode('utf-8').decode("unicode_escape")

        await cursor.execute(
            "insert into bilibili_article (title, author, profile_img_url, article, img_urls) values (%s, %s, %s, %s, %s)",
            (title, author, profile_img, article, img_urls)
        )

        await conn.commit()


async def getArticle(url, pool, semaphore):
    async with semaphore:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                async with aiohttp.ClientSession() as session:  # 创建一个session用于发起请求
                    html = await request(session, url)

                    await parser(html, cursor, conn)


async def getArticleUrl(url, i, pool, semaphore):
    async with semaphore:

        article_urls = [url + str(i) for i in range(i, i + 150)]

        tasks = [getArticle(url, pool, semaphore) for url in article_urls]

        await asyncio.gather(*tasks)


async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='121522734a',
                                      db='Enclusiv', loop=loop, minsize=5, maxsize=150)
    semaphore = asyncio.Semaphore(300)

    base_url = "https://www.bilibili.com/read/cv"


    start_task = [getArticleUrl(base_url, i, pool, semaphore)
                  for i in range(1000000, 1015000, 250)]
    await asyncio.gather(*start_task)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(1))
loop.close()



