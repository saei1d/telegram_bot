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
import re

bot = telebot.TeleBot(BOT_TOKEN)


def check_membership(chat_id, channel_username):
    member = bot.get_chat_member(channel_username, chat_id)
    if member.status == 'member' or member.status == 'creator' or member.status == 'administrator':
        return True
    else:
        bot.send_message(chat_id, f'برای استفاده از ربات، لطفا عضو کانال {channel_username} شوید.')
        return False


admin_user_ids = [366470485, 6696631466]


@bot.message_handler(commands=['admin'])
def handle_admin_settings(message):
    print('aaaa')
    if message.from_user.id in admin_user_ids:
        bot.send_message(message.chat.id, 'Admin settings menu.')

    else:
        bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    channel_username = '@jimboo_vpn'
    client_code = message.from_user.id
    if check_membership(chat_id, channel_username):
        username = message.from_user.username or "NoUsername"  # برای کاربرانی که username ندارند
        save_user_and_create_wallet(client_code, username)
        reply_markup = get_main_buttons()
        bot.send_message(message.chat.id,
                         "♥️سلام دوست عزیز\n\nبه ربات جیمبو خوش آمدید🚀\n\nلطفا یک گزینه را انتخاب کنید👇",
                         reply_markup=reply_markup)

    else:
        bot.send_message(chat_id, 'اگر جوین شدید مجدد /start کنید')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if message.text == "خرید اشتراک":
        bot.send_message(message.chat.id, "تعرفه مورد نظر خودتون رو انتخاب کنید", reply_markup=get_tariff_buttons())
    elif message.text == 'پشتیبانی':
        bot.send_message(message.chat.id, "با مطالعه سوالات متداول ممکنه به جوابت برسی",
                         reply_markup=get_support_buttons())
    elif message.text == "کیف پول":

        # فرض می‌شود تابع `find_user_id_from_client_code` ID کاربر را بر اساس chat_id بازگرداند
        user_id = find_user_id_from_client_code(message.chat.id)
        balance = show_user_wallet_balance(user_id)
        bot.send_message(message.chat.id, f"مقدار موجودی شما: {balance} ترون",
                         reply_markup=get_wallet_recharge_buttons())
    elif message.text == "آموزش استفاده":
        bot.send_message(message.chat.id, "آموزش مد نظرتو انتخاب کن", reply_markup=get_education_buttons())

    elif message.text == "قیمت لحظه ای ترون":
        bot.send_message(message.chat.id, tron_price(chat_id))

    elif message.text == "عودت وجه":
        bot.send_message(message.chat.id, "متن تستی عودت وجه")
    elif message.text == "درامدزایی":
        bot.send_message(message.chat.id, "متن تستی درامد زایی ", reply_markup=button_validate())
    elif message.text == "ارسال ایمیل":
        msg = bot.send_message(message.chat.id, "لطفا ایمیل خودتون رو وارد کنید \n  مثال: example@gmail.com")
        bot.register_next_step_handler(msg, email)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    data = json.loads(message.contact)
    # دسترسی به اطلاعات مورد نظر
    phone_number = data['phone_number']
    first_name = data['first_name']
    user_id = data['user_id']
    phone = int(phone_number)
    print(type(phone_number))
    print(phone_number,first_name,user_id)
    make_refral_wallet_by_phone(user_id, first_name, phone)


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
    discount_code = f'{username1}%{username}%{username2}{random_number}'

    cur.execute("UPDATE users SET first_name = %s , phone_number = %s, referral_code = %s WHERE client_code = %s",
                (first_name, phone, discount_code, client_code))

    bot.send_message(client_code,
                     f'متن تستی کد تخفیف \n   <code>{discount_code}</code>',
                     parse_mode='HTML')

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
    discount_code = f'{username1}%{username}%{username2}{random_number}'

    cur.execute("UPDATE users SET email = %s, referral_code = %s WHERE client_code = %s",
                (email_validate, discount_code, client_code))

    bot.send_message(client_code,
                     f'متن تستی کد تخفیف \n   <code>{discount_code}</code>',
                     parse_mode='HTML')

    # ذخیره تغییرات
    conn.commit()

    # بستن cursor و اتصال
    cur.close()
    conn.close()


