# https://docs.telethon.dev/en/latest/basic/quick-start.html

from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotoVideo
import os

api_id = os.environ['api_id']
api_hash = os.environ['api_hash']
channel = int(os.environ['channel'])

with TelegramClient('session_name', api_id, api_hash) as client:

    for message in client.iter_messages(channel,
                                        limit=10,
                                        filter=InputMessagesFilterPhotoVideo):

        filename = (f'{message.date.year}'
                    f'{message.date.month}-'
                    f'{message.text or "unknown"}-'
                    f'{message.file.id[-8:]}'
                    f'{message.file.ext}'
                    )

        if os.path.isfile(filename):
            print(f'{filename} already exists. Skipping.')
        else:
            print(f'{filename} downloading...')
            path = message.download_media(file=filename)
