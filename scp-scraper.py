from bs4 import BeautifulSoup as soup
import requests
import json
import asyncio
import time
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession
import sqlite3

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')

async def test(itemno,tag,minrating=0,session=None):
    print(f'{itemno} executed at ' + str(time.time()))
    link = f'http://www.scp-wiki.net/scp-{itemno}'
    try:
        skip = await fetch_html(link,session)
    except:
        return 'yeet'
    print(f'{itemno} comp at ' + str(time.time()))
    return SCP_scraper(skip,itemno,tag,link)

async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found
    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        return found

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html

def SCP_scraper(page,itemno,tag,link):

    skip = page
    scp = soup(skip, features="html.parser")
    page_tags = scp.select('div[class="page-tags"] span a')
    page_tags = [tag.string for tag in page_tags]
    rating = int(scp.select('span[class=\'number prw54353\']')[0].string[1:])
    author = 'not implimented'
    conn = sqlite3.connect('scps.db')
    itemno = re.sub('-','',itemno)
    print(itemno,rating,tag)
    with conn as scpdb:
        c = scpdb.cursor()
        try:
            c.execute('SELECT * FROM scp_main')
        except sqlite3.OperationalError:
            c.execute('CREATE TABLE scp_main (number INTEGER PRIMARY KEY, rating INTEGER , link TEXT)')
        finally:
            try:
                c.execute('INSERT INTO scp_main VALUES (:number,:rating,:link)',{'number':itemno,'rating':rating,'link':link})
            except sqlite3.IntegrityError:
                c.execute(f'UPDATE scp_main SET rating =:rating WHERE scp_main.number =:number',{'rating':rating,'number':itemno})

        for tag in page_tags:
            tag = re.sub('-','_',tag)
            try:
                c.execute(f'INSERT INTO {tag} VALUES (:number,:rating)',{'number':itemno,'rating':rating})
            except sqlite3.OperationalError:
                    c.execute(f'CREATE TABLE {tag} (number INTEGER PRIMARY KEY, rating INTEGER )')
                    c.execute(f'INSERT INTO {tag} VALUES (:number,:rating)', {'number': itemno, 'rating': rating})
            except sqlite3.IntegrityError:
                c.execute(f'UPDATE {tag} SET rating =:rating WHERE {tag}.number =:number',
                          {'number': itemno, 'rating': rating})


async def search_main(tag,minrating=0):

    res = []
    for j in range(2,3):
        output = []
        async with ClientSession() as session:
            for i in range(100*(j-1),100*j+1):
                if i < 100:
                    if i < 10:
                        no = f'00{i}'
                    else:
                        no = f'0{i}'
                else:
                    no = str(i)
                output.append(asyncio.create_task(test(no,tag,minrating,session)))
            output = await asyncio.gather(*output)
        res += output







if __name__ == '__main__':
    t = time.time()
    asyncio.run(search_main(None))
    print(time.time()-t)