import telebot
from config import BOT_TOKEN
from buttons import *
from database import *
import requests
import random
import string
import math
from decimal import Decimal
import jdatetime
from datetime import datetime
from bs4 import BeautifulSoup
import time
from hiddify_api import *
import os

import segno
from pathlib import Path
import re

bot = telebot.TeleBot(BOT_TOKEN)
channel_username = '@jimboo_vpn'


def check_membership(chat_id, channel_username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT deleted FROM users WHERE client_code = %s", (chat_id,))
    if cur.fetchone()[0] is False:
        member = bot.get_chat_member(channel_username, chat_id)
        if member.status == 'member' or member.status == 'creator' or member.status == 'administrator':
            return True
        else:
            bot.send_message(chat_id, f'برای استفاده از ربات، لطفا عضو کانال {channel_username} شوید.')
            bot.send_message(chat_id, 'اگر جوین شدید مجدد /start کنید')
            return False
    else:
        bot.send_message(chat_id, f'شما محدود شدید لطفا دلیل ر از پشتیبانی جویا شوید',
                         reply_markup=get_support_buttons())


###############################################################


#                   PANEL ADMIN


########################################################


def chek_admin(client_code):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT type FROM admins WHERE client_code = %s", (client_code,))
    result = cur.fetchone()
    if result:
        types = result[0]
        return types
    else:
        return False


@bot.message_handler(commands=['admin/add_admin'])
def add_admin(message):
    if chek_admin(message.chat.id) == "SUPERADMIN":

        bot.send_message(message.chat.id, 'Admin  settings menu.')
        msg = bot.send_message(message.chat.id, "client_code ra vared konid baraye ezafe kardan_admin")
        bot.register_next_step_handler(msg, add_admin_add)
    else:
        bot.send_message(message.chat.id, 'لطفا از کلید های زیر استفاده کنید')
    print(chek_admin(message.chat.id))


def add_admin_add(message):
    global admin_jadid
    admin_jadid = message.text
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE client_code = %s)", (admin_jadid,))
    if cur.fetchone():
        msg = bot.send_message(message.chat.id, "نوع ادمین رو مشخص کنید از بین AGENT , SUPERADMIN")
        bot.register_next_step_handler(msg, add_admin_type)
    else:
        bot.send_message(message.chat.id, "client_code ghalat ast")


def add_admin_type(message):
    conn = connect_db()
    cur = conn.cursor()
    type = message.text
    if type == 'AGENT' or type == 'SUPERADMIN':
        cur.execute("INSERT INTO admins (client_code, type) VALUES (%s, %s);", (admin_jadid, type))
        conn.commit()
        bot.send_message(message.chat.id, "همچیز به درستی انجام شد")

    else:
        bot.send_message(message.chat.id, "type ghalat ast")


@bot.message_handler(commands=['admin/balance'])
def handle_admin_settings(message):
    if chek_admin(message.chat.id) == "SUPERADMIN":
        bot.send_message(message.chat.id, 'Admin balance settings menu.')
        msg = bot.send_message(message.chat.id, "client_code ra vared konid baraye balance")
        bot.register_next_step_handler(msg, search_client_code_for_balance)

    else:
        bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')


def search_client_code_for_balance(message):
    balance_client_code = message.text
    wallet_id = find_user_id_from_client_code(balance_client_code)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT balance , all_buy FROM  wallets WHERE user_id = %s", (wallet_id,))
    wallet = cur.fetchone()
    if wallet:
        balance = wallet[0]
        all_buy = wallet[1]
        msg = bot.send_message(message.chat.id,
                               f'این کاربر درحال حاضر با موجودی {balance} و در کل به مقدار {all_buy} داشبورد جیمبو خودشو شارژ کرده \n اگر میخاهید بالانس شخصی رو افزایش دهید فقط عددی ک میخاهید با بالانس جمع بشود رو وارد کنید⚠')
        bot.register_next_step_handler(msg, balance_admin, wallet_id)


def balance_admin(message, wallet_id):
    balance_client2 = message.text
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE wallets SET balance = balance + %s , all_buy = all_buy + %s WHERE user_id = %s",
                (balance_client2, balance_client2, wallet_id))
    conn.commit()
    cur.execute("SELECT balance , all_buy FROM  wallets WHERE user_id = %s", (wallet_id,))
    wallet = cur.fetchone()
    if wallet:
        bbbbb = wallet[0]
        aaaaa = wallet[1]
        bot.send_message(message.chat.id,
                         f"با موفقیت انجام شد \n این کاربر درحال حاضر با موجودی {bbbbb} و در کل به مقدار {aaaaa}")


@bot.message_handler(commands=['admin/balance_decrease'])
def handle_admin_settings(message):
    if chek_admin(message.chat.id) == "SUPERADMIN":
        bot.send_message(message.chat.id, 'Admin decreasebalance settings menu.')
        msg = bot.send_message(message.chat.id, "client_code ra vared konid baraye decreasebalance")
        bot.register_next_step_handler(msg, search_client_code_for_decreasebalance)

    else:
        bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')


def search_client_code_for_decreasebalance(message):
    balance_client_code = message.text
    wallet_id = find_user_id_from_client_code(balance_client_code)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT balance , all_buy FROM  wallets WHERE user_id = %s", (wallet_id,))
    wallet = cur.fetchone()
    if wallet:
        balance = wallet[0]
        all_buy = wallet[1]
        msg = bot.send_message(message.chat.id,
                               f'این کاربر درحال حاضر با موجودی {balance} و در کل به مقدار {all_buy} داشبورد جیمبو خودشو شارژ کرده \n اگر میخاهید بالانس شخصی رو کاهش دهید فقط عددی ک میخاهید از بالانس کم  بشود رو وارد کنید⚠')
        bot.register_next_step_handler(msg, decreasebalance_admin, wallet_id)


def decreasebalance_admin(message, wallet_id):
    balance_client2 = message.text
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE wallets SET balance = balance - %s  WHERE user_id = %s",
                (balance_client2, wallet_id))

    conn.commit()
    cur.execute("SELECT balance , all_buy FROM  wallets WHERE user_id = %s", (wallet_id,))
    wallet = cur.fetchone()
    if wallet:
        bbbbb = wallet[0]
        aaaaa = wallet[1]
        bot.send_message(message.chat.id,
                         f"با موفقیت انجام شد \n این کاربر درحال حاضر با موجودی {bbbbb} و در کل به مقدار {aaaaa}")


