import os
import pathlib
from typing import Dict, List

AUTHORIZED_USERS: List[int] = [int(uid) for uid in os.environ.get(
    'AUTHORIZED_USERS', '').split(',')]

BOT_AUTH: str = os.environ.get('BOT_AUTH', '')

TRANSMISSION_AUTH: str = os.environ.get('TRANSMISSION_AUTH', '')

TRANSMISSION_FINISHED_FOLDER: pathlib.Path = pathlib.Path.home() / 'Content'

TRANSMISSION_IN_PROGRESS_FOLDER: pathlib.Path = TRANSMISSION_FINISHED_FOLDER / \
    'torrent-inprogress'

PLEX_PRESORTED_FOLDER: pathlib.Path = TRANSMISSION_FINISHED_FOLDER

PLEX_PRESORTED_IGNORE_FOLDERS: List[pathlib.Path] = [PLEX_PRESORTED_FOLDER / 'Movies', PLEX_PRESORTED_FOLDER /
                                                     'TV Shows', PLEX_PRESORTED_FOLDER / 'torrent-inprogress', PLEX_PRESORTED_FOLDER / 'transcoder-tmp']

PLEX_LIBRARY_FOLDERS: Dict[str, pathlib.Path] = {
    'movies': PLEX_PRESORTED_FOLDER / 'Movies',
    'tvshows': PLEX_PRESORTED_FOLDER / 'TV Shows',
}

DEFAULT_INLINE_KEYBOARD_VALUES: List[str] = [
    '/help', '/mediaList', '/torrentList']
