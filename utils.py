import logging
import pathlib
import subprocess
import traceback
from functools import wraps
from typing import Generator, List

import telegram

from config import AUTHORIZED_USERS, DEFAULT_INLINE_KEYBOARD_VALUES
from db import DB


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in AUTHORIZED_USERS:
            logging.info("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def log_user(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        logging.info(
            f"{update.effective_message.text} requested by {update.effective_user}"
        )
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        if chat_id:
            DB.update_user_and_chat_id(user_id, chat_id)
        return func(update, context, *args, **kwargs)

    return wrapped


def report_fail(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        try:
            return func(update, context, *args, **kwargs)
        except subprocess.CalledProcessError as e:
            tb = traceback.format_exc()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Running `{update.effective_message.text}` failed:\n\nStacktrace:\n```{tb}```\n\nSTDERR:\n```{e.stderr}```\n\nSTDOUT:\n```{e.stdout}```",  # noqa: E501
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
        except Exception:
            tb = traceback.format_exc()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Running `{update.effective_message.text}` failed:\n\n```{tb}```",
                parse_mode=telegram.ParseMode.MARKDOWN,
            )

    return wrapped


def auth_command(func):
    @restricted
    @log_user
    @report_fail
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        return func(update, context, *args, **kwargs)

    return wrapped


def non_auth_command(func):
    @log_user
    @report_fail
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        return func(update, context, *args, **kwargs)

    return wrapped


def run_shell_сommand(cmd) -> str:
    return subprocess.run(
        cmd, capture_output=True, check=True, text=True, timeout=10
    ).stdout


def get_inline_button(
    file: pathlib.Path, emoji, char_limit=10
) -> List[telegram.InlineKeyboardButton]:
    try:
        return [
            telegram.InlineKeyboardButton(
                f"{emoji.value} {file.name}",
                callback_data=f"content_list_{file.name[:char_limit]}",
            )
        ]
    except telegram.error.BadRequest:
        return get_inline_button(file, emoji, char_limit=char_limit - 1)


def default_inline_keyboard() -> telegram.ReplyKeyboardMarkup:
    custom_keyboard = [
        [
            telegram.InlineKeyboardButton(
                text=keyboard["text"], url=keyboard["callback"]
            )
            for keyboard in DEFAULT_INLINE_KEYBOARD_VALUES
        ]
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    return reply_markup


def glob_dir(
    path: pathlib.Path, ignore: List[pathlib.Path]
) -> Generator[pathlib.Path, None, None]:
    for path in path.glob("*"):
        if path not in ignore:
            yield path


class HandlerBaseClass(object):

    command = ""
    help_string = ""
    pattern = ""
    filters = None

    @staticmethod
    def handle(update, context):
        pass