@bot.message_handler(commands=['admin/delete'])
def handle_admin_settings(message):
    if chek_admin(message.chat.id) == "SUPERADMIN":
        bot.send_message(message.chat.id, 'Admin delete settings menu.')
        msg = bot.send_message(message.chat.id, "client_code ra vared konid baraye delete")
        bot.register_next_step_handler(msg, search_client_code_for_delete)

    else:
        bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')


def search_client_code_for_delete(message):
    deleted_client = message.text
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET deleted = TRUE WHERE client_code = %s", (deleted_client,))
    conn.commit()
    bot.send_message(message.chat.id, "کاربر شما تماما محدود شد")


@bot.message_handler(commands=['admin/undelete'])
def handle_admin_settings(message):
    if chek_admin(message.chat.id) == "SUPERADMIN":
        bot.send_message(message.chat.id, 'Admin undelete settings menu.')
        msg = bot.send_message(message.chat.id, "client_code ra vared konid baraye undelete")
        bot.register_next_step_handler(msg, search_client_code_for_undelete)

    else:
        bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')


def search_client_code_for_undelete(message):
    deleted_client = message.text
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET deleted = FALSE WHERE client_code = %s", (deleted_client,))
    conn.commit()
    bot.send_message(message.chat.id, "کاربر شما تماما رفع محدودیت شد")


@bot.message_handler(commands=['admin'])
def handle_admin_settings(message):
    if chek_admin(message.chat.id) == "SUPERADMIN":
        bot.send_message(message.chat.id, 'Admin settings menu.')
        msg = bot.send_message(message.chat.id, "client_code ra vared konid")
        bot.register_next_step_handler(msg, search_client_code)

    else:
        bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')


def search_client_code(message):
    client_searched = str(message.text)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id,join_by_code,referral_code,phone_number,email  FROM users WHERE client_code =%s",
                (client_searched,))
    user = cur.fetchone()
    user_id = user[0]

    cur.execute("SELECT balance,all_buy  FROM wallets WHERE user_id =%s",
                (user_id,))
    wallet = cur.fetchone()
    if user:
        balance = wallet[0]
        all_buy = wallet[1]
        join_by_code = user[1]
        referral_code = user[2]
        phone_number = user[3]
        email = user[4]
        user_configss = show_configs(client_searched)
        print(user_configss(client_searched))
        for mmd in user_configss:
            bot.send_message(message.chat.id, mmd)
        bot.send_message(message.chat.id,
                         f' یوزر آیدی{user_id},دعوت شده توسط {join_by_code} کد رفرال {referral_code} شماره موبایل{phone_number}و ایمیل {email} و داشبورد جیمبو این شخص در حال حاضر مقدار {balance} و در کل به مقدار {all_buy} ترون شارژ شده است')
    else:
        bot.send_message(message.chat.id, "karbar shenasaei nashod")


###############################################################


#                   PANEL AGENT


########################################################


@bot.message_handler(commands=['فروش'])
def agent(message):
    if chek_admin(message.chat.id) != False:
        msg = bot.send_message(message.chat.id,
                               "اینجا پنلی هست که همکاران ما در فروش میتونن به راحتی درامدزایی داشته باشند \n اگر تمایل دارید که اکانت روی نام کاربری شما ارسال شود و توسط شما به مشتری ارائه شود نام کاربری خود را وارد کنید \n نام کاربری شما: ----------- مونو \n  اما اگر میخواهید اکانت برای مشتری ارسال شود از مشتری خود بخواهید ربات را استارت کرده و نام کاربری مشتری را وارد کنید در اینصورت اکانت مستقیما برای مشتری ارسال خواهد شد و در هر دو حالت تخفیف ۵۰ درصدی برای شما لحاظ خواهد شد که میتوانید مبلغ اصلی را از مشتری خود دریافت نمایید.")
        bot.register_next_step_handler(msg, agent2)


def agent2(message):
    client_code_moshtari = message.text
    client_code_agent = message.chat.id
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE client_code = %s)", (client_code_moshtari,))
    if cur.fetchone():
        cur.execute("SELECT join_by_code FROM users WHERE client_code = %s", (client_code_moshtari,))
        mmd17 = cur.fetchone()[0]
        if mmd17 is None:
            cur.execute("SELECT referral_code FROM users WHERE client_code = %s", (client_code_agent,))
            referral_code = cur.fetchone()[0]
            if referral_code:
                cur.execute("UPDATE users SET join_by_code = %s WHERE client_code =%s",
                            (client_code_agent, client_code_moshtari,))
                cur.execute("UPDATE referrals SET people = people + %s WHERE client_code = %s", (1, client_code_agent))

                conn.commit()

                msg = bot.send_message(message.chat.id,
                                       "کاربر مد نظر شما با موفقیت زیر مجموعه شما شد و با هر خرید ۱۰ درصد رو شما دریافت خواهید کرد \n\n  اگر قصد خرید برای این کاربر رو دارید از پلن های موجود داخل ربات فقط عدد کانفیگ مورد  نظر رو انتخاب کنید \n 1:اکانت ۳۰ گیگ ۴۰ روزه 5.5 ترون \n 2: اکانت ۵۰ گیگ ۴۰ روزه 8.5 ترون \n 3: اکانت ۷۰ گیگ ۴۰ روزه 11 ترون \n 4: اکانت ۹۰ گیگ ۴۰ روزه 13.5 ترون \n 5: اکانت ۱۲۰ گیگ ۴۰ روزه 15.5 ترون \n \n این قیمت ها فقط برای فروشنده ها میباشد و تمام کانفیگ ها دو کاربره هستند \n \n برای ساخت اکانت اختصاصی از کامند /AGENT/EKHTESASI استفاده کنید \n لطفا فقط عدد کانفیگ مورد نظرتون رو ارسال کنید⚠ ")
                bot.register_next_step_handler(msg, takhsis_account, client_code_moshtari)



            else:
                bot.send_message(message.chat.id,
                                 "شما کد رفرال ندارید لطفا از دکمه درامد زایی کد رفرال بگیرید و سپس امتحان کنید")

        else:
            msg = bot.send_message(message.chat.id,
                                   "این کاربر قبلا  دعوت شده و نمیتوانیم زیر مجموعه شما قرارش بدیم برای خرید کانفیگ برای این کد کاربری متن را بخونید \n \n اگر قصد خرید برای این کاربر رو دارید از پلن های موجود داخل ربات فقط عدد کانفیگ مورد  نظر رو انتخاب کنید \n 1:اکانت ۳۰ گیگ ۴۰ روزه 5.5 ترون \n 2: اکانت ۵۰ گیگ ۴۰ روزه 8.5 ترون \n 3: اکانت ۷۰ گیگ ۴۰ روزه 11 ترون \n 4: اکانت ۹۰ گیگ ۴۰ روزه 13.5 ترون \n 5: اکانت ۱۲۰ گیگ ۴۰ روزه 15.5 ترون \n \n این قیمت ها فقط برای فروشنده ها میباشد و تمام کانفیگ ها دو کاربره هستند \n \n برای ساخت اکانت اختصاصی از کامند /AGENT/EKHTESASI استفاده کنید \n لطفا فقط عدد کانفیگ مورد نظرتون رو ارسال کنید⚠ ")
            bot.register_next_step_handler(msg, takhsis_account, client_code_moshtari)

    else:
        bot.send_message(message.chat.id, "این کاربر موجود نیست و دکمه استارت ربات رو نزده")


