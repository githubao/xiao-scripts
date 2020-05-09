#!/usr/bin/env python
# encoding: utf-8

"""
@description: telegram photos

@author: baoqiang
@time: 2020/3/8 3:21 下午
"""

from telethon.sync import TelegramClient, events

api_id = 1372901
api_hash = "8ca256c53d4384ff4f80574120a47358"


def run():
    with TelegramClient('name', api_id, api_hash) as client:
        client.send_message('me', 'Hello, myself!')
        print(client.download_profile_photo('me'))

        # @client.on(events.NewMessage(pattern='(?i).*Hello'))
        # async def handler(event):
        #     await event.reply('Hey!')
        #
        # client.run_until_disconnected()


if __name__ == '__main__':
    run()
