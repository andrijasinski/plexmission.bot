import pathlib
import os

AUTHORIZED_USERS = [int(uid) for uid in os.environ.get('AUTHORIZED_USERS', '').split(',')]

BOT_AUTH = os.environ.get('BOT_AUTH', '')

TRANSMISSION_AUTH = os.environ.get('TRANSMISSION_AUTH', '')

TRANSMISSION_FINISHED_FOLDER = pathlib.Path.home() / 'Content'

TRANSMISSION_IN_PROGRESS_FOLDER = TRANSMISSION_FINISHED_FOLDER / 'torrent-inprogress'

PLEX_PRESORTED_FOLDER = TRANSMISSION_FINISHED_FOLDER

PLEX_PRESORTED_IGNORE_FOLDERS = [PLEX_PRESORTED_FOLDER / 'Movies', PLEX_PRESORTED_FOLDER /
                                 'TV Shows', PLEX_PRESORTED_FOLDER / 'torrent-inprogress', PLEX_PRESORTED_FOLDER / 'transcoder-tmp']

PLEX_LIBRARY_FOLDERS = {
    'movies': PLEX_PRESORTED_FOLDER / 'Movies',
    'tvshows': PLEX_PRESORTED_FOLDER / 'TV Shows',
}
