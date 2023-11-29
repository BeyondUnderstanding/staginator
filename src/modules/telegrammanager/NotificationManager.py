from telebot import TeleBot

class NotificationManager:
    def __init__(self, bot: TeleBot, chat_id: int, thread_id: int):
        self.bot: TeleBot = bot
        self.chat_id = chat_id
        self.thread_id = thread_id

    def stage_created(self, stage, url, port_1, port_2):
        payload_text = "<b>Stage created -> {0}</b>\n" \
                        "<b>Ports: </b><i>{1} -> {2}</i>\n" \
                        "<a href='{3}'><b>Stage link</b></a>"
        self.bot.send_message(
            chat_id=self.chat_id,
            message_thread_id=self.thread_id,
            parse_mode='HTML',
            text=payload_text.format(stage, port_1, port_2, url)
        )

    def stage_delete(self, stage: str, url: str):
        payload_text = "<b>Stage deleted -> {0}</b>\n" \
                        "<a href='{1}'><b>Stage link</b></a>"
        self.bot.send_message(
            chat_id=self.chat_id,
            message_thread_id=self.thread_id,
            parse_mode='HTML',
            text=payload_text.format(stage, url)
        )

    def stage_rebuild_start(self, stage):
        payload_text = "<b>Stage rebuild started -> {0}</b>"
        self.bot.send_message(
            chat_id=self.chat_id,
            message_thread_id=self.thread_id,
            parse_mode='HTML',
            text=payload_text.format(stage)
        )

    def stage_build_finished(self, stage, url):
        payload_text = "<b>Stage build complete -> {0}</b>\n" \
                        "<a href='{1}'><b>Stage link</b></a>"
        self.bot.send_message(
            chat_id=self.chat_id,
            message_thread_id=self.thread_id,
            parse_mode='HTML',
            text=payload_text.format(stage, url)
        )

    def stage_build_failed(self, stage, message):
        payload_text = "<b>Stage build failed -> {0}</b>\n" \
                       "<b>{1}</b>"
        self.bot.send_message(
            chat_id=self.chat_id,
            message_thread_id=self.thread_id,
            parse_mode='HTML',
            text=payload_text.format(stage, message)
        )
