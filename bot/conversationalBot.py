import logging
from flask import Flask,request
from telegram.ext import Dispatcher, MessageHandler,CommandHandler,Filters
from telegram import Bot, Update, ReplyKeyboardMarkup
import utils

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',level = logging.INFO)
logger = logging.getLogger(__name__)

TOKKEN = "5379272290:AAFuyEUZmV7HALqFjjxGC2lR2_aV4OFPuBs"

app = Flask(__name__)
@app.route('/')
def index():
	return "Hello!"

@app.route(f'/{TOKKEN}',methods = ['GET','POST'])
def webhook():
	update = Update.de_json(request.get_json(),bot)
	dp.process_update(update)
	return "Ok!"

def start(update,context):
	author = update.message.from_user.first_name
	reply = "Hi! {}".format(author)
	context.bot.send_message(chat_id = update.message.chat_id,text = reply)

def _help(update, context):
	reply = "Hi this is a help text."
	context.bot.send_message(chat_id = update.message.chat_id,text = reply)

def echo_text(update, context):
	intent, reply = utils.get_reply(update.message.text,update.message.chat_id)
	if intent=="get_news":
		reply_text = utils.fetch_news(reply)
		for article in  reply_text :
			context.bot.send_message(chat_id = update.message.chat_id,text = article['link'])
	else:
		context.bot.send_message(chat_id = update.message.chat_id,text = reply)

def news (update, context):
	context.bot.send_message(chat_id = update.message.chat_id, text = "Choose one topic for news",
		reply_markup = ReplyKeyboardMarkup(keyboard = utils.topics_keyboard, one_time_keyboard = True))

def echo_sticker(update, context):
	reply = update.message.sticker.file_id
	context.bot.send_sticker(chat_id = update.message.chat_id,sticker = reply)

def error(update,context):
	logger.error("Update {} caused error {}".format(update,update.error))

if __name__ == "__main__":
	bot = Bot(TOKKEN)
	bot.set_webhook("https://b4fd-2400-80c0-1105-39c-5cc4-253c-1d9f-4364.in.ngrok.io/"+TOKKEN)
	dp = Dispatcher(bot,None)
	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help",_help))
	dp.add_handler(CommandHandler("news",news))
	dp.add_handler(MessageHandler(Filters.text,echo_text))
	dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
	dp.add_error_handler(error)
	app.run(port=8443)