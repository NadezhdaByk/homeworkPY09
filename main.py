from pickle import GLOBAL
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import random


bot = Bot(token='5355207931:AAFy1qKTwsWVihTjdBLlqgEOZgHG6daVutM')
updater = Updater(token='5355207931:AAFy1qKTwsWVihTjdBLlqgEOZgHG6daVutM')
dispatcher = updater.dispatcher


A = 0
B = 1
C = 2
D = 3
candle = 221
cand1 = 0
cand2 = 0
i=1

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Привет\nДавай поиграем:)')

    return A


def answer(update, context):
    text = update.message.text
    if 'давай' in text.lower():
        context.bot.send_message(update.effective_chat.id, 'У нас 221 конфета. Ты можешь взять не более 28 конфет.\nСколько возмешь конфет?')
    else:
        context.bot.send_message(update.effective_chat.id, 'Тогда в следующий раз')
        return ConversationHandler.END
    return B

def step_user(update, context): 
    global candle
    global cand2
    global i  
    if candle>0:       
        text = update.message.text
        if int(text)>28:
            context.bot.send_message(update.effective_chat.id, 'Ай-ай! Ты хочешь забрать слишком много конфет! Попробуй еще раз')
            return B
        else:
            candle=candle-int(text)
            context.bot.send_message(update.effective_chat.id, f'Ты взял {text} конфет. Осталось {candle}. Набери бот')
            cand2=cand2+int(text)
            i=1
            return C
    else: 
        context.bot.send_message(update.effective_chat.id, f'Игра закончена. Хочешь узнать кто выиграл?')
        return D
    

def step_bot(update, context):
    global candle
    global cand1
    global i
    if candle>0:
        cand=candle%29
        candle=candle-cand
        context.bot.send_message(update.effective_chat.id, f'Я взял {cand} конфет. Осталось {candle}. Ты сколько возьмёшь конфет? ')            
        cand1=cand1+cand
        i=0
        return B
    else: 
        context.bot.send_message(update.effective_chat.id, f'Игра закончена. Хочешь узнать кто выиграл?')
        return D

def winner(update, context):
    if i==1:
        context.bot.send_message(update.effective_chat.id,f'Поздравляем! Вы выиграли.Вам достается {cand1} моих конфет!')
    else:
        context.bot.send_message(update.effective_chat.id,f'Выиграл бот :( Ему достается {cand2} Ваших конфет!')
    return ConversationHandler.END


def cancel(update, context):
    context.bot.send_message(update.effective_chat.id, 'Прощай!!!')


start_handler = CommandHandler('start', start)
answer_handler = MessageHandler(Filters.text, answer)
step_user_handler = MessageHandler(Filters.text, step_user)
step_bot_handler = MessageHandler(Filters.text, step_bot)
winner_handler = MessageHandler(Filters.text, winner)
cancel_handler = CommandHandler('cancel', cancel)
conv_handler = ConversationHandler(entry_points=[start_handler],
                                    states={A: [answer_handler],
                                            B: [step_user_handler],
                                            C: [step_bot_handler],
                                            D: [winner_handler]},                                          
                                    fallbacks=[cancel_handler])
dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()