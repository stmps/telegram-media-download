# Description

Download the media files from a Telegram channel (or group, or chat).

Uses the [Telethon](https://github.com/LonamiWebs/Telethon) library.

# Usage

    usage: telegram_media.py [-h] [--api-id API_ID] [--api-hash API_HASH]
                         [--list-channels] [--channel CHANNEL] [--limit LIMIT]

    Download media from a Telegram channel (or private chat).
    
    optional arguments:
      -h, --help           show this help message and exit
      --api-id API_ID      API ID
      --api-hash API_HASH  API Hash
      --list-channels      List all channel IDs
      --channel CHANNEL    Channel ID
      --limit LIMIT        Only download the last n items
      
Or, set parameters via environment variable:

    export api_id=12345678
    export api_hash=123456789abcdef
    export channel=-987654321
    export limit=100  # optional
    
Use `--list-channels` to find the ID of your group or chat:

    Group Chat Example: -100123456
    Person: 110987654
    
# Example Output

    python3 telegram_media.py
    Downloading: 20200522_172821626_AgADBSDfsDSFSDFfsdfDF2t0AAu7lwACAg_.jpg
    File already exists: 20200522_172821626_AgADBQADi6kxG-L9OFj5nf88t0AAvgygACAg_.jpg

