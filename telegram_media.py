import argparse
import os

from telethon import types
from telethon.sync import TelegramClient


def main():
    args = get_args()

    # use env vars if they're provided, otherwise use command-line args
    api_id = os.environ.get('api-id', args.api_id)
    api_hash = os.environ.get('api-hash', args.api_hash)
    channel = int(os.environ.get('channel', args.channel))
    limit = int(os.environ.get('limit', args.limit))

    with TelegramClient('session_name', api_id, api_hash) as client:

        if args.list_channels:
            list_channel_ids(client)
        else:
            # Refer to the documentation for other filter types.
            # https://tl.telethon.dev/types/messages_filter.html
            message_filter = types.InputMessagesFilterPhotoVideo

            for message in client.iter_messages(channel, limit=limit, filter=message_filter):
                # You lose the original filename when you share a file in a Telegram chat.
                # So we construct a new, and hopefully unique, filename.
                # TODO use inbuilt path module
                filename = '_'.join([
                    message.date.strftime("%Y%m%d"),
                    str(message.chat_id),
                    message.file.id,
                    message.file.ext
                ])

                if os.path.isfile(filename):
                    print(f'File already exists: {filename}')
                else:
                    print(f'Downloading: {filename}')
                    path = message.download_media(file=filename)


def get_args():
    parser = argparse.ArgumentParser(description='Download media from a Telegram channel (or private chat).')
    parser.add_argument("--api-id", help="API ID")
    parser.add_argument("--api-hash", help="API Hash")
    parser.add_argument("--list-channels", help="List all channel IDs", action="store_true")
    parser.add_argument("--channel", help="Channel ID")
    parser.add_argument("--limit", help="Only download the last n items", default=0)
    return parser.parse_args()


def list_channel_ids(client):
    for dialog in client.iter_dialogs():
        print(f'{dialog.name}: {dialog.id}')


if __name__ == "__main__":
    main()