def takhsis_account(message, client_code_moshtari):
    user_id = find_user_id_from_client_code(message.chat.id)
    balance = show_user_wallet_balance(user_id)
    conf_moshtari = int(message.text)
    price = 0
    limit = 0
    if conf_moshtari == 1:
        price = Decimal("5.5")
        limit = 30
    elif conf_moshtari == 2:
        price = Decimal("8.5")
        limit = 50


    elif conf_moshtari == 3:
        price = Decimal("11")
        limit = 70

    elif conf_moshtari == 4:
        price = Decimal("13.5")
        limit = 90

    elif conf_moshtari == 5:
        price = Decimal("15.5")
        limit = 120

    else:
        bot.send_message(message.chat.id,
                         "عدد وارد شده شما خارج محدوده بود لطفا فقط عدد کانفیگ رو وارد کنید بین 1 تا 5")

    if balance >= price != 0:
        if limit != 0:

            bot.send_message(client_code_moshtari, hiddify_api_put(client_code_moshtari, 40, limit, ),
                             get_education_platform_buttons())
            buy_payment(user_id, price)
            balance -= price
            bot.send_message(message.chat.id, f"خرید شما با موفقیت انجام شد. موجودی جدید شما: {balance} ترون")

        else:
            bot.send_message(message.chat.id, "کانفیگی که انتخاب کردید نامشخص است")

    else:
        bot.send_message(message.chat.id, "داشبورد جیمبو شما موجودی کافی ندارد")


@bot.message_handler(commands=['فروش/اختصاصی'])
def admin_ehtesasi(message):
    if chek_admin(message.chat.id) != False:
        msg = bot.send_message(message.chat.id,
                               "شما درحال حاضر در صفحه ادمین هستید برای  تهیه اکانت اختصاصی برای مشتریتون نام کاربری مشتری را وارد کنید ")
        bot.register_next_step_handler(msg, agent3)


def agent3(message):
    global client_code_moshtari
    client_code_moshtari = message.text
    client_code_agent = message.chat.id
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE client_code = %s)", (client_code_moshtari,))
    if cur.fetchone():
        cur.execute("SELECT join_by_code FROM users WHERE client_code = %s", (client_code_moshtari,))
        mmd17 = cur.fetchone()[0]
        if mmd17 is None:
            cur.execute("SELECT referral_code FROM users WHERE client_code = %s", (client_code_agent,))
            referral_code = cur.fetchone()[0]
            if referral_code:
                cur.execute("UPDATE users SET join_by_code = %s WHERE client_code =%s",
                            (client_code_agent, client_code_moshtari,))
                cur.execute("UPDATE referrals SET people = people + %s WHERE client_code = %s", (1, client_code_agent))

                conn.commit()

                msg = bot.send_message(message.chat.id,
                                       "زیر مجموعه شما شد 🤩\n برای ساخت اکانت اختصاصی لازمه که اول حجم رو مشخص کنید و حداقل حجم 30 گیگ میباشد \n حجم خودتون رو وارد کنید")
                bot.register_next_step_handler(msg, account_shakhsi2)



            else:
                bot.send_message(message.chat.id,
                                 "شما کد رفرال ندارید لطفا از دکمه درامد زایی کد رفرال بگیرید و سپس امتحان کنید")

        else:
            msg = bot.send_message(message.chat.id,
                                   "قبلا اضافه شده بود \n برای ساخت اکانت اختصاصی لازمه که به فرمت زیر ارسال کنی \n (30 40 2) \n (حجم روز کاربر) \n عدد اول حجم عدد دوم تعداد روز و عدد سوم تعداد کاربر را با یک اسپیس جدا کنید")
            bot.register_next_step_handler(msg, account_shakhsi2)

    else:
        bot.send_message(message.chat.id, "این کاربر موجود نیست و دکمه استارت ربات رو نزده")


def account_shakhsi2(message):
    hagm = str(message.text)
    global num1
    global num2
    numbers_list = hagm.split()
    num1 = int(numbers_list[0])
    num2 = int(numbers_list[1])
    num3 = int(numbers_list[2])
    if num1 < 30:
        num1 = 30
    elif num1 > 1000:
        num1 = 1000
        bot.send_message(message.chat.id,
                         "عددی که برای حجم وارد کردید بیشتر از 1000 بود و برای شما 1000 در نظر گرفته شد")
    if num2 < 40:
        num2 = 40
    elif num2 > 1000:
        num2 = 1000
        bot.send_message(message.chat.id,
                         "عددی که برای روز وارد کردید بیشتر از 1000 بود و برای شما 1000 در نظر گرفته شد")
    if num3 < 2:
        num3 = 2

    mmd1 = num2 - 40
    mmd2 = num3 - 2

    su = (1300 * num1) + (700 * mmd1) + (mmd2 * 7000)
    global tron_ekhh
    ttrr77rr = su / 7000
    tron_ekhh = round(ttrr77rr, 2)  # گرد کردن به دو رقم اعشار
    bot.send_message(message.chat.id,
                     f'حجم شما {num1} و تعداد روز شما {num2} و تعداد کاربر شما {num3} در نظر گرفتید  این کانفیگ به مبلغ {tron_ekhh} ترون به شما اراعه خواهد شد\n ',
                     reply_markup=tarefe_ekhtesai_agent())


