from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
import globals
from database import Database

database = Database("ru and uz.db")


def main_menu(update, context, lang_id):
    buttons = [
        [KeyboardButton(text=globals.btn_sell[lang_id]), KeyboardButton(text=globals.btn_buy[lang_id])],
        [KeyboardButton(text=globals.btn_setting[lang_id])],
    ]
    update.message.reply_text(text=globals.btn_use[lang_id],
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


def insert_category(update, context, categories, lang_id):
    buttons = []
    for category in categories:
        buttons.append(
            [InlineKeyboardButton(text=f"{category['title']}",
                                  callback_data=f"categories_{category['id']}")]
        )
    update.message.reply_text(text=globals.btn_sell_category[lang_id],
                              parse_mode="HTML",
                              reply_markup=InlineKeyboardMarkup(buttons))


def insert_category_product(update, context, products, chat_id, message_id, lang_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(
                text=f"{product['title']}",
                callback_data=f"categories_products_{product['title']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(products) % 2 == 1:
        buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(
            text=globals.btn_back[lang_id],
            callback_data=f"categories_back"
        )]
    )
    context.bot.edit_message_text(text=globals.btn_sell_category[lang_id],
                                  parse_mode="HTML",
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(buttons))


def insert_category_product_buy(update, context, products, chat_id, message_id, lang_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(
                text=f"{product['title']}",
                callback_data=f"category_product_{product['title']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(products) % 2 == 1:
        buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(
            text=globals.btn_back[lang_id],
            callback_data=f"category_back"
        )]
    )
    context.bot.edit_message_text(text=globals.btn_sell_category[lang_id],
                                  parse_mode="HTML",
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(buttons))


def sell_back_to_category(update, context, categories, chat_id, message_id, lang_id):
    buttons = []
    for category in categories:
        buttons.append(

            [InlineKeyboardButton(text=f"{category['title']}",
                                  callback_data=f"categories_{category['id']}")]
        )
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=globals.btn_sell_category[lang_id],
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def get_info_category(update, context, categories, lang_id):
    buttons = []
    for category in categories:
        buttons.append(

            [InlineKeyboardButton(text=f"{category['title']}",
                                  callback_data=f"category_{category['id']}")]

        )
    update.message.reply_text(text=globals.btn_sell_category[lang_id],
                              parse_mode="HTML",
                              reply_markup=InlineKeyboardMarkup(buttons))


def get_info_category_buy(update, context, categories, lang_id):
    buttons = []
    for category in categories:
        buttons.append(

            [InlineKeyboardButton(text=f"{category['title']}",
                                  callback_data=f"category_{category['id']}")]

        )
    update.message.reply_text(text=globals.btn_buy_category[lang_id],
                              parse_mode="HTML",
                              reply_markup=InlineKeyboardMarkup(buttons))


def back_to_category(update, context, categories, chat_id, message_id, lang_id):
    buttons = []
    for category in categories:
        buttons.append(

            [InlineKeyboardButton(text=f"{category['title']}",
                                  callback_data=f"category_{category['id']}")]
        )
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=globals.btn_tan[lang_id],
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def back_to_category_product(update, context, products, chat_id, message_id, lang_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(
                text=f"{product['title']}",
                callback_data=f"category_product_{product['title']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(products) % 2 == 1:
        buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(
            text=globals.btn_back[lang_id],
            callback_data=f"category_back"
        )]
    )
    context.bot.edit_message_text(text=globals.btn_tan[lang_id],
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(buttons))


def category_product(update, context, products, chat_id, message_id, lang_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(
                text=f"{product['title']}",
                callback_data=f"category_product_{product['id']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(products) % 2 == 1:
        buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(
            text=globals.btn_back[lang_id],
            callback_data=f"category_back"
        )]
    )
    context.bot.edit_message_text(text=globals.btn_tan[lang_id],
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(buttons))


def sell_end(update, context, lang_id):
    buttons = [
        [KeyboardButton(text=globals.btn_sell[lang_id]), KeyboardButton(text=globals.btn_buy[lang_id])],
        [KeyboardButton(text=globals.btn_setting[lang_id])],
    ]
    update.message.reply_text(
        text=globals.btn_thank[lang_id],
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def send_info(update, context, infos, message_id, data, chat_id, lang_id):
    if infos:
        text = ""
        count = 1
        for info in infos:
            count += 1
            btn_chek = {
                1: f"<b>✅✅✅\n{count}. {info['title']}\nNarxi: {info['price']} so'm\nMassasi : {info['tons']} tonna\nShahar: {info['city']}\nSotuvchi: {info['customer']}\n☎: {info['contact']}</b>\n\n",
                2: f"<b>✅✅✅\n{count}. {info['title']}\nЦена: {info['price']} сумма\nМасса : {info['tons']} тонны\nГород: {info['city']}\nПродавец: {info['customer']}\n☎: {info['contact']}</b>\n\n"
            }
            text += btn_chek[lang_id]

        buttons = [
            [InlineKeyboardButton(text=globals.btn_back[lang_id],
                                  callback_data=f"category_product_back_{data}")]
        ]
        context.bot.edit_message_text(text=text,
                                      parse_mode="HTML",
                                      chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=InlineKeyboardMarkup(buttons))
    else:
        buttons = [
            [InlineKeyboardButton(text=globals.btn_back[lang_id],
                                  callback_data=f"category_product_back_{data}")]
        ]
        context.bot.edit_message_text(text=globals.btn_no[lang_id],
                                      chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=InlineKeyboardMarkup(buttons))


def get_lang(update, context, lang_id):
    buttons = [
        [KeyboardButton(text="🇺🇿 O'zbek tili"), KeyboardButton(text="🇷🇺 Rus tili")]
    ]
    update.message.reply_text(
        text=globals.btn_ch_lan[lang_id],
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
