# https://core.telegram.org/bots#
# https://pytorch.org/get-started/locally/
# pip3 install opencv-python
# pip3 install PyTelegramBotAPI==2.2.3


import telebot
from telebot import types

import config
from tg_bot.api import getPrintStatus
from tg_bot.interval import RepeatedTimer, BotStatus

bot = telebot.TeleBot(config.TOKEN)
botStatus = BotStatus()
trackStatus = False


def checkStatus(chatId):
  try:
    data = getPrintStatus()
    bot.send_photo(chatId, photo=data['image'], caption=data['status'])
    if data['status'] != 0:
      interval.stop()

    botStatus.errors = 0
  except:
    bot.send_message(chatId, 'Ошибка получения статуса!', reply_markup=getMessageMarkup(interval.is_running, True))
    botStatus.errors = botStatus.errors + 1


def track():
  if botStatus.errors > 2:
    interval.stop()
    bot.send_message(
      botStatus.lastMessage.chat.id,
      'Cлишком много ошибок. Отслеживание прекращено',
      reply_markup=getMessageMarkup(False, True))
    return

  checkStatus(botStatus.lastMessage.chat.id)


interval = RepeatedTimer(config.UPDATE_STATUS_DELAY, track)


@bot.message_handler(commands=[config.HELP, 'Помощь'])
def start_message(message):
  answerMessage = 'Бот позволит отслеживать статус печати. ' \
                  '\nНачать отслеживане: /' + config.COMMAND_START + '.' + \
                  '\nПолучить стаус /' + config.GET_STATUS + '.' + \
                  '\nПрекратить отслеживане: /' + config.COMMAND_STOP + '.' + \
                  '\nПомощь: /' + config.HELP + '.'

  bot.send_message(message.chat.id,
                   answerMessage,
                   reply_markup=getMessageMarkup())


@bot.message_handler(commands=[config.COMMAND_START])
def start_message(message):
  startTracking(message)


@bot.message_handler(commands=[config.COMMAND_STOP])
def start_message(message):
  stopTracking(message)


@bot.message_handler(commands=[config.GET_STATUS])
def start_message(message):
  checkStatus(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
  if call.data == config.COMMAND_START:
    startTracking(call.message)
  if call.data == config.COMMAND_STOP:
    stopTracking(call.message)

  bot.answer_callback_query(call.id)


def startTracking(message):
  if interval.is_running:
    bot.send_message(message.chat.id,
                     'Отслеживание уже начато',
                     reply_markup=getMessageMarkup(False, True))
    return

  bot.send_message(message.chat.id,
                   'Отслеживание началось. Для остановки введите /' + config.COMMAND_STOP,
                   reply_markup=getMessageMarkup(True, True))

  botStatus.setLastMessage(message)
  interval.start()


def stopTracking(message):
  if not interval.is_running:
    bot.send_message(message.chat.id,
                     'Отслеживание не начато',
                     reply_markup=getMessageMarkup(False, True))
    return

  bot.send_message(message.chat.id,
                   'Отслеживание прекращено. Для возобновления введите /' + config.COMMAND_START,
                   reply_markup=getMessageMarkup(False, True))

  botStatus.setLastMessage(message)
  interval.stop()


def getMessageMarkup(isStop=False, withHelp=False):
  markup = types.InlineKeyboardMarkup()

  if isStop:
    markup.row(
      types.InlineKeyboardButton('Стоп', callback_data=config.COMMAND_STOP),
      types.InlineKeyboardButton('Статус', callback_data=config.GET_STATUS))
  else:
    markup.row(
      types.InlineKeyboardButton('Старт', callback_data=config.COMMAND_START),
      types.InlineKeyboardButton('Статус', callback_data=config.GET_STATUS))

  if withHelp:
    markup.row(types.InlineKeyboardButton('Помощь', callback_data=config.HELP))

  return markup


if __name__ == '__main__':
  import time

  while True:
    try:
      bot.polling(none_stop=True)
    except Exception as e:
      time.sleep(15)