def buy_ekhtesasi_agent(call, tron_ekhh, num1, num2, client_code_moshtari):
    user_id = find_user_id_from_client_code(call.message.chat.id)
    tron = Decimal(tron_ekhh)
    if user_id is not None:
        balance = show_user_wallet_balance(user_id)
        if balance >= tron != 0:
            bot.send_message(client_code_moshtari, hiddify_api_put(client_code_moshtari, num2, num1))
            bot.send_message(client_code_moshtari,
                             f"لینک بالا برای استفاده روی سیستم عامل های Android و ios میباشد اگر فایل همین کانفیگ رو میخاهید به پشتیبانی مراجعه کنید\n نام کاربری شما:<code>{call.message.chat.id}</code> \n  روی شماره کاربریت کلیک کن و مستقیم به آیدی زیر ارسال کن. \n آیدی:@jimboovpn_Support",
                             parse_mode="HTML",
                             reply_markup=get_education_platform_buttons())
            buy_payment(user_id, tron)
            balance -= tron
            balance_pro = round(balance, 2)  # گرد کردن به دو رقم اعشار

            bot.send_message(call.message.chat.id,
                             f'عملیات تخصیص اکانت با موفقیت انجام شد داشبورد جیمبو شما درحال حاضر {balance_pro} ترون دارد ')  # بروزرسانی موجودی پس از خرید

        else:
            bot.send_message(call.message.chat.id, "شما پول کافی ندارید")


@bot.callback_query_handler(func=lambda call: call.data == "EEEE2")
def buy222222222222222222_ekhtesasi_agent(call):
    buy_ekhtesasi_agent(call, tron_ekhh, num1, num2, client_code_moshtari)


###############################################################
#
#
#
#
#
#                   PANEL          client
#
#
#
#
########################################################


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    client_code = message.from_user.id
    if check_membership(chat_id, channel_username):
        username = message.from_user.username or "NoUsername"
        save_user_and_create_wallet(client_code, username)
        reply_markup = get_main_buttons()
        bot.send_message(message.chat.id,
                         f'سلام عزیزم ❤️\nخوش اومدی به خانواده بزرگ جیمبو ✈️\nیکی از کلید های پایین رو بزن 👇 \n  \n نام کاربری شما : {chat_id}',
                         reply_markup=reply_markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if message.text == "خرید اشتراک🛍":
        if check_membership(chat_id, channel_username):
            bot.send_message(message.chat.id, "تعرفه مورد نظر خودتون رو انتخاب کنید", reply_markup=get_tariff_buttons())
    elif message.text == 'پشتیبانی👥':
        bot.send_message(message.chat.id,
                         "سعی کردیم اکثر سوالات شمارا پاسخ دهیم اما اگر همچنان به جواب سوال خود در قسمت سوالات متداول نرسیدید میتوانید با پشتیبانی ارتباط برقرار نمایید",
                         reply_markup=get_support_buttons())
    elif message.text == "داشبورد جیمبو 🖥":
        if check_membership(chat_id, channel_username):
            # فرض می‌شود تابع `find_user_id_from_client_code` ID کاربر را بر اساس chat_id بازگرداند
            user_id = find_user_id_from_client_code(message.chat.id)
            balance = show_user_wallet_balance(user_id)
            bot.send_message(message.chat.id, f" موجودی شما تو داشبورد جیمبو : {balance}  ترون",
                             reply_markup=get_wallet_recharge_buttons())
    elif message.text == "آموزش استفاده💿📖":
        bot.send_message(message.chat.id, "آموزش مد نظرتو انتخاب کن", reply_markup=get_education_buttons())

    elif message.text == "قیمت لحظه ای ترون🌐":
        if check_membership(chat_id, channel_username):
            my_string = tron_price(chat_id)
            if my_string:
                bot.send_message(chat_id, f'ترون در حال حاضر {my_string} می باشد  . ')
            else:
                pass
    elif message.text == "عودت وجه❌":
        bot.send_message(message.chat.id,
                         "برای برداشت موجودی داشبورد خود آیدی ----- خودرا برای پشتیبان ارسال نمایید ---------")
    elif message.text == "درآمدزایی⚡💵":
        if check_membership(chat_id, channel_username):
            if check_safir(chat_id):
                income_safir(chat_id)
            else:
                bot.send_message(message.chat.id,
                                 "جیمبو قراره این بار برات پول بسازه 😍  \n اگه فروشنده اکانت میتونی باشی به هر شکلی خانواده،دوستان و ... \n کافیه اینجا ثبت نام کنی تا برات یه کد تخفیف اختصاصی بسازم که باهاش هم به مخاطبات تخفیف بدی و هم از هر خرید اونها تا ابد سود به دست بیاری 😉\n نکته جالبش اینه که هرکدوم از زیر مجموعه هات مجددا کسی رو به خرید دعوت کنه تا 10 نفر زیرمجموعه بازم سودش تو جیب تو میره😱 ",
                                 reply_markup=button_validate())
    elif message.text == "ارسال ایمیل":
        msg = bot.send_message(message.chat.id, "لطفا ایمیل خودتون رو وارد کنید \n  مثال: example@gmail.com")
        bot.register_next_step_handler(msg, email)

    elif message.text == "اکانت تستی رایگان🔥":
        if check_membership(chat_id, channel_username):
            test_account(chat_id)


    elif message.text == "اشتراک های من🔋":
        user_configs = show_configs(chat_id)
        bot.send_message(chat_id, f'شما با نام کاربری: {chat_id} \n')
        if user_configs:
            for message in user_configs:
                bot.send_message(chat_id, message)
        else:
            bot.send_message(message.chat.id, "شما درحال حاضر کانفیگی ندارید")

    elif message.text == "بازگشت":
        bot.send_message(chat_id, "شما به منوی اصلی برگشتید", reply_markup=get_main_buttons())


################ ##################

#                   referral generate

#############################
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact_data = {
        'first_name': message.contact.first_name,
        'phone_number': message.contact.phone_number,
        'user_id': message.contact.user_id
    }

    json_data = json.dumps(contact_data)
    data = json.loads(json_data)

    # دسترسی به مقادیر
    first_name = data['first_name']
    phone_number = data['phone_number']
    user_id = data['user_id']
    make_refral_wallet_by_phone(user_id, first_name, phone_number)


def email(message):
    email_validate = message.text
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email_validate):
        bot.send_message(message.chat.id, "ایمیل شما با موفقیت ذخیره شد")
        make_refral_wallet_by_email(message.chat.id, email_validate)

    else:
        bot.send_message(message.chat.id, "ایمیل شما اشتباه وارد شده است")

        return False


