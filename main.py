import logging
import os

from telegram.ext import (CallbackQueryHandler, CommandHandler, MessageHandler,
                          Updater)

import managing
import media
import torrent
from config import BOT_AUTH
from custom_cmds import CustomCmds
from file_watcher import FileWatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    logging.info("== Starting...")
    updater = Updater(BOT_AUTH, use_context=True)
    dp = updater.dispatcher
    handlers = (
        managing.COMMAND_HANDLERS
        + torrent.COMMAND_HANDLERS
        + media.COMMAND_HANDLERS
        + [managing.RestartHandler(updater)]
    )
    callbacks = media.CALLBACKS + torrent.CALLBACKS
    message_handlers = torrent.MESSAGE_HANDLERS

    help_handler = managing.HelpHandler()
    for handler in handlers:
        dp.add_handler(CommandHandler(handler.command, handler.handle))
        help_handler.add_line(handler.help_string)
    for handler in CustomCmds.get_handlers():
        dp.add_handler(CommandHandler(handler.command, handler.handle))
        help_handler.add_line(handler.help_string)
    dp.add_handler(CommandHandler(help_handler.command, help_handler.handle))

    for callback in callbacks:
        dp.add_handler(
            CallbackQueryHandler(callback=callback.handle, pattern=callback.pattern)
        )

    for message_handler in message_handlers:
        dp.add_handler(MessageHandler(message_handler.filters, message_handler.handle))

    FileWatcher.watch(updater)

    updater.start_polling()
    logging.info("== Started!")
    if os.environ.get("GITHUB_ACTION") is not None:
        os._exit(0)
    updater.idle()


if __name__ == "__main__":
    main()
