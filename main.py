from telegram import (Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from database import Database
from datetime import datetime
import commands
import globals

database = Database("ru and uz.db")


def check_user_data(func):
    def inner(update, context):
        chat_id = update.message.from_user.id
        user = database.get_user_by_chat_id(chat_id)
        state = context.user_data.get("state", 0)
        if state == 0 or state == 5:
            if user:
                if not user['lang_id']:
                    update.message.reply_text(
                        text=globals.text_choose_language,
                        reply_markup=ReplyKeyboardMarkup(
                            [[KeyboardButton(text=globals.btn_lang_uz), KeyboardButton(text=globals.btn_lang_ru)]],
                            resize_keyboard=True)
                    )
                    context.user_data["state"] = 1
                    return False

                elif not user['first_name']:
                    lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
                    update.message.reply_text(
                        text=globals.btn_first_name[lang_id],
                        reply_markup=ReplyKeyboardRemove()
                    )
                    context.user_data["state"] = 2
                    return False

                elif not user['last_name']:
                    lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
                    update.message.reply_text(
                        text=globals.btn_last_name[lang_id],
                        reply_markup=ReplyKeyboardRemove()
                    )
                    context.user_data["state"] = 3
                    return False

                elif not user['contact']:
                    lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
                    update.message.reply_text(
                        text=globals.btn_contact[lang_id],
                        reply_markup=ReplyKeyboardMarkup(
                            [[KeyboardButton(text=globals.btn_share_contact[lang_id], request_contact=True)]],
                            resize_keyboard=True)
                    )
                    context.user_data["state"] = 4
                    return False

                else:
                    return func(update, context)

            else:
                database.create_user(chat_id, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                update.message.reply_text(
                    text=globals.text_start
                )
                update.message.reply_text(
                    text=globals.text_choose_language,
                    reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text=globals.btn_lang_uz),
                                                       KeyboardButton(text=globals.btn_lang_ru)]],
                                                     resize_keyboard=True)
                )
                context.user_data["state"] = 1
                return False

        else:
            return func(update, context)

    return inner


def check_user_state(update, context):
    chat_id = update.message.from_user.id
    user = database.get_user_by_chat_id(chat_id)
    if user:
        if not user['lang_id']:
            update.message.reply_text(
                text=globals.text_choose_language,
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton(text=globals.btn_lang_uz), KeyboardButton(text=globals.btn_lang_ru)]],
                    resize_keyboard=True)
            )
            context.user_data["state"] = 1

        elif not user['first_name']:
            lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
            update.message.reply_text(
                text=globals.btn_first_name[lang_id],
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data["state"] = 2

        elif not user['last_name']:
            lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
            update.message.reply_text(
                text=globals.btn_last_name[lang_id],
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data["state"] = 3

        elif not user['contact']:
            lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
            update.message.reply_text(
                text=globals.btn_contact[lang_id],
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton(text=globals.btn_share_contact[lang_id], request_contact=True)]],
                    resize_keyboard=True)
            )
            context.user_data["state"] = 4

        else:
            context.user_data["state"] = 5
            commands.main_menu(update, context, user['lang_id'])
    else:
        database.create_user(chat_id, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        update.message.reply_text(
            text=globals.text_start
        )
        update.message.reply_text(
            text=globals.text_choose_language,
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text=globals.btn_lang_uz), KeyboardButton(text=globals.btn_lang_ru)]],
                resize_keyboard=True)
        )
        context.user_data["state"] = 1