def make_refral_wallet_by_phone(client_code, first_name, phone):
    conn = connect_db()
    cur = conn.cursor()
    # اجرای دستور UPDATE برای به‌روزرسانی مقادیر فیلد email در جدول users
    cur.execute("SELECT username FROM users WHERE client_code =%s", (client_code,))
    username = cur.fetchone()
    username = username[0]
    if username == "NoUsername":
        random_number = '{:02}'.format(random.randint(10, 999))
        # تعیین یوزرنیم‌ها
        username1 = 'jim'
        username = 'boo'
        username2 = "VPN"
    else:
        # تولید یک عدد تصادفی دو رقمی
        random_number = '{:02}'.format(random.randint(10, 99))
        # تعیین یوزرنیم‌ها
        username1 = 'jim'
        username2 = 'boo'

    # ایجاد کد تخفیف
    discount_code = f'{username1}_{username}_{username2}{random_number}'

    cur.execute("UPDATE users SET first_name = %s , phone_number = %s, referral_code = %s WHERE client_code = %s",
                (first_name, phone, discount_code, client_code))

    bot.send_message(client_code,
                     f'شروع شد قراره باهم بترکونیم🔥\n کدتخفیف اختصاصی شما: \n   <code>{discount_code}</code> \ این کد رو برای دوستات ارسال کن',
                     parse_mode='HTML')

    cur.execute("INSERT INTO discount_codes (name, percentage, owner,status) VALUES (%s, %s, %s,%s);",
                (discount_code, 10, client_code, 1))

    cur.execute("INSERT INTO referrals (client_code,people,income) VALUES (%s,%s,%s);", (client_code, 0, 0))
    # ذخیره تغییرات
    # ذخیره تغییرات
    conn.commit()

    # بستن cursor و اتصال
    cur.close()
    conn.close()


def make_refral_wallet_by_email(client_code, email_validate):
    conn = connect_db()
    cur = conn.cursor()
    # اجرای دستور UPDATE برای به‌روزرسانی مقادیر فیلد email در جدول users
    cur.execute("SELECT username FROM users WHERE client_code =%s", (client_code,))
    username = cur.fetchone()
    username = username[0]
    if username == "NoUsername":
        random_number = '{:02}'.format(random.randint(10, 999))
        # تعیین یوزرنیم‌ها
        username1 = 'jim'
        username = 'boo'
        username2 = "VPN"
    else:
        # تولید یک عدد تصادفی دو رقمی
        random_number = '{:02}'.format(random.randint(10, 99))
        # تعیین یوزرنیم‌ها
        username1 = 'jim'
        username2 = 'boo'
    # ایجاد کد تخفیف
    discount_code = f'{username1}_{username}_{username2}{random_number}'

    cur.execute("UPDATE users SET email = %s, referral_code = %s WHERE client_code = %s",
                (email_validate, discount_code, client_code))

    bot.send_message(client_code,
                     f'متن تستی کد تخفیف \n   <code>{discount_code}</code>',
                     parse_mode='HTML')
    cur.execute("INSERT INTO discount_codes (name, percentage, owner,status) VALUES (%s, %s, %s,%s);",
                (discount_code, 10, client_code, 1))

    cur.execute("INSERT INTO referrals (client_code,people,income) VALUES (%s,%s,%s);", (client_code, 0, 0))
    # ذخیره تغییرات
    conn.commit()

    # بستن cursor و اتصال🙃
    cur.close()
    conn.close()


#################################
#
#
#
#
#           BUY
#
#
#
#
####################################


def send_purchase_confirmation(chat_id, tariff):
    limit = 0
    if tariff == "tarefe30gig":
        limit = 30
    elif tariff == "tarefe50gig":
        limit = 50
    elif tariff == "tarefe70gig":
        limit = 70
    elif tariff == "tarefe90gig":
        limit = 90
    elif tariff == "tarefe120gig":
        limit = 120

    if limit != 0:
        global buy_config
        buy_config = hiddify_api_put(chat_id, 40, limit)
        bot.send_message(chat_id, buy_config, reply_markup=qr())

        bot.send_message(chat_id,
                         f"لینک بالا برای استفاده روی سیستم عامل های Android و ios میباشد گر فایل همین کانفیگ رو میخاهید به پشتیبانی مراجعه کنید \n نام کاربری شما:<code>{chat_id}</code> \n  روی شماره کاربریت کلیک کن و مستقیم به آیدی زیر ارسال کن. \n آیدی:@jimboovpn_Support",
                         parse_mode="HTML",
                         reply_markup=get_education_platform_buttons())
        return True
    else:
        bot.send_message(chat_id, "شما تعرفه درستی رو انتخاب نکردید")


@bot.callback_query_handler(func=lambda call: call.data == "qqq")
def qr_code_code(call):
    slts_qrcode = segno.make_qr(f'{buy_config}')
    background_image_path = Path("root/telegram_bot/bot/telegram_bot/asli.jpg")
    # Generate artistic QR code
    slts_qrcode.to_artistic(
        background=background_image_path,
        target="animated_qrcode_telegram.png",
        scale=10,
    )

    # Open the generated image (adjust for photo or animation)
    with open("animated_qrcode_telegram.png", "rb") as image_file:
        image_data = image_file.read()

    # Send the image using the appropriate bot method (photo or animation)
    bot.send_photo(call.message.chat.id, image_data)

    # Clean up (optional)
    # os.remove("animated_qrcode_telegram.png")


