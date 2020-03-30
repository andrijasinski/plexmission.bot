import logging
import pathlib
import threading
import time

import telegram
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from config import PLEX_PRESORTED_FOLDER, PLEX_PRESORTED_IGNORE_FOLDERS
from db import DB
from managing import Emojis
from utils import get_inline_button, glob_dir


class FileDirCreateHandler(FileSystemEventHandler):

    def __init__(self, updater):
        self._updater = updater

    def on_created(self, event: FileSystemEvent):
        p = pathlib.Path(event.src_path)
        button_list = [get_inline_button(
            p, Emojis.FOLDER if p.is_dir() else Emojis.FILM_CAMERA)]
        reply_markup = telegram.InlineKeyboardMarkup(button_list)
        for _, chat_id in DB.get_all_user_and_chat_ids():
            self._updater.bot.send_message(
                chat_id=chat_id,
                text=f'{Emojis.HORNS.value} Hey, new {"folder" if p.is_dir() else "file"} in `{PLEX_PRESORTED_FOLDER}`:',
                parse_mode=telegram.ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )


class FileWatcher(object):

    @classmethod
    def watch(cls, updater):
        subthread = threading.Thread(target=cls._watch, args=(updater,))
        logging.info('== Starting file watcher thread...')
        subthread.start()
        logging.info('== File watcher thread started!')

    @staticmethod
    def _watch(updater):
        path = PLEX_PRESORTED_FOLDER
        if not path.exists():
            logging.warning(f'==== Path {path} does not exist')
            return
        event_handler = FileDirCreateHandler(updater)
        observer = Observer()
        observer.schedule(event_handler, path=f'{path}', recursive=False)
        observer.start()

        logging.info(f'==== Listening to changes in {path}')
        try:
            while True:
                time.sleep(1)
        except:
            observer.stop()
        observer.join()
