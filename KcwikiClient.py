import asyncio
import datetime
import json

import aiohttp
from aiohttp.client_exceptions import ContentTypeError

from KcwikiClientException import KcwikiClientException


class KcwikiClient:
    kcwikiAPIUrl = 'https://zh.kcwiki.org/api.php'
    kcdataUrl = 'https://kcwikizh.github.io/kcdata/ship/all.json'

    def __init__(self):
        self.loginToken = ''
        self.editToken = ''
        headers = {
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }

        self.timestamp = str(
            datetime.datetime.now().strftime(r'%Y_%m_%d')
        )
        self.config = self.loadConfig()
        self.connector = aiohttp.TCPConnector(
            verify_ssl=False,
            use_dns_cache=True
        )
        self.session = aiohttp.ClientSession(
            connector=self.connector, headers=headers
        )

    def loadConfig(self):
        with open('config.json', 'r', encoding='utf-8') as fp:
            return json.load(fp)

    def request(self, url, method='GET', rdata=None, timeout=10):
        return self.session.request(
            method=method,
            data=rdata, url=url,
            timeout=timeout
        )

    async def login(self):
        rdata = {
            'action': 'query',
            'meta': 'tokens',
            'type': 'login',
            'format': 'json'
        }
        async with self.request(self.kcwikiAPIUrl, 'POST', rdata) as resp:
            try:
                resp_json = await resp.json()
                if not resp_json:
                    raise KcwikiClientException('Failed to get login token!')
                self.loginToken = resp_json['query']['tokens']['logintoken']
            except aiohttp.client_exceptions.ContentTypeError:
                raise KcwikiClientException('Failed to get login token!')
        rdata = {
            'action': 'login',
            'format': 'json',
            'lgtoken': self.loginToken
        }
        username = input('Plz input your username: ')
        rdata['lgname'] = username
        rdata['lgpassword'] = input('Now input your password: ')
        async with self.request(self.kcwikiAPIUrl, 'POST', rdata) as resp:
            try:
                resp_json = await resp.json()
                if not resp_json:
                    raise KcwikiClientException('Failed to log in!')
                if resp_json['login']['result'] == 'Failed':
                    raise KcwikiClientException(resp_json['login']['reason'])
            except aiohttp.client_exceptions.ContentTypeError:
                raise KcwikiClientException('Failed to log in!')
        rdata = {
            'action': 'query',
            'meta': 'tokens',
            'format': 'json'
        }
        async with self.request(self.kcwikiAPIUrl, 'POST', rdata) as resp:
            try:
                resp_json = await resp.json()
                if not resp_json:
                    raise KcwikiClientException('Failed to get edit token!')
                self.editToken = resp_json['query']['tokens']['csrftoken']
            except aiohttp.client_exceptions.ContentTypeError:
                raise KcwikiClientException('Failed to get edit token!')

        if self.editToken == '+\\':
            raise KcwikiClientException('Incorrect edittoken \'+\\\' !')
        print('Login as "{}" Successfully!'.format(username))

    def __del__(self):
        loop = asyncio.get_event_loop()
        self.session.connector.close()
        asyncio.run_coroutine_threadsafe(self.session.close(), loop)


__all__ = ['KcwikiClient']
