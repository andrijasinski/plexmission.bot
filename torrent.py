import logging
import re
import tempfile

import telegram

from config import TRANSMISSION_AUTH
from managing import Emojis
from utils import HandlerBaseClass, auth_command, run_shell_сommand
from dog import send_dog

TRANSMISSION_BASE_CMD = ['transmission-remote', '-n', TRANSMISSION_AUTH]


class TorrentListHandler(HandlerBaseClass):

    command = 'torrentList'
    help_string = f"/{command} - list currently added torrents"

    @staticmethod
    @auth_command
    def handle(update, context):
        button_list = inline_list_of_torrents()

        button_list.append([telegram.InlineKeyboardButton(
            "RELOAD", callback_data=f"torrent_reload")])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{Emojis.OK_HAND.value} list of torrents:",
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=telegram.InlineKeyboardMarkup(button_list),
        )


class TorrentAddFileHandler(HandlerBaseClass):

    filters = telegram.ext.Filters.document

    @staticmethod
    @auth_command
    def handle(update, context):
        with tempfile.NamedTemporaryFile() as tf:
            f = update.effective_message.document.get_file().download(
                custom_path=f'{tf.name}')

            cmd = TRANSMISSION_BASE_CMD + ['-a', f]
            run_shell_сommand(cmd)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"The `{update.effective_message.document.file_name}` torrent added! {Emojis.OK_HAND.value}",
                parse_mode=telegram.ParseMode.MARKDOWN
            )
        send_dog(update, context)


class TorrentListCallbackHandler(HandlerBaseClass):

    pattern = r'torrent_list_.+'

    @staticmethod
    @auth_command
    def handle(update, context):
        torrent_id = context.matches[0].group(0).split('torrent_list_')[1]
        cmd = TRANSMISSION_BASE_CMD + ['-t', torrent_id, '-i']
        output = run_shell_сommand(cmd)
        file_name = re.findall(r'\s*Name:\s*(.*)', output)[0]

        button_list = [
            [telegram.InlineKeyboardButton(
                'Get more info', callback_data=f"info_torrent_{torrent_id}")],
            [telegram.InlineKeyboardButton(
                'START torrent', callback_data=f"start_torrent_{torrent_id}")],
            [telegram.InlineKeyboardButton(
                'PAUSE torrent', callback_data=f"pause_torrent_{torrent_id}")],
        ]

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{Emojis.THUMB_UP.value} Select action for `{file_name}`",
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=telegram.InlineKeyboardMarkup(button_list),
        )


class InfoTorrentCallbackHandler(HandlerBaseClass):

    pattern = r'info_torrent_.+'

    @staticmethod
    @auth_command
    def handle(update, context):
        torrent_id = context.matches[0].group(0).split('info_torrent_')[1]
        cmd = TRANSMISSION_BASE_CMD + ['-t', torrent_id, '-i']
        output = run_shell_сommand(cmd)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{Emojis.OK_HAND.value} Here's the info:\n\n```{output}```\n",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        send_dog(update, context)


class PauseTorrentCallbackHandler(HandlerBaseClass):

    pattern = r'pause_torrent_.+'

    @staticmethod
    @auth_command
    def handle(update, context):
        torrent_id = context.matches[0].group(0).split('pause_torrent_')[1]
        cmd = TRANSMISSION_BASE_CMD + ['-t', torrent_id, '-S']
        run_shell_сommand(cmd)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{Emojis.OK_HAND.value} The torrent is paused",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        send_dog(update, context)


class StartTorrentCallbackHandler(HandlerBaseClass):

    pattern = r'start_torrent_.+'

    @staticmethod
    @auth_command
    def handle(update, context):
        torrent_id = context.matches[0].group(0).split('start_torrent_')[1]
        cmd = TRANSMISSION_BASE_CMD + ['-t', torrent_id, '-s']
        run_shell_сommand(cmd)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{Emojis.OK_HAND.value} The torrent is started",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        send_dog(update, context)


class TorrentListReloadCallbackHandler(HandlerBaseClass):

    pattern = r'torrent_reload'

    @staticmethod
    @auth_command
    def handle(update, context):
        button_list = inline_list_of_torrents()

        button_list.append([telegram.InlineKeyboardButton(
            "RELOAD", callback_data=f"torrent_reload")])

        try:
            context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=update.effective_message.message_id,
                text=f"{Emojis.OK_HAND.value} list of torrents:",
                parse_mode=telegram.ParseMode.MARKDOWN,
                reply_markup=telegram.InlineKeyboardMarkup(button_list),
            )
        except telegram.error.BadRequest:
            logging.warning('---- The message has not been changed.')


def inline_list_of_torrents():
    separator = '?' * 8
    cmd = TRANSMISSION_BASE_CMD + ['-l']
    output = run_shell_сommand(cmd).split('\n')
    button_list = []
    for line in output[1:]:
        line = line.strip()
        attrs = re.sub(r'\s{2,}', separator, line).split(separator)
        if not attrs or not attrs[0] or not attrs[0][0].isnumeric():
            continue
        button_text = f'{attrs[7]} | {attrs[1]} | {attrs[-1][:25]}.. |  Down {attrs[5]}'
        button_list.append([telegram.InlineKeyboardButton(
            button_text, callback_data=f"torrent_list_{attrs[0].replace('*', '')}")])
    return button_list


COMMAND_HANDLERS = [TorrentListHandler]
MESSAGE_HANDLERS = [TorrentAddFileHandler]
CALLBACKS = [TorrentListCallbackHandler, InfoTorrentCallbackHandler,
             PauseTorrentCallbackHandler, StartTorrentCallbackHandler, TorrentListReloadCallbackHandler]