@bot.callback_query_handler(func=lambda call: call.data == "kharid_azma")
def kharid_azma(call):
    bot.send_message(call.message.chat.id,
                     f" با استفاده از ایدی زیر میتونی ترون رو به پایین ترین قیمت تهیه کنی و داشبوردتو مستقیم شارژ کنی. \n نام کاربری شما:<code>{call.message.chat.id}</code> \n  روی شماره کاربریت کلیک کن و مستقیم به آیدی زیر ارسال کن. \n  (این ایدی مورد تایید جیمبو میباشد)👇  \n آیدی:@jimboovpn_Support",
                     parse_mode="HTML",
                     reply_markup=amozesh_kharid_tron_az_ma())


def buy_ekhtesasi(chat_id, tron, days, volume):
    if check_membership(chat_id, channel_username):
        user_id = find_user_id_from_client_code(chat_id)
        tron = Decimal(tron)
        if user_id is not None:
            balance = show_user_wallet_balance(user_id)
            if balance >= tron != 0:
                bot.send_message(chat_id, hiddify_api_put(chat_id, days, volume, ))
                bot.send_message(chat_id,
                                 f"لینک بالا برای استفاده روی سیستم عامل های Android و ios میباشد گر فایل همین کانفیگ رو میخاهید به پشتیبانی مراجعه کنید \n نام کاربری شما:<code>{chat_id}</code> \n  روی شماره کاربریت کلیک کن و مستقیم به آیدی زیر ارسال کن. \n آیدی:@jimboovpn_Support",
                                 parse_mode="HTML",
                                 reply_markup=get_education_platform_buttons())
                buy_payment(user_id, tron)
                balance -= tron  # بروزرسانی موجودی پس از خرید
            else:
                bot.send_message(chat_id, "شما پول کافی ندارید")


@bot.callback_query_handler(func=lambda call: call.data.startswith("tarefe"))
def handle_buy_callback(call):
    if check_membership(call.message.chat.id, channel_username):
        user_id = find_user_id_from_client_code(call.message.chat.id)
        if user_id is not None:
            balance = show_user_wallet_balance(user_id)
            price = 0
            if call.data == "tarefe30gig":
                price = Decimal("11")
            elif call.data == "tarefe50gig":
                price = Decimal("17")
            elif call.data == "tarefe70gig":
                price = Decimal("22")
            elif call.data == "tarefe90gig":
                price = Decimal("27")
            elif call.data == "tarefe120gig":
                price = Decimal("31")

            if balance >= price != 0:
                if send_purchase_confirmation(call.message.chat.id, call.data):
                    buy_payment(user_id, price)
                    balance -= price  # بروزرسانی موجودی پس از خرید

                    bot.send_message(call.message.chat.id,
                                     f"خرید شما با موفقیت انجام شد. موجودی جدید شما: {balance} ترون")
                else:
                    bot.send_message(call.message.chat.id, "خطایی در انجام تراکنش رخ داد.")
            else:
                bot.send_message(call.message.chat.id,
                                 f"متاسفانه موجودی شما کافی نیست. موجودی فعلی شما: {balance} ترون",
                                 reply_markup=get_wallet_recharge_buttons())
        else:
            bot.send_message(call.message.chat.id, "کاربر یافت نشد.مجددا start کنید بات رو")


@bot.callback_query_handler(func=lambda call: call.data == "Ekhtesasi")
def Ekhtesasi(call):
    bot.send_message(call.message.chat.id,
                     " شمامیتوانید با وارد کردن تعداد روز مقدار حجم کانفیگ و تعداد کاربر کانفیگ خودتون رو اختصاصی کنید \n\n مقدار ثابت و حداقلی هر کانفیگ 30 گیگ 40 روز و تعداد کاربر 2 میباشد ",
                     reply_markup=ekhtesasiii())


@bot.callback_query_handler(func=lambda call: call.data == "make_config")
def mmd(call):
    msg = bot.send_message(call.message.chat.id,
                           "حجم مد نظر خودتون رو وارد کنید با عدد انگلیسی نهایت حجم 1000 \n مثال:(150)")
    bot.register_next_step_handler(msg, vol)


def vol(message):
    global volume
    volume = int(message.text)
    days = bot.send_message(message.chat.id,
                            'تعداد روز های مدنظر خودتون رو با عدد انگلیسی وارد کنید که باید بیشتر از 40 باشد (کمتر از 40 روز 40 درنظر گرفته خواهد شد) \n برای مثال:(90)')
    bot.register_next_step_handler(days, client)


def client(message):
    global day
    day = int(message.text)
    if day < 40:
        day = 40
    elif day > 1000:
        day = 1000
        bot.send_message(message.chat.id,
                         "عددی که برای تعداد روز وارد کردید بزرگتر ۱۰۰۰ بود و برای شما ۱۰۰۰ درنظر گرفته شد")
        bot.send_message(message.chat.id, "عددی که وارد کردید کوچکتر از 40 بود و برای شما همان 40 روز لحاظ شد")
    client = bot.send_message(message.chat.id,
                              "تعداد کاربران رو مشخص کنید و حداقل دوکاربر درنظر گرفته خواهد شد \n مثال:(3) ")
    bot.register_next_step_handler(client, defa)


def defa(message):
    global clieee
    clieee = int(message.text)
    if clieee < 2:
        clieee = 2
        bot.send_message(message.chat.id, "عددی که وارد کردید کوچکتر از 2 بود و برای شما همان 2 کاربر لحاظ شد")
    mmd = day - 40
    mmd2 = clieee - 2

    if volume > 1000:
        volume_asli = 1000
        bot.send_message(message.chat.id, "حجمی که وارد کردید بیشتر از 1000بود و برای شما 1000 درنظرگرفته شد")

    else:
        volume_asli = volume

    su = (2400 * volume_asli) + (1400 * mmd) + (mmd2 * 13000)
    global rounded_trtr
    trtr = su / 7000
    rounded_trtr = round(trtr, 2)  # گرد کردن به دو رقم اعشار

    bot.send_message(message.chat.id,
                     f'کانفیگ شما با حجم {volume} و تعداد {day} روز و با تعداد کاربر {clieee} محاسبه شد \n \n    این کانفیگ با مبلغ {su} هزار تومان معادل {rounded_trtr} ترون تقدیم شما قرار خواهد گرفت',
                     reply_markup=tarefe_ekhtesai_buy())


