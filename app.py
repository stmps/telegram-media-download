import argparse
import os
import typing
from pathlib import Path

from progress.bar import Bar
from telethon import types
from telethon.sessions import Session
from telethon.sync import TelegramClient


class DownloadBar(Bar):
    import sys

    check_tty = False  # required for e.g. PyCharm or Jupyter Notebook
    file = sys.stdout
    suffix = '%(percent).1f%% - %(filesize_kbytes)d KB'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self, received, total):
        self.max = total
        self.index = received
        self.next()

    @property
    def filesize_kbytes(self):
        return self.max // 1024


class TelegramMediaDownload(TelegramClient):
    def __init__(self, session: 'typing.Union[str, Session]',
                 api_id,
                 api_hash,
                 channel: int = None,
                 limit: int = None):

        super().__init__(session, api_id, api_hash)
        self.channel = channel
        self.limit = limit

    def list_channels(self):
        for d in self.iter_dialogs():
            print(f'{d.name}: {d.id}')

    def download_all_media(self):
        # Refer to the documentation for other filter types.
        # https://tl.telethon.dev/types/messages_filter.html
        message_filter = types.InputMessagesFilterPhotoVideo

        for message in client.iter_messages(self.channel, limit=self.limit, filter=message_filter):
            # You lose the original filename when you share a file in a Telegram chat.
            # So we construct a new, and hopefully unique, filename.
            path = Path('_'.join([
                message.date.strftime("%Y%m%d"),
                str(message.chat_id),
                message.file.id,
                message.file.ext
            ]))

            if os.path.isfile(path) and message.file.size == os.path.getsize(path):
                print(f'File already exists: {path}')
            else:
                bar = DownloadBar(message=f'Downloading: {path}')
                path = message.download_media(file=path, progress_callback=bar.callback)
                bar.finish()


def get_args():
    parser = argparse.ArgumentParser(description='Download media from a Telegram channel (or private chat).')
    parser.add_argument("--list-channels", help="List all channel IDs", action="store_true")
    parser.add_argument("--limit", help="Only download the last n items", type=int, default=0)
    parser.add_argument("api_id", help="API ID")
    parser.add_argument("api_hash", help="API Hash")
    parser.add_argument("channel", help="Channel ID", type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    with TelegramMediaDownload('session_name', args.api_id, args.api_hash, args.channel, args.limit) as client:
        if args.list_channels:
            client.list_channels()
        else:
            client.download_all_media()
