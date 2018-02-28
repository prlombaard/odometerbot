#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Simple Bot to send timed Telegram messages.

# This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import datetime
import logging
import os
import sys
import time
from collections import OrderedDict

# DONE: Add colored logging
import coloredlogs
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

_BOT_VERSION_ = "Version 1.4"

_BOT_START_DATETIME_ = datetime.datetime.now()
_BOT_START_TIME_ = time.time()

_BOT_NAME_ = "Timerbot"

_SENT_MESSAGES_ = 0
_RECEIVED_MESSAGES_ = 0

_BOT_SHUTDOWN_DURATION = 3

# TODO: Add status command handler and callback to display bot status
# TODO: Add os_status command handler and callback to diplay os status in which the bot app is running


# Create a logger object.
logger = logging.getLogger(__name__)

# By default the install() function installs a handler on the root logger,
# this means that log messages from your code and log messages from the
# libraries that you use will all show up on the terminal.
coloredlogs.install(level='DEBUG')

# If you don't want to see log messages from libraries, you can pass a
# specific logger object to the install() function. In this case only log
# messages originating from that logger will show up on the terminal.
coloredlogs.install(level='DEBUG', logger=logger)

# Some examples from coloredlogs
logger.debug("this is a debugging message")
logger.info("this is an informational message")
logger.warning("this is a warning message")
logger.error("this is an error message")
logger.critical("this is a critical message")


def respawn():
    # From https://stackoverflow.com/questions/31447442/difference-between-os-execl-and-os-execv-in-python
    logger.info("Script is going to re-spawn")
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)
    logger.warning("You should not see this message")


def respawn_handler(bot, update):
    logger.info("handler:respawn_handler:start")
    respawn()
    logger.info("handler:respawn_handler:end")


def voice_handler(bot, update):
    logger.info("handler:voice_handler:start")
    logger.debug("Getting file descriptor")
    file = bot.getFile(update.message.voice.file_id)
    logger.info("file_id" + str(update.message.voice.file_id))
    filename = 'voice.ogg'
    file.download(filename)
    logger.info(f'Voice message successfully saved to disk with filename {filename}')
    logger.info("handler:voice_handler:end")


def document_handler(bot, update):
    logger.info("handler:document_handler:start")
    logger.debug("Getting file descriptor")
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file = bot.getFile(file_id)
    logger.info("file_id: " + str(file_id))
    logger.info("file_name: " + str(file_name))
    # TODO: Make a backup of this bot's code before saving (overwriting python file)
    filename = file_name
    file.download(filename)
    logger.info(f'Document successfully saved to disk with filename {filename}')

    logger.warning("new code received, re-spawning this code")
    # TODO: Check file name
    # TODO: Include some kind of password protection
    # TODO: First check that downloaded code is working before restarting the bot
    # re-spawn bot if correct file
    update.message.reply_text("Bot have received new code, re-spawning, check if I still live using /start")
    respawn()
    logger.info("handler:document_handler:end")


def shutdown_command(bot, update):
    import time
    import os
    logger.info("command:shutdown:start")
    logger.info("Received shutdown command from Telegram chat, going to try and shut down gracefully")
    update.message.reply_text("Shutdown command received")
    update.message.reply_text(f"OK, I'm shutting down in {_BOT_SHUTDOWN_DURATION} seconds")
    logger.info(f"Shutting down (killing this script in {_BOT_SHUTDOWN_DURATION} seconds")
    time.sleep(_BOT_SHUTDOWN_DURATION)
    logger.info("BYE!!")
    update.message.reply_text("BYE!!")

    os.kill(os.getpid(), 9)  # 9 means SIGKILL
    logger.info("command:shutdown:end")


def status_command(bot, update):
    logger.info("command:status:start")
    update.message.reply_text("Here is my status:")
    update.message.reply_text(f"Hi!, i'm {sys.modules[__name__]} {_BOT_VERSION_}")
    update.message.reply_text(f"I was started at absolute_time({_BOT_START_TIME_})")
    update.message.reply_text(
        f"I was started at {_BOT_START_DATETIME_}")  # DONE: Move this info to advanced status command handler
    if _SENT_MESSAGES_:
        update.message.reply_text(f"I've received {_SENT_MESSAGES_} messages")
    else:
        update.message.reply_text(f"I've received no messages")
    if _SENT_MESSAGES_:
        update.message.reply_text(f"I've sent {_RECEIVED_MESSAGES_} messages")
    else:
        update.message.reply_text(f"I've sent no messages")
    logger.info("command:status:end")


