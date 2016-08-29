#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Telegram bot and Blynk for easy managing your IoT
# based on telegram-bot-api and blynkapi libs
#

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from blynkapi import Blynk
import logging

# Vars 
# your telegram bot token id
tokenid = '251sdbrmvorfiojoeirjgoejfwcwlclrlGxAqQUpnc'

# Blynk projects id
my_project = "fe4ab7fe7aawfd3qffervw45t2sdferrf34e"
my_project2 = "sbvhcaci34hwch8qghdhp8csdnci0jvhd39s"

# create a blynk objects with you want to work
k_amp_power = Blynk(my_project, pin = "V3")
k_light = Blynk(my_project, pin = "V4")
k_amp_src = Blynk(my_project2, pin = "V2")

# begin of program
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

def start(bot, update):
	"""Base menu with all available commands"""
	bot.sendMessage(chat_id=update.message.chat_id, text="""
		I'm a bot, please talk to me!
		You can:

		/amplifier	turn On/Off amp on kitchen
		/light 		turn On/Off light on kitchen
		/source		kitchen amp source 3,5/Bluetooth """)

def stat_conv(res):
	"""Conver value from 1-0 to on-off"""
	if res[0] == "0":
		return "off"
	elif res[0] == "1":
		return "on"
	else:
		return "unknown" 

def answers(bot, update, objectx, desc, action):
	"""Function for generating """
	if action == "on":
		res = objectx.on()
		next_state = "off"
	elif action == "off":
		res = objectx.off()
		next_state = "on"
	else:
		return "Err"
	bot.answerCallbackQuery(
		callback_query_id=update.callback_query.id, 
		text="Turning "+str(action)+" "+str(desc)+"! " + res)
	bot.editMessageText(
		chat_id=update.callback_query.message.chat.id, 
		message_id=update.callback_query.message.message_id, 
		text="The "+str(desc)+" is "+str(stat_conv(objectx.get_val()))+". Do you want to turn it "+ next_state)
	bot.editMessageReplyMarkup(
		chat_id=update.callback_query.message.chat.id, 
		message_id=update.callback_query.message.message_id, 
		reply_markup=telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(next_state, callback_data="k_"+str(desc)+"_"+next_state)]]))

def inl(bot, update):
	"""Inline answers handler"""
	if update.callback_query.data == "k_amp_on":
		answers(bot, update, k_amp_power, "amp", "on")

	elif update.callback_query.data == "k_amp_off":
		answers(bot, update, k_amp_power, "amp", "off")
	
	elif update.callback_query.data == "k_light_on":
		answers(bot, update, k_light, "light", "on")

	elif update.callback_query.data == "k_light_off":
		answers(bot, update, k_light, "light", "off")

	elif update.callback_query.data == "k_src_off":
		answers(bot, update, k_amp_src, "src", "off")
		# bt = off
	elif update.callback_query.data == "k_src_on":
		answers(bot, update, k_amp_src, "src", "on")
		# 3,5 = on
	else:
		bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Else")

def echo(bot, update):
	"""Function for simply echo all text from chat"""
	bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)
	start(bot, update)

def k_amp_h(bot, update):
	# Print main menu
	start(bot, update)
	# create a inline buttons
	reply_markup = telegram.InlineKeyboardMarkup(
		[[telegram.InlineKeyboardButton(
			"On", 
			callback_data="k_amp_on"), 
		telegram.InlineKeyboardButton(
			"Off", 
			callback_data="k_amp_off")]])
	# create and sent message with inline buttons
	bot.sendMessage(
		chat_id=update.message.chat_id, 
		text="Do you want to turn On or Off amplifier? " + str(stat_conv(k_amp_power.get_val())), 
		reply_markup=reply_markup)

def k_light_h(bot, update):
	start(bot, update)
	reply_markup = telegram.InlineKeyboardMarkup(
		[[telegram.InlineKeyboardButton(
			"On", 
			callback_data="k_light_on"), 
		telegram.InlineKeyboardButton(
			"Off", 
			callback_data="k_light_off")]])
	bot.sendMessage(
		chat_id=update.message.chat_id, 
		text="Do you want to turn On or Off light? " + str(stat_conv(k_light.get_val())), 
		reply_markup=reply_markup)

def k_src_h(bot, update):
	start(bot, update)
	reply_markup = telegram.InlineKeyboardMarkup(
		[[telegram.InlineKeyboardButton(
			"3,5 jack", 
			callback_data="k_src_on"), 
		telegram.InlineKeyboardButton(
			"Bluetooth", 
			callback_data="k_src_off")]])
	bot.sendMessage(
		chat_id=update.message.chat_id, 
		text="Set input for amplifier 3,5 or bluetooth? " + str(stat_conv(k_amp_src.get_val())), 
		reply_markup=reply_markup)

def unknown(bot, update):
	"""Catch unknown commands"""
	start(bot, update)
	bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, command not found!")	

def error(bot, update, error):
	"""Errors handler"""
    logging.warning('Update "%s" caused error "%s"' % (update, error))


if __name__ == "__main__":
	# Start bot
	updater = Updater(token=tokenid)
	# Handler groups
	dispatcher = updater.dispatcher

	# Define commands
	# start
	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)
	# Kitchen amp
	k_amp_handler = CommandHandler('amplifier', k_amp_h)
	dispatcher.add_handler(k_amp_handler)
	# Kitchen light
	k_light_handler = CommandHandler('light', k_light_h)
	dispatcher.add_handler(k_light_handler)
	# Kitchen amp source
	k_src_handler = CommandHandler('source', k_src_h)
	dispatcher.add_handler(k_src_handler)

	# Handle all inline button answers
	inl_handler = CallbackQueryHandler(inl)
	dispatcher.add_handler(inl_handler)	
	
	# echo
	echo_handler = MessageHandler([Filters.text], echo)
	dispatcher.add_handler(echo_handler)
	
	# catch unknown commands
	unknown_handler = MessageHandler([Filters.command], unknown)
	dispatcher.add_handler(unknown_handler)
	
	# catch errors
	updater.dispatcher.add_error_handler(error)

	# start bot
	updater.start_polling()
	
	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()