def check_product(update, context, info):
    chat_id = update.message.from_user.id
    user = database.get_user_by_chat_id(chat_id)
    lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
    if info:
        if not info['tons']:
            update.message.reply_text(text=globals.btn_tons[lang_id],
                                      parse_mode="HTML")
            return 7

        elif not info['city']:
            update.message.reply_text(text=globals.btn_city[lang_id],
                                      parse_mode="HTML")
            return 8

        elif not info['customer']:
            update.message.reply_text(text=globals.btn_full[lang_id],
                                      parse_mode="HTML")
            return 9

        elif not info['contact']:
            buttons = [
                [KeyboardButton(globals.btn_share_contact[lang_id], request_contact=True)]
            ]
            update.message.reply_text(text=globals.btn_contact[lang_id],
                                      reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
            return 10
        else:
            commands.sell_end(update, context, user['lang_id'])

    else:
        pass


@check_user_data
def start_command(update, context):
    chat_id = update.message.from_user.id
    user = database.get_user_by_chat_id(chat_id)
    commands.main_menu(update, context, user['lang_id'])


@check_user_data
def message_handler(update, context):
    msg = update.message.text
    chat_id = update.message.from_user.id
    lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
    user = database.get_user_by_chat_id(chat_id)
    state = context.user_data.get("state", 0)

    if state == 1:
        if msg == globals.btn_lang_uz:
            database.update_user(state, chat_id, 1)
            check_user_state(update, context)

        elif msg == globals.btn_lang_ru:
            database.update_user(state, chat_id, 2)
            check_user_state(update, context)

        else:
            pass

    elif state == 2:
        database.update_user(state, chat_id, msg)
        check_user_state(update, context)

    elif state == 3:
        database.update_user(state, chat_id, msg)
        check_user_state(update, context)

    elif state == 4:
        database.update_user(state, chat_id, msg)
        check_user_state(update, context)

    elif state == 6 and (msg != globals.btn_buy[lang_id] and msg != globals.btn_sell[lang_id] and msg != globals.btn_setting[lang_id]):
        info_id = context.user_data.get("info_id", 0)
        database.update_info_products(state, msg, info_id, user['lang_id'])
        info = database.give_info_product(info_id, user['lang_id'])
        context.user_data['state'] = check_product(update, context, info)

    elif state == 7 and (msg != globals.btn_buy[lang_id] and msg != globals.btn_sell[lang_id] and msg != globals.btn_setting[lang_id]):
        info_id = context.user_data.get("info_id", 0)
        database.update_info_products(state, msg, info_id, user['lang_id'])
        info = database.give_info_product(info_id, user['lang_id'])
        context.user_data['state'] = check_product(update, context, info)

    elif state == 8 and (msg != globals.btn_buy[lang_id] and msg != globals.btn_sell[lang_id] and msg != globals.btn_setting[lang_id]):
        info_id = context.user_data.get("info_id", 0)
        database.update_info_products(state, msg, info_id, user['lang_id'])
        info = database.give_info_product(info_id, user['lang_id'])
        context.user_data['state'] = check_product(update, context, info)

    elif state == 9 and (msg != globals.btn_buy[lang_id] and msg != globals.btn_sell[lang_id] and msg != globals.btn_setting[lang_id]):
        info_id = context.user_data.get("info_id", 0)
        database.update_info_products(state, msg, info_id, user['lang_id'])
        info = database.give_info_product(info_id, user['lang_id'])
        context.user_data['state'] = check_product(update, context, info)

    elif state == 10 and (msg != globals.btn_buy[lang_id] and msg != globals.btn_sell[lang_id] and msg != globals.btn_setting[lang_id]):
        info_id = context.user_data.get("info_id", 0)
        database.update_info_products(state, msg, info_id, user['lang_id'])
        info = database.give_info_product(info_id, user['lang_id'])
        context.user_data['state'] = check_product(update, context, info)

    else:
        user = database.get_user_by_chat_id(chat_id)
        if msg == "🇺🇿 O'zbek tili":
            database.update_user(1, chat_id, 1)
            user = database.get_user_by_chat_id(chat_id)
            commands.main_menu(update, context, user['lang_id'])

        elif msg == "🇷🇺 Rus tili":
            database.update_user(1, chat_id, 2)
            user = database.get_user_by_chat_id(chat_id)
            commands.main_menu(update, context, user['lang_id'])

        elif msg == globals.btn_sell[lang_id]:
            categories = database.get_category(user["lang_id"])
            commands.insert_category(update, context, categories, user['lang_id'])

        elif msg == globals.btn_buy[lang_id]:
            categories = database.get_category(user["lang_id"])
            commands.get_info_category_buy(update, context, categories, user['lang_id'])

        elif msg == globals.btn_setting[lang_id]:
            commands.get_lang(update, context, user['lang_id'])


def contact_handler(update, context):
    chat_id = update.message.from_user.id
    user = database.get_user_by_chat_id(chat_id)
    contact = update.message.contact.phone_number
    state = context.user_data.get("state", 0)
    if state == 4:
        database.update_user(state, chat_id, contact)
        check_user_state(update, context)

    elif state == 10:
        info_id = context.user_data.get("info_id", 0)
        database.update_info_products(state, contact, info_id, user['lang_id'])
        info = database.give_info_product(info_id, user['lang_id'])
        context.user_data['state'] = check_product(update, context, info)


def callback_handler(update, context):
    query = update.callback_query
    data = query.data.split("_")
    chat_id = query.from_user.id
    lang_id = database.get_user_by_chat_id(chat_id)['lang_id']
    message_id = query.message.message_id
    user = database.get_user_by_chat_id(chat_id)
    if data[0] == "category":
        if data[1] == "back":
            categories = database.get_category(user['lang_id'])
            commands.back_to_category(update, context, categories, chat_id, message_id, user['lang_id'])

        elif data[1] == "product":
            if data[2] == "back":
                products = database.get_category_id_product(int(data[3]), user['lang_id'])
                commands.back_to_category_product(update, context, products, chat_id, message_id, user['lang_id'])

            else:
                info = database.get_info_product(str(data[2]), user['lang_id'])
                pk = database.get_product_id(str(data[2]), user['lang_id'])
                commands.send_info(update, context, info, message_id, pk, chat_id, user['lang_id'])

        else:
            products = database.get_category_id_product(int(data[1]), user["lang_id"])
            commands.insert_category_product_buy(update, context, products, chat_id, message_id, user['lang_id'])

    elif data[0] == "categories":
        if data[1] == "back":
            categories = database.get_category(user['lang_id'])
            commands.sell_back_to_category(update, context, categories, chat_id, message_id, user['lang_id'])

        elif data[1] == "products":
            product = database.give_product(str(data[2]), user['lang_id'])
            user_id = database.get_user_id(chat_id)
            database.update_products(user_id['id'], product['id'], product['title'], user['lang_id'])
            pk = database.get_product_id_max(user_id['id'], user['lang_id'])
            context.user_data['info_id'] = pk
            context.user_data['state'] = 6

            context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
            context.bot.send_message(
                text=globals.btn_price[lang_id],
                chat_id=chat_id,
                parse_mode="HTML"
            )

        else:

            products = database.get_category_id_product(int(data[1]), user["lang_id"])
            commands.insert_category_product(update, context, products, chat_id, message_id, user['lang_id'])


def main():
    updater = Updater("1778612834:AAFryAyhCQzouzKweXoCi1LAv1ryqYP2Td0")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
