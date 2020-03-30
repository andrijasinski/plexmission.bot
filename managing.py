import os
import pathlib
import shlex
import subprocess
import sys
import traceback
from enum import Enum
from functools import wraps
from threading import Thread

import telegram

from utils import (HandlerBaseClass, auth_command, default_inline_keyboard,
                   non_auth_command, run_shell_сommand)


class HelpHandler(HandlerBaseClass):

    command = 'help'
    lines = [f"/{command} - list available commands"]

    def add_line(self, line):
        self.lines.append(line)

    def handle(self, update, context):
        self._handle(update, context, '\n\n'.join(self.lines))

    @staticmethod
    @non_auth_command
    def _handle(update, context, lines):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Available commands:\n{lines}',
            parse_mode=telegram.ParseMode.MARKDOWN
        )


class UpdateHandler(HandlerBaseClass):

    command = 'update'
    help_string = f"/{command} - pull changes from Github"

    @staticmethod
    @auth_command
    def handle(update, context):
        cmd = ['git', 'pull', 'origin', 'master']
        output = run_shell_сommand(cmd)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{' '.join(cmd)}` output:\n\n`{output}`",
            parse_mode=telegram.ParseMode.MARKDOWN
        )


class RunCmdHandler(HandlerBaseClass):

    command = 'run'
    help_string = f"/{command} <args> - run shell command (ex. `/run df -h`)"

    @staticmethod
    @auth_command
    def handle(update, context):
        cmd = shlex.split(' '.join(context.args))
        output = run_shell_сommand(cmd)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{' '.join(cmd)}` output:\n\n`{output}`",
            parse_mode=telegram.ParseMode.MARKDOWN
        )


class StartHandler(HandlerBaseClass):

    command = 'start'
    help_string = f"/{command} - run to get your user ID"

    @staticmethod
    @non_auth_command
    def handle(update, context):
        user_id = update.effective_user.id
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Your User ID --- `{user_id}`",
            reply_markup=default_inline_keyboard(),
            parse_mode=telegram.ParseMode.MARKDOWN)


class RestartHandler(HandlerBaseClass):

    def __init__(self, updater):
        self.command = 'restart'
        self.help_string = f"/{self.command} - restart bot"
        self.updater = updater

    def handle(self, update, context):
        self._handle(update, context, self.updater)

    @staticmethod
    @auth_command
    def _handle(update, context, updater):
        def stop_and_restart():
            updater.stop()
            os.execl(sys.executable, sys.executable, *sys.argv)
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()


COMMAND_HANDLERS = [StartHandler, UpdateHandler, RunCmdHandler]


class Emojis(Enum):
    FILM_CAMERA = "📽"
    FOLDER = "🗂"
    OK_HAND = "👌"
    HORNS = "🤘"
    THUMB_UP = "👍"
    DOG = "🐶"
