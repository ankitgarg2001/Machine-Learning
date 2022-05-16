import logging
from telegram.ext import Updater,CommandHandler, MessageHandler,Filters

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',level = logging.INFO)
logger = logging.getLogger(__name__)

TOKKEN = "5379272290:AAFuyEUZmV7HALqFjjxGC2lR2_aV4OFPuBs"

def start(update, context):
	print(update)
	author = update.message.from_user.first_name
	reply = "Hi! {}".format(author)
	context.bot.send_message(chat_id = update.message.chat_id, text = reply)

def _help(update, context):
	help_txt = "Hey ! This is the help text."
	context.bot.send_message(chat_id = update.message.chat_id, text = help_txt)		

def echo_text(update, context):
	reply = update.message.text
	context.bot.send_message(chat_id = update.message.chat_id,text = reply)

def echo_sticker(update, context):
	reply = update.message.sticker.file_id  
	context.bot.send_sticker(chat_id = update.message.chat_id,sticker = reply)

def error(update, context):
	logger.error("Update '%s' caused error '%s'",update,update.error)

def main():
	updater = Updater(TOKKEN,use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help",_help))
	dp.add_handler(MessageHandler(Filters.text,echo_text))
	dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__=="__main__":
	main()