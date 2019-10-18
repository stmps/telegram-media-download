import os
from telethon.sync import TelegramClient
# Refer to the documentation for other filter types.
# https://tl.telethon.dev/types/messages_filter.html
from telethon.tl.types import InputMessagesFilterPhotoVideo

api_id = os.environ['api_id']
api_hash = os.environ['api_hash']
channel = int(os.environ['channel'])
limit = int(os.environ.get('limit', 10))

with TelegramClient('session_name', api_id, api_hash) as client:

    for message in client.iter_messages(channel,
                                        limit=limit,
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