def meminfo():
    """ Return the information in /proc/meminfo
    as a dictionary """
    meminfo = OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo


def host_status_command(bot, update):
    import platform

    logger.info("command:host_status:start")
    update.message.reply_text("Here is my host status:")
    update.message.reply_text(f"platform.uname:{platform.uname()}")
    update.message.reply_text(f"platform.system:{platform.system()}")
    update.message.reply_text(f"platform.architecture(){platform.architecture()}")
    if platform.system() == 'Linux':
        logger.info("status:Linux platform")
        update.message.reply_text(f"platform.linux_distribution:{platform.linux_distribution()}")

        # Display processing units models
        with open('/proc/cpuinfo') as f:
            for line in f:
                # Ignore the blank line separating the information between
                # details about two processing units
                if line.strip():
                    if line.rstrip('\n').startswith('model name'):
                        model_name = line.rstrip('\n').split(':')[1]
                        update.message.reply_text(f"{model_name}")
        memory_info = meminfo()
        update.message.reply_text(f"Total memory: {memory_info['MemTotal']}")
        update.message.reply_text(f"Free memory: {memory_info['MemFree']}")
    else:
        logger.info("status:Windows platform")
    logger.info("command:host_status:end")


def help_command(bot, update):
    logger.info("command:help:start")
    update.message.reply_text('Use /set <seconds> to set a timer')
    update.message.reply_text('Use /unsetall to unset all timers')
    update.message.reply_text('Use /list to list all timers. Not working, only showing last created timer')
    update.message.reply_text('Use /respawn to re-spawn the bot. ie. reload the bot''s code')
    logger.info("command:help:end")


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_command(bot, update):
    logger.info("command:start")
    update.message.reply_text(f"Hi!, i'm {_BOT_NAME_} {_BOT_VERSION_}")
    # DONE: Add version number
    update.message.reply_text(f"I was started at {_BOT_START_DATETIME_}")
    update.message.reply_text('Use /help to display bot commands')

    # TODO: Add other methods that the bot supports
    # TODO: Add help on how to update bot OTA via Telegram


def alarm(bot, job):
    """Send the alarm message."""
    logger.info("callback_alarm: Sending alarm message")
    bot.send_message(job.context, text='Beep!')


def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    logger.info("command:set_timer")
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        logger.debug(f"Add job to que, setting due time to {due} seconds")
        job = job_queue.run_once(alarm, due, context=chat_id, name=f'job_{due}_seconds_from_now')
        logger.debug("Job added to queue")
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text("No value specidfed after /set")
        update.message.reply_text("Setting timer to default 60s seconds")
        # Calling recursively this same method but this time with a valid args[0] value
        set_timer(bot, update, [60], job_queue, chat_data)


def unsetall(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    logger.info("command:unsetall")
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def list_timers(bot, update, chat_data):
    """List all jobs on the queue"""
    logger.info("command:list_timers")
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timers')
        return

    job = chat_data['job']
    logger.debug(type(job))
    logger.debug(job)
    logger.debug(dir(job))
    logger.debug(job.interval_seconds)
    logger.debug(job.interval)
    logger.debug(job.name)
    update.message.reply_text('Timers')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    logger.info("Setting up Telegram bot")
    logger.info(f'Bot started at datetime({_BOT_START_DATETIME_})')
    logger.info(f'Bot started at absolute time({_BOT_START_TIME_})')
    import sys
    if len(sys.argv) == 1:
        raise EnvironmentError("Telegram Authentication Token not found in environment variable argv[1]")

    updater = Updater(sys.argv[1])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    logger.info("Adding command handlers")
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("status", status_command))
    dp.add_handler(CommandHandler("shutdown", shutdown_command))
    dp.add_handler(CommandHandler("host_status", host_status_command))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unsetall", unsetall, pass_chat_data=True))
    dp.add_handler(CommandHandler("list", list_timers, pass_chat_data=True))
    dp.add_handler(CommandHandler("respawn", respawn_handler, pass_chat_data=False))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    dp.add_handler(MessageHandler(Filters.document, document_handler))

    # log all errors
    dp.add_error_handler(error)

    logger.info("Starting the Bot")
    logger.info(
        f"This is {_BOT_VERSION_}")  # DONE: Add version number from this module, DO NOT hardcode into strings!!!
    logger.info("This bot can be updated OTA with Telegram")

    # Start the Bot
    logger.debug("Bot is starting to poll for messages")
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

    logger.info("Exiting script, this message should only be seen when shutting down script")


if __name__ == '__main__':
    main()
