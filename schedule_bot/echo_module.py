from telegram.ext import CommandHandler


class EchoModule:

    def __init__(self, name):
        self.name = name

    def add_cmd_handlers(self, dispatcher):
        dispatcher.add_handler(CommandHandler("echo", cmd_start_echo))
        dispatcher.add_handler(CommandHandler("0echo", cmd_stop_echo))

    def cmd_start_echo(self, update, context):
        """
        Включение бота 'echo'.
        :param update: - событие получения сообщения от пользователя.
        :param context: - текущее состояние бота.
        """
        update.message.reply_text(f"Начал работу {self.name}_bot!")

    def cmd_stop_echo(self, update, context):
        """
        Выключение бота 'echo'.
        :param update: - событие получения сообщения от пользователя.
        :param context: - текущее состояние бота.
        """
        update.message.reply_text(f"{self.name}_bot прекратил работу!")

    def cmd_echo(self, update, context):
        """
        Бот 'echo'. Обработчик сообщения от пользователя.
        :param update: - событие получения сообщения от пользователя.
        :param context: - текущее состояние бота.
        """
        update.message.reply_text(update.message.text)