def send_purchase_confirmation(chat_id, tariff):
    if tariff == "tarefe30gig":
        bot.send_message(chat_id, hiddify_api_put(chat_id, 40, 30, ))
        bot.send_message(chat_id,
                         "لینک بالا برای اندروید و ios مورد استفاده است درصورت نیاز به فایل windowsکانفیگ همراه با uuid به پشتیبانی مراجعه کنید",
                         reply_markup=get_education_platform_buttons())
        return True
    elif tariff == "tarefe50gig":
        bot.send_message(chat_id, hiddify_api_put(chat_id, 40, 50, ))
        bot.send_message(chat_id,
                         "لینک بالا برای اندروید و ios مورد استفاده است درصورت نیاز به فایل windowsکانفیگ همراه با uuid به پشتیبانی مراجعه کنید",
                         reply_markup=get_education_platform_buttons())
        return True
    elif tariff == "tarefe70gig":
        bot.send_message(chat_id, hiddify_api_put(chat_id, 40, 70, ))
        bot.send_message(chat_id,
                         "لینک بالا برای اندروید و ios مورد استفاده است درصورت نیاز به فایل windowsکانفیگ همراه با uuid به پشتیبانی مراجعه کنید",
                         reply_markup=get_education_platform_buttons())
        return True
    elif tariff == "tarefe90gig":
        bot.send_message(chat_id, hiddify_api_put(chat_id, 40, 90, ))
        bot.send_message(chat_id,
                         "لینک بالا برای اندروید و ios مورد استفاده است درصورت نیاز به فایل windowsکانفیگ همراه با uuid به پشتیبانی مراجعه کنید",
                         reply_markup=get_education_platform_buttons())
        return True
    elif tariff == "tarefe120gig":
        bot.send_message(chat_id, hiddify_api_put(chat_id, 40, 120, ))
        bot.send_message(chat_id,
                         "لینک بالا برای اندروید و ios مورد استفاده است درصورت نیاز به فایل windowsکانفیگ همراه با uuid به پشتیبانی مراجعه کنید",
                         reply_markup=get_education_platform_buttons())
        return True


@bot.callback_query_handler(func=lambda call: call.data == "kharid_azma")
def kharid_azma(call):
    bot.send_message(call.message.chat.id,
                     "متن تستی خرید ازما بعلاوه یوزر نیم ترون فروش و دکمه زیر آموزش متنی تصویری لینک کانال",
                     reply_markup=amozesh_kharid_tron_az_ma())


@bot.callback_query_handler(func=lambda call: call.data.startswith("tarefe"))
def handle_buy_callback(call):
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
            # انجام تراکنش و بروزرسانی موجودی
            if send_purchase_confirmation(call.message.chat.id, call.data):
                buy_payment(user_id, price)
                balance -= price  # بروزرسانی موجودی پس از خرید

                bot.send_message(call.message.chat.id, f"خرید شما با موفقیت انجام شد. موجودی جدید شما: {balance} ترون")
            else:
                bot.send_message(call.message.chat.id, "خطایی در انجام تراکنش رخ داد.")
        else:
            bot.send_message(call.message.chat.id, f"متاسفانه موجودی شما کافی نیست. موجودی فعلی شما: {balance} ترون",
                             reply_markup=get_wallet_recharge_buttons())
    else:
        bot.send_message(call.message.chat.id, "کاربر یافت نشد.مجددا start کنید بات رو")


@bot.callback_query_handler(func=lambda call: call.data == "Ekhtesasi")
def Ekhtesasi(call):
    bot.send_message(call.message.chat.id,
                     " شمامیتوانید با وارد کردن تعداد روز مقدار حجم کانفیگ و تعداد کابر کانفیگ خودتون رو اختصاصی کنید \n\n  با وارد کردن عدد 0 اینگلیسی مقدار ثابت برای کانفیگ شما درنظر گرفته خواهد شد مثلا مقدار ثابت و حداقلی هر کانفیگ 40 روز و تعداد کاربر 2 میباشد ",
                     reply_markup=ekhtesasiii())


