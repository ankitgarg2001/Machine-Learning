import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',level = logging.INFO)
logger = logging.getLogger(__name__)

TOKKEN = "5379272290:AAFuyEUZmV7HALqFjjxGC2lR2_aV4OFPuBs"

app = Flask(__name__)
@app.route('/')
def index():
	return "Hello!"

@app.route(f'/{TOKKEN}',methods=['GET','POST'])
def webhook():
	# webhook view which recieves updates from telegram
	# create update object from json-format request data
	update = Update.de_json(request.get_json(),bot)
	# process update
	dp.process_update(update)
	return "ok"

def start(update,context):
	author = update.message.from_user.first_name
	reply =  "Hi! {}".format(author)
	context.bot.send_message(chat_id = update.message.chat_id, text = reply)

def _help(update,context):
	reply = "Hi this is a help text"
	context.bot.send_message(chat_id = update.message.chat_id, text = reply)

def echo_text(update,context):
	reply  = update.message.text
	context.bot.send_message(chat_id = update.message.chat_id, text = reply)

def echo_sticker(update,context):
	reply = update.message.sticker.file_id
	context.bot.send_sticker(chat_id = update.message.chat_id, sticker = reply)

def error(update,context):
	logger.error("Update '%s' caused error '%s'",update,update.error)

if __name__=="__main__":
	bot = Bot(TOKKEN)
	bot.set_webhook("https://d83c-2400-80c0-2001-5fb-1801-9970-eca1-f56e.in.ngrok.io/"+TOKKEN)
	dp = Dispatcher(bot, None)
	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help",_help))
	dp.add_handler(MessageHandler(Filters.text,echo_text))
	dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
	dp.add_error_handler(error)
	app.run(port=8443)