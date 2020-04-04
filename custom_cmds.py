import telegram

from config import CUSTOM_CMDS
from utils import HandlerBaseClass, auth_command, run_shell_сommand


class CustomCmds(object):
    @staticmethod
    def get_handlers():
        for tg_cmd, v in CUSTOM_CMDS.items():
            yield CustomCmdHandler.create_custom_handler(tg_cmd, v["cmd"], v["help"])


class CustomCmdHandler(HandlerBaseClass):
    def __init__(self, tg_cmd: str, cmd: str, help_string: str) -> None:
        self.command = tg_cmd
        self.help_string = f"/{tg_cmd} - {help_string}"
        self.cmd = cmd

    @classmethod
    def create_custom_handler(cls, tg_cmd: str, cmd: str, help_string: str):
        return cls(tg_cmd, cmd, help_string)

    def handle(self, update, context):
        self._handle(update, context, self.cmd)

    @staticmethod
    @auth_command
    def _handle(update, context, cmd):
        output = run_shell_сommand(cmd)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{' '.join(cmd)}` output:\n\n`{output}`",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