@bot.callback_query_handler(func=lambda call: call.data == "make_config")
def mmd(call):
    msg = bot.send_message(call.message.chat.id, "حجم مد نظر خودتون رو وارد کنید با عدد انگلیسی \n مثال:(150)")
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
    su = (2400 * volume) + (1400 * mmd) + (mmd2 * 13000)

    bot.send_message(message.chat.id,
                     f'کانفیگ شما با حجم {volume} و تعداد {day} روز و با تعداد کاربر {clieee} محاسبه شد \n \n    این کانفیگ با مبلغ {su} هزار تقدیم شما قرار خواهد گرفت')


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
    print(discount_percentage)
    address = "TRZw3VgCdJoz93akEAt7yrMC1Wr6FgUFqY"
    bot.send_message(call.message.chat.id,
                     f"برای شارژ کیف پول خود، ترون را به آدرس زیر ارسال کنید:\n\n<code>{address}</code>",
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
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT percentage FROM discount_codes WHERE name = %s", (discount_client,))
    is_done = cur.fetchone()
    if is_done:
        discount_percentage = is_done[0]
        bot.send_message(message.chat.id, f'کد تخفیف شما مورد تایید قرار گرفت به مقدار {discount_percentage}%')
        handle_edame_kharid_callback(call, discount_percentage)
    else:
        bot.send_message(message.chat.id, f' کد تخفیف شما مورد تایید قرار نگرفت ', reply_markup=get_back_buttons())
    if message.text == "برگشت":
        bot.send_message(message.chat.id, "شما به منوی اصلی برگشتید", reply_markup=get_main_buttons())
        return


def insert_payment_and_update_wallet(conn, amount, transaction_hash, client_code, percent_asli):
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
            # به‌روزرسانی موجودی کیف پول
            cur.execute("UPDATE wallets SET balance = balance + %s WHERE wallet_id = %s;", (amount, wallet_id))
            conn.commit()
            return True
        else:
            # اگر wallet_id پیدا نشود، عملیات ناموفق است
            return False


def process_transaction_hash(message, percent_asli):
    hash1 = message.text

    if message.text == "برگشت":
        bot.send_message(message.chat.id, "شما به منوی اصلی برگشتید", reply_markup=get_main_buttons())
        return

    elif len(hash1) != 64:
        bot.send_message(message.chat.id, "به نظر می‌رسد که کد هش وارد شده نامعتبر است. لطفاً مجدداً امتحان کنید.")
        return

    # اتصال به دیتابیس
    conn = connect_db()
    cur = conn.cursor()

    # بررسی تکراری بودن کد هش
    cur.execute("SELECT EXISTS(SELECT 1 FROM payments WHERE hash_code = %s);", (hash1,))
    if cur.fetchone()[0]:
        bot.send_message(message.chat.id, "کد هش قبلا ثبت شده است.")
        cur.close()
        conn.close()
        return

    bot.send_message(message.chat.id, "لطفاً کمی صبر کنید، در حال بررسی تراکنش...")

    # اینجا کد برای fetch_trx_details اضافه می‌شود (فرضی)
    rounded, hash_verified = fetch_trx_details(hash1, "30a1c098-6be5-4561-ad20-06b34d999dce",
                                               "TRZw3VgCdJoz93akEAt7yrMC1Wr6FgUFqY")
    rounded = rounded + ((rounded * percent_asli) / 100)
    print(rounded)
    if rounded is not None and hash_verified:
        # در اینجا کد برای insert_payment_and_update_wallet اضافه می‌شود (فرضی)
        if insert_payment_and_update_wallet(conn, rounded, hash1, message.chat.id, percent_asli):
            bot.send_message(message.chat.id, f"کیف پول شما با موفقیت شارژ شد. به مقدار: {rounded} ترون")
        else:
            bot.send_message(message.chat.id, "مشکلی در بروزرسانی کیف پول به وجود آمد.")
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


def tron_price(chat_id):
    bot.send_chat_action(chat_id, action='typing')
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
                        bot.send_message(chat_id, f'ترون در حال حاضر {my_string} می باشد  . ')

                        break
                break
            break


#                                ADMIN PANEL                      پنل ادمین


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