@bot.callback_query_handler(func=lambda call: call.data == "EEEE")
def buy_callback(call):
    buy_ekhtesasi(call.message.chat.id, rounded_trtr, day, volume)


def fetch_trx_details(hash1, api_key, target_wallet_address):
    trx_info_url = f"https://apilist.tronscan.org/api/transaction-info?hash={hash1}&apikey={api_key}"
    trx_response = requests.get(trx_info_url)

    if trx_response.status_code == 200:
        trx_data = trx_response.json()
        if trx_data.get('toAddress') == target_wallet_address and trx_data.get('contractRet') == 'SUCCESS':
            trx_amount = trx_data['contractData']['amount'] / 1_000_000  # تبدیل واحد از سانت به ترون

            rounded_amount = math.ceil(trx_amount * 10) / 10

            return rounded_amount, hash1

        else:
            return None, None
    else:
        return None, None


@bot.callback_query_handler(func=lambda call: call.data == "sharzh")
def handle_sharzh_callback(call):
    bot.send_message(call.message.chat.id, "اگر کد تخفیف دارید وارد کنید", reply_markup=discount())


@bot.callback_query_handler(func=lambda call: call.data == "edame_kharid")
def handle_edame_kharid_callback(call, discount_percentage=0):
    address = "TRZw3VgCdJoz93akEAt7yrMC1Wr6FgUFqY"
    bot.send_message(call.message.chat.id,
                     f"برای شارژ داشبورد جیمبو خود، ترون را به آدرس زیر ارسال کنید:\n\n<code>{address}</code>",
                     parse_mode="HTML")
    bot.send_message(call.message.chat.id, "پس از ارسال، کد هش تراکنش را اینجا وارد کنید:",
                     reply_markup=get_back_buttons())
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_transaction_hash,
                                              percent_asli=discount_percentage)


@bot.callback_query_handler(func=lambda call: call.data == "discount")
def dis(call):
    msg = bot.send_message(call.message.chat.id, "کد تخفیف خودتون رو وارد کنید", reply_markup=get_back_buttons())
    bot.register_next_step_handler(msg, disco, call)


def disco(message, call):
    discount_client = message.text
    if message.text == "برگشت":
        bot.send_message(message.chat.id, "شما به منوی اصلی برگشتید", reply_markup=get_main_buttons())
        return

    client_code = message.chat.id
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT percentage,status,owner FROM discount_codes WHERE name = %s", (discount_client,))
    is_done = cur.fetchone()
    if is_done:
        discount_percentage = is_done[0]
        status = is_done[1]
        owner = is_done[2]
        if status == 1:
            cur.execute("SELECT join_by_code FROM users WHERE client_code = %s", (client_code,))
            cliiii = cur.fetchone()[0]
            if cliiii is None or cliiii == str(owner):
                if cliiii is None:
                    cur.execute("UPDATE referrals SET people = people + %s WHERE client_code = %s", (1, owner))

                cur.execute("UPDATE users SET join_by_code = %s WHERE client_code = %s", (owner, client_code))
                conn.commit()
                bot.send_message(message.chat.id,
                                 f'کد تخفیف شما ثبت شد در اینجا با هر مقدار شارژ به مقدار کد تخفیف  {discount_percentage}%')
                handle_edame_kharid_callback(call, discount_percentage)
            else:
                bot.send_message(call.message.chat.id,
                                 "کد تخفیفی که وارد کردید رفرال بوده و قبلا شما توسط فرد دیگری دعوت شدید \n لطفا از کدتخفیف های عمومی استفاده کنید")
                return
        else:
            bot.send_message(message.chat.id,
                             f'کد تخفیف شما ثبت شد در اینجا با هر مقدار شارژ به مقدار کدتخفیف خود شارژ رایگان دریافت کنید')
            handle_edame_kharid_callback(call, discount_percentage)
    else:
        bot.send_message(message.chat.id, f' کد تخفیف شما مورد تایید قرار نگرفت ', reply_markup=get_main_buttons())


def insert_payment_and_update_wallet(conn, amount, transaction_hash, client_code, percent_asli, rounded):
    with conn.cursor() as cur:
        # پیدا کردن wallet_id با استفاده از client_code
        cur.execute("SELECT w.wallet_id FROM wallets w JOIN users u ON w.user_id = u.user_id WHERE u.client_code = %s;",
                    (client_code,))
        wallet_info = cur.fetchone()
        if wallet_info:
            wallet_id = wallet_info[0]
            # ذخیره تراکنش در جدول payments
            cur.execute(
                "INSERT INTO payments (wallet_id, amount, hash_code,discount_percentage) VALUES (%s, %s, %s,%s);",
                (wallet_id, amount, transaction_hash, percent_asli))
            # به‌روزرسانی موجودی داشبورد جیمبو
            cur.execute("UPDATE wallets SET balance = balance + %s , all_buy = all_buy + %s  WHERE wallet_id = %s;",
                        (amount, rounded, wallet_id))
            conn.commit()
            return True
        else:
            # اگر wallet_id پیدا نشود، عملیات ناموفق است
            return False


