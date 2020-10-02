# Подключение модулей и библиотек сторонних.
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Подключение модулей и библиотек текущего проекта
from .log import logger
from .config import Config

# region Data
current_bot: str = ''

# Словарь ботов, которые работают с текстовыми входными данными.
# 'Название бота': флажок, указывающий включен бот или нет.
bots = {
    'echo': False,
    'invert_echo': False,
    'class_timetable': False
}
day_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
help_info = '/start - начало беседы нового пользователя с ботом\n' \
            '/help - вывод списка команд с описаниями\n' \
            '/bots - вывод списка ботов с описаниями\n' \
            '/echo - включение бота (echo)\n' \
            '/0echo - выключение бота (echo)\n' \
            '/invert_echo - включение бота (invert_echo)\n' \
            '/0invert_echo - выключение бота (invert_echo)\n' \
            '/class_timetable - включение бота (class_timetable)\n' \
            '/0class_timetable - выключение бота (class_timetable)\n'\
            '/ct_days - вывод дней недели (class_timetable)\n'
bots_info = '/echo - выводит введеное пользователем сообщение\n' \
            '/invert_echo - выводит введенное пользователем сообщение в обратном порядке\n' \
            '/class_timetable - вывод расписания занятий\n'
# endregion


# region Commands
def cmd_start_bot(bot_name, update, context):
    global bots
    global current_bot
    if current_bot != bot_name:
        if current_bot != '':
            bots[current_bot] = False
        bots[bot_name] = True
        current_bot = bot_name
        update.message.reply_text(f"Начал работу {bot_name}_bot!")


def cmd_stop_bot(bot_name, update, context):
    global current_bot
    global bots
    if current_bot == bot_name:
        bots[current_bot] = False
        current_bot = ''
        update.message.reply_text(f"Прекратил работу {bot_name}_bot!")


def cmd_start(update, context):
    """
    Команда для бота: начало общения.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    update.message.reply_text(f"Привет, {update.message.chat.username}! Ты начал со мной общение!")


def cmd_help(update, context):
    """
    Команда для бота: вывод списка всех команд с описаниями.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    update.message.reply_text(str(help_info))


def cmd_bots(update, context):
    """
    Команда для бота: вывод списка ботов с описаниями.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    update.message.reply_text(str(bots_info))


def cmd_msg_handlers_manager(update, context):
    """
    Менеджер обработчиков текстовых сообщений. Передает полученное сообщение обработчику текущего бота.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    if bots['invert_echo']:
        cmd_invert_echo(update, context)
    elif bots['class_timetable']:
        pass
    elif bots['echo']:
        cmd_echo(update, context)


# region Bot Invert Echo
def cmd_start_invert_echo(update, context):
    """
    Включение бота 'invert_echo'.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    cmd_start_bot('invert_echo', update, context)


def cmd_stop_invert_echo(update, context):
    """
    Выключение бота 'invert_echo'.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    cmd_stop_bot('invert_bot', update, context)


def cmd_invert_echo(update, context):
    """
    Бот 'invert_echo'. Обработчик сообщения от пользователя.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    update.message.reply_text(update.message.text[::-1])
# endregion


# region Bot Echo
def cmd_start_echo(update, context):
    """
    Включение бота 'echo'.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    cmd_start_bot('echo', update, context)


def cmd_stop_echo(update, context):
    """
    Выключение бота 'echo'.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    cmd_stop_bot('echo', update, context)


def cmd_echo(update, context):
    """
    Бот 'echo'. Обработчик сообщения от пользователя.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    update.message.reply_text(update.message.text)
# endregion


# region Bot Class Timetable
def cmd_start_class_timetable(update, context):
    """
    Включение бота 'class_timetable'.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    cmd_start_bot('class_timetable', update, context)


def cmd_stop_class_timetable(update, context):
    """
    Выключение бота 'class_timetable'.
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    cmd_stop_bot('class_timetable', update, context)


def cmd_timetable_days(update, context):
    """
    Бот 'class_timetable'. Вывод кнопок для выбора дня недели
    :param update: - событие получения сообщения от пользователя.
    :param context: - текущее состояние бота.
    """
    if current_bot == 'class_timetable':
        buttons = [[InlineKeyboardButton(day_of_week[0], callback_data = day_of_week[0]),
                    InlineKeyboardButton(day_of_week[1], callback_data = day_of_week[1])],
                   [InlineKeyboardButton(day_of_week[2], callback_data = day_of_week[2]),
                    InlineKeyboardButton(day_of_week[3], callback_data = day_of_week[3])],
                   [InlineKeyboardButton(day_of_week[4], callback_data = day_of_week[4]),
                    InlineKeyboardButton(day_of_week[5], callback_data = day_of_week[5])]]

        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text('Выбери день:', reply_markup = reply_markup)
# endregion
# endregion


def command_handlers_build(dispatcher):
    """
    Сборка обработчиков команд бота.
    :param dispatcher: - диспетчер обработчиков команд.
    """
    dispatcher.add_handler(CommandHandler("start", cmd_start))
    dispatcher.add_handler(CommandHandler("help", cmd_help))
    dispatcher.add_handler(CommandHandler("bots", cmd_bots))

    dispatcher.add_handler(CommandHandler("echo", cmd_start_echo))
    dispatcher.add_handler(CommandHandler("0echo", cmd_stop_echo))

    dispatcher.add_handler(CommandHandler("invert_echo", cmd_start_invert_echo))
    dispatcher.add_handler(CommandHandler("0invert_echo", cmd_stop_invert_echo))

    dispatcher.add_handler(CommandHandler("class_timetable", cmd_start_class_timetable))
    dispatcher.add_handler(CommandHandler("0class_timetable", cmd_stop_class_timetable))
    dispatcher.add_handler(CommandHandler("ct_days", cmd_timetable_days))


def message_handlers_build(dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, cmd_msg_handlers_manager))


def main():
    Config.read_opts()
    updater = Updater(token = Config.TOKEN, use_context = True)
    dp = updater.dispatcher
    command_handlers_build(dp)
    message_handlers_build(dp)

    updater.start_polling()
    updater.idle()
