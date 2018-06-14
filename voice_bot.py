#!/usr/bin/env python3

import asyncio
import sys

from KcwikiVoiceClient import KcwikiVoiceClient


def printHelp():
    print('''kcwiki_bot - kcwiki语音更新助手

用法:

    python voice_bot.py [command]

命令:

\tfix(f)\t\t修复更新语音下载
\tdownload(d)\t查看更新语音并下载
\tupload(u)\t上传语音到zh.kcwiki.moe（必须已下载语音文件）
\tgenwiki(g)\t生成wikicode

使用 "python voice_bot.py help" 查看帮助。
''')


async def main():
    voiceClient = KcwikiVoiceClient()

    if len(sys.argv) == 2:
        if sys.argv[1] == 'download' or sys.argv[1] == 'd':
            print('start to download.')
            await voiceClient.downloadVoice()
        elif sys.argv[1] == 'fix' or sys.argv[1] == 'f':
            print('start fixing.')
            await voiceClient.fixRetryVoice()
        elif sys.argv[1] == 'upload' or sys.argv[1] == 'u':
            print('start to upload.')
            await voiceClient.removeDuplicatedVoice()
            await voiceClient.uploadVoice()
        elif sys.argv[1] == 'genwiki' or sys.argv[1] == 'g':
            print('start to generate wikicode.')
            await voiceClient.generateWikiCode()
        elif sys.argv[1] == 'help' or sys.argv[1] == 'h':
            printHelp()
        else:
            printHelp()
        print()
    else:
        printHelp()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