def process_transaction_hash(message, percent_asli):
    hash1 = message.text
    client_code = message.chat.id

    if message.text == "برگشت":
        bot.send_message(message.chat.id, "شما به منوی اصلی برگشتید", reply_markup=get_main_buttons())
        return

    elif len(hash1) != 64:
        bot.send_message(message.chat.id, "به نظر می‌رسد که کد هش وارد شده نامعتبر است. لطفاً مجدداً امتحان کنید.",
                         reply_markup=get_main_buttons())
        return

    # اتصال به دیتابیس
    conn = connect_db()
    cur = conn.cursor()

    # بررسی تکراری بودن کد هش
    cur.execute("SELECT EXISTS(SELECT 1 FROM payments WHERE hash_code = %s);", (hash1,))
    if cur.fetchone()[0]:
        bot.send_message(message.chat.id, "کد هش قبلا ثبت شده است.", get_main_buttons())
        cur.close()
        conn.close()
        return

    bot.send_message(message.chat.id, "لطفاً کمی صبر کنید، در حال بررسی تراکنش...")

    # اینجا کد برای fetch_trx_details اضافه می‌شود (فرضی)
    rounded, hash_verified = fetch_trx_details(hash1, "30a1c098-6be5-4561-ad20-06b34d999dce",
                                               "TRZw3VgCdJoz93akEAt7yrMC1Wr6FgUFqY")

    rounded_plus_bounos = rounded + ((rounded * percent_asli) / 100)

    if rounded_plus_bounos is not None and hash_verified:
        # در اینجا کد برای insert_payment_and_update_wallet اضافه می‌شود (فرضی)
        if insert_payment_and_update_wallet(conn, rounded_plus_bounos, hash1, message.chat.id, percent_asli, rounded):
            bot.send_message(message.chat.id,
                             f"داشبورد جیمبو شما با موفقیت شارژ شد. به مقدار: {rounded_plus_bounos} ترون")
            safirs = []
            current_client_code = client_code

            for i in range(0, 10):

                cur.execute("SELECT join_by_code FROM users WHERE client_code = %s;", (current_client_code,))
                result = cur.fetchone()
                if result is not None:
                    current_client_code = result[0]
                    safirs.append(current_client_code)
                else:
                    break

            aval = safirs[0]
            total_money = rounded
            num_people = len(safirs)

            first_person_money = total_money * 0.10
            first_person_money = round(first_person_money, 2)

            remaining_money = total_money - first_person_money

            per_person_money = remaining_money * 0.03 / num_people
            per_person_money = round(per_person_money, 2)

            cur.execute("UPDATE referrals SET income = income + %s WHERE client_code = %s;",
                        (first_person_money, str(aval)))
            bot.send_message(aval, f'شما به مبلغ {first_person_money} از طریق زیر مجموعه مستقیم شارژ شدید')
            for i in range(1, num_people):
                clieclie = safirs[i]
                if clieclie is not None:
                    cur.execute("UPDATE referrals SET income = income + %s WHERE client_code = %s;",
                                (per_person_money, str(clieclie)))
                    bot.send_message(clieclie,
                                     f'شما به مبلغ {per_person_money} از طریق زیر مجموعه غیر مستقیم شارژ شدید')

            conn.commit()

        else:
            bot.send_message(message.chat.id, "مشکلی در بروزرسانی داشبورد جیمبو به وجود آمد.")
    else:
        bot.send_message(message.chat.id, "تراکنش معتبر نیست یا تأیید نشده است.")

    cur.close()
    conn.close()


@bot.callback_query_handler(func=lambda call: call.data == "Dastgah")
def Amozesh_etesal(call):
    bot.send_message(call.message.chat.id, "دستگاه مد نظر خودتون رو انتخاب کنید",
                     reply_markup=get_education_platform_buttons())


@bot.callback_query_handler(func=lambda call: call.data.startswith("AMOZESH"))
def handle_buy_callback(call):
    if call.date == "AMOZESH_android":
        pass
    elif call.date == "AMOZESH_ios":
        pass
    elif call.date == "AMOZESH_windows":
        pass
    elif call.date == "AMOZESH_mac":
        pass


def tron_price(client_code):
    bot.send_chat_action(client_code, action='typing')
    bot.send_message(client_code, "چند لحظه صبر کنید")
    url = 'https://bitmit.co/price/TRX'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    root = soup.find_all("div", {"class": "container"})
    for m in root:
        asghar = m.find_all("div", {"class": "row justify-content-evenly gap-2 gap-md-1 gap-lg-2"})
        if asghar:
            for item in asghar:
                s = item.find_all("div",
                                  {
                                      "class": "col-12 col-md-6 col-lg-4 col-xl-3 text-center shadow-box rounded-6 bg-white"})
                if s:
                    for ahmad in s:
                        h5_tag = ahmad.find('h5')
                        my_string = h5_tag.text
                        time.sleep(10)
                        bot.send_message(client_code, f'ترون در حال حاضر {my_string} می باشد  . ')

                        break
                break
            break


def check_safir(client_code):
    conn = connect_db()
    cur = conn.cursor()

    # بررسی تکراری بودن کد هش
    cur.execute("SELECT EXISTS(SELECT 1 FROM referrals WHERE client_code = %s);", (client_code,))
    if cur.fetchone()[0]:
        return True
    else:
        return False


def income_safir(client_code):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT people, income FROM referrals WHERE client_code = %s;", (client_code,))
    safir = cur.fetchone()
    if safir:
        people = safir[0]
        income = safir[1]
        cur.execute("SELECT referral_code FROM users WHERE client_code = %s;", (client_code,))
        referral_code = cur.fetchone()
        if referral_code:
            referral_code = referral_code[0]
            bot.send_message(client_code,
                             f' افراد زیر مجموعه: {people} نفر\n درامد فعلی شما: {income}ترون \n کد تخفیف اختصاصی شما \n <code>{referral_code}</code>',
                             parse_mode='HTML', reply_markup=bardasht())
            return True

    return


def test_account(chat_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT test_account FROM users WHERE client_code = %s;", (chat_id,))
    test_account = cur.fetchone()
    test_account_value = test_account[0]  # برداشتن مقدار از تاپل
    if test_account_value == False:
        bot.send_message(chat_id, hiddify_api_put(chat_id, 0, 0.1, ))
        bot.send_message(chat_id,
                         "این کانفیگ تا ۱۲ شب فعال است از هر زمان که شروع کنید به استفاده تا ۱۲ شب همون روز زمان دارید")

        cur.execute("UPDATE users SET test_account = %s WHERE client_code = %s;", (True, chat_id))
        conn.commit()

    else:
        bot.send_message(chat_id, "یکبار از اکانت تستی استفاده کردی \n الان میتونی با یه تخفیف خوب اکانت خودتو بسازی👇",
                         reply_markup=discount2())


@bot.callback_query_handler(func=lambda call: call.data == "bardasht")
def bardasht1(call):
    bot.send_message(call.message.chat.id,
                     f' با استفاده از ایدی زیر میتونی برداشت ترون انجام بدی حداقل مقدار برداشت ۱۰ ترون میباشد. \n نام کاربری شما:<code>{call.message.chat.id}</code> \n  روی شماره کاربریت کلیک کن و مستقیم به آیدی زیر ارسال کن. \n آیدی:@jimboovpn_Support',
                     parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data == "mmd2")
def dddd(call):
    bot.send_message(call.message.chat.id, "تعرفه مورد نظر خودتون رو انتخاب کنید", reply_markup=get_tariff_buttons())


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
