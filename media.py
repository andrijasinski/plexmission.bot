import pathlib
from functools import reduce

import telegram

from config import (
    PLEX_LIBRARY_FOLDERS,
    PLEX_PRESORTED_FOLDER,
    PLEX_PRESORTED_IGNORE_FOLDERS,
)
from managing import Emojis
from utils import HandlerBaseClass, auth_command, get_inline_button, glob_dir


class MediaListHandler(HandlerBaseClass):

    command = "mediaList"
    help_string = f"/{command} - list contents of the `{PLEX_PRESORTED_FOLDER}` folder"

    @staticmethod
    @auth_command
    def handle(update, context):
        button_list = [
            get_inline_button(p, Emojis.FOLDER if p.is_dir() else Emojis.FILM_CAMERA)
            for p in glob_dir(PLEX_PRESORTED_FOLDER, PLEX_PRESORTED_IGNORE_FOLDERS)
        ]
        if not button_list:
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"`{PLEX_PRESORTED_FOLDER}` is empty {Emojis.OK_HAND.value}",
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
        reply_markup = telegram.InlineKeyboardMarkup(button_list)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{Emojis.THUMB_UP.value} Files and folders in `{PLEX_PRESORTED_FOLDER}`:",
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )


class MoveFileToFolderCallbackHandler(HandlerBaseClass):

    pattern = r"content_list_.+"

    @staticmethod
    @auth_command
    def handle(update, context):
        file = context.matches[0].group(0).split("content_list_")[1]
        button_list = []
        for k, v in PLEX_LIBRARY_FOLDERS.items():
            button_list.append(
                [
                    telegram.InlineKeyboardButton(
                        f'Move to "{v.name if type(v) == pathlib.PosixPath else v}"',
                        callback_data=f"{k}_{file}",
                    )
                ]
            )
        reply_markup = telegram.InlineKeyboardMarkup(button_list)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Move `{file[:10]}...` to:",
            reply_markup=reply_markup,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )


class MoveFileToFolderCallbackCallbackHandler(HandlerBaseClass):

    pattern = reduce(lambda acc, k: f"{acc}{k}_.+|", PLEX_LIBRARY_FOLDERS.keys(), "")[
        :-1
    ]

    @staticmethod
    @auth_command
    def handle(update, context):
        match = context.matches[0].group(0)
        file, folder = "", ""
        for k, v in PLEX_LIBRARY_FOLDERS.items():
            if match.startswith(k):
                file = match.split(f"{k}_")[1]
                folder = v
        if not (file and folder):
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Unsupported prefix for file `{match}`",
                parse_mode=telegram.ParseMode.MARKDOWN,
            )

        for f in PLEX_PRESORTED_FOLDER.glob("*"):
            if f.name.startswith(file):
                f.replace(PLEX_PRESORTED_FOLDER / folder / f.name)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"`{f.name}` is moved to {folder} {Emojis.OK_HAND.value}",
                    parse_mode=telegram.ParseMode.MARKDOWN,
                )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"No file with this prefix: `{file}`",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )


COMMAND_HANDLERS = [MediaListHandler]
CALLBACKS = [MoveFileToFolderCallbackHandler, MoveFileToFolderCallbackCallbackHandler]
