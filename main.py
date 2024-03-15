import telebot
from config import BOT_TOKEN
from buttons import *
from database import *
import requests
import math
from decimal import Decimal

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    client_code = message.from_user.id  # استفاده از ID تلگرام به عنوان client_code
    username = message.from_user.username or "NoUsername"  # برای کاربرانی که username ندارند
    save_user_and_create_wallet(client_code, username)
    reply_markup = get_main_buttons()
    bot.send_message(message.chat.id, "♥️سلام دوست عزیز\n\nبه ربات جیمبو خوش آمدید🚀\n\nلطفا یک گزینه را انتخاب کنید👇",
                     reply_markup=reply_markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):

    if message.text == "خرید اشتراک💴":
        bot.send_message(message.chat.id, "تعرفه مورد نظر خودتون رو انتخاب کنید", reply_markup=get_tariff_buttons())
    elif message.text == 'پشتیبانی👥':
        bot.send_message(message.chat.id, "با مطالعه سوالات متداول ممکنه به جوابت برسی",
                         reply_markup=get_support_buttons())
    elif message.text == "شارژ کیف پول⚡️":
        # فرض می‌شود تابع `find_user_id_from_client_code` ID کاربر را بر اساس chat_id بازگرداند
        user_id = find_user_id_from_client_code(message.chat.id)
        balance = show_user_wallet_balance(user_id)
        bot.send_message(message.chat.id, f"مقدار موجودی شما: {balance} دلار",
                         reply_markup=get_wallet_recharge_buttons())
    elif message.text == "آموزش استفاده👨🏻‍🏫":
        bot.send_message(message.chat.id, "آموزش مد نظرتو انتخاب کن", reply_markup=get_education_buttons())


def send_purchase_confirmation(chat_id, tariff):
    conn = connect_db()
    cur = conn.cursor()

    with conn.cursor() as cur:

        if tariff == "tarefe1":
            cur.execute("SELECT link,address,name FROM links WHERE status = %s AND amount = %s;", (0, 1))
            rows = cur.fetchone()
            print(rows)
            if rows:
                for row in rows:
                    link = row[0]
                    address = row[1]
                    name = row[2]
                    print(tariff)
                    bot.send_message(chat_id, link)
                    bot.send_message(chat_id, "لینک بالا برای ios , اندروید  است")
                    with open(f'{address}{name}', 'r') as file:
                        bot.send_document(chat_id, file, caption="این فایل برای windows  میباشد امیدوارم لذت ببرید")
                    cur.execute("UPDATE links SET status = %s WHERE link = %s;", (1, link))
                    # commit تغییرات به دیتابیس
                    conn.commit()
                return True
            else:
                bot.send_message(chat_id,
                                 "این تعرفه درحال حاضر موجود نیست لطفا از کانفیگ های دیگر استفاده کنید یا به پشتیبانی اطلاع دهید")
                return False
        elif tariff == "tarefe2":
            cur.execute("SELECT link,address,name FROM links WHERE status = %s AND amount = %s;", (0, 1.5))
            rows = cur.fetchone()
            if rows:
                for row in rows:
                    link = row[0]
                    address = row[1]
                    name = row[2]
                    bot.send_message(chat_id, link)
                    bot.send_message(chat_id, "لینک بالا برای ios , اندروید  است")
                    with open(f'{address}{name}', 'r') as file:
                        bot.send_document(chat_id, file, caption="این فایل برای windows  میباشد امیدوارم لذت ببرید")
                    cur.execute("UPDATE links SET status = %s WHERE link = %s;", (1, link))
                    # commit تغییرات به دیتابیس
                    conn.commit()
                return True
            else:
                bot.send_message(chat_id,
                                 "این تعرفه درحال حاضر موجود نیست لطفا از کانفیگ های دیگر استفاده کنید یا به پشتیبانی اطلاع دهید")
                return False
        elif tariff == "tarefe3":
            cur.execute("SELECT link,address,name FROM links WHERE status = %s AND amount = %s;", (0, 2))
            rows = cur.fetchone()
            if rows:
                for row in rows:
                    link = row[0]
                    address = row[1]
                    name = row[2]
                    bot.send_message(chat_id, link)
                    bot.send_message(chat_id, "لینک بالا برای ios , اندروید  است")
                    with open(f'{address}{name}', 'r') as file:
                        bot.send_document(chat_id, file, caption="این فایل برای windows  میباشد امیدوارم لذت ببرید")
                    cur.execute("UPDATE links SET status = %s WHERE link = %s;", (1, link))
                    # commit تغییرات به دیتابیس
                    conn.commit()
                return True
            else:
                bot.send_message(chat_id,
                                 "این تعرفه درحال حاضر موجود نیست لطفا از کانفیگ های دیگر استفاده کنید یا به پشتیبانی اطلاع دهید")
                return False


@bot.callback_query_handler(func=lambda call: call.data.startswith("tarefe"))
def handle_buy_callback(call):
    user_id = find_user_id_from_client_code(call.message.chat.id)
    if user_id is not None:
        balance = show_user_wallet_balance(user_id)
        price = 0
        if call.data == "tarefe1":
            price = Decimal("1")
        elif call.data == "tarefe2":
            price = Decimal("1.5")
        elif call.data == "tarefe3":
            price = Decimal("2")
        if balance >= price != 0:
            # انجام تراکنش و بروزرسانی موجودی
            if buy_payment(user_id, price):

                balance -= price  # بروزرسانی موجودی پس از خرید
                send_purchase_confirmation(call.message.chat.id, call.data)

                bot.send_message(call.message.chat.id, f"خرید شما با موفقیت انجام شد. موجودی جدید شما: {balance} دلار")
            else:
                bot.send_message(call.message.chat.id, "خطایی در انجام تراکنش رخ داد.")
        else:
            bot.send_message(call.message.chat.id, f"متاسفانه موجودی شما کافی نیست. موجودی فعلی شما: {balance} دلار",
                             reply_markup=get_money())
    else:
        bot.send_message(call.message.chat.id, "کاربر یافت نشد.مجددا start کنید بات رو")


def fetch_trx_details(hash1, api_key, target_wallet_address):
    trx_info_url = f"https://apilist.tronscan.org/api/transaction-info?hash={hash1}&apikey={api_key}"
    trx_response = requests.get(trx_info_url)

    if trx_response.status_code == 200:
        trx_data = trx_response.json()
        if trx_data.get('toAddress') == target_wallet_address and trx_data.get('contractRet') == 'SUCCESS':
            trx_amount = trx_data['contractData']['amount'] / 1_000_000  # تبدیل واحد از سانت به ترون

            price_url = 'https://api.coingecko.com/api/v3/simple/price?ids=tron&vs_currencies=usd'
            price_response = requests.get(price_url)

            if price_response.status_code == 200:
                price_data = price_response.json()
                tron_price = price_data['tron']['usd']
                usdt_amount = tron_price * trx_amount
                rounded_amount = math.ceil(usdt_amount * 100) / 100
                return rounded_amount, hash1
            else:
                print("Error fetching Tron price.")
                return None, None
        else:
            print("Transaction not successful or toAddress mismatch.")
            return None, None
    else:
        print("Error fetching transaction details.")
        return None, None


@bot.callback_query_handler(func=lambda call: call.data == "sharzh")
def handle_sharzh_callback(call):
    address = "TApqj7VRYQtt8wXcy22rhont6oECgNqCXQ"
    bot.send_message(call.message.chat.id,
                     f"برای شارژ کیف پول خود، ترون را به آدرس زیر ارسال کنید:\n<code>{address}</code>",
                     parse_mode="HTML")
    bot.send_message(call.message.chat.id, "پس از ارسال، کد هش تراکنش را اینجا وارد کنید:")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_transaction_hash)


def insert_payment_and_update_wallet(conn, amount, transaction_hash, client_code):
    with conn.cursor() as cur:
        # پیدا کردن wallet_id با استفاده از client_code
        cur.execute("SELECT w.wallet_id FROM wallets w JOIN users u ON w.user_id = u.user_id WHERE u.client_code = %s;",
                    (client_code,))
        wallet_info = cur.fetchone()
        if wallet_info:
            wallet_id = wallet_info[0]
            # ذخیره تراکنش در جدول payments
            cur.execute("INSERT INTO payments (wallet_id, amount, hash_code) VALUES (%s, %s, %s);",
                        (wallet_id, amount, transaction_hash))
            # به‌روزرسانی موجودی کیف پول
            cur.execute("UPDATE wallets SET balance = balance + %s WHERE wallet_id = %s;", (amount, wallet_id))
            conn.commit()
            return True
        else:
            # اگر wallet_id پیدا نشود، عملیات ناموفق است
            return False


def process_transaction_hash(message):
    hash1 = message.text
    if len(hash1) != 64:
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
                                               "TApqj7VRYQtt8wXcy22rhont6oECgNqCXQ")
    if rounded is not None and hash_verified:
        # در اینجا کد برای insert_payment_and_update_wallet اضافه می‌شود (فرضی)
        if insert_payment_and_update_wallet(conn, rounded, hash1, message.chat.id):
            bot.send_message(message.chat.id, f"کیف پول شما با موفقیت شارژ شد. به مقدار: {rounded} دلار")
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
    bot.send_video(call.message.chat.id, open("/root/telegram_bot/videos/vid.mp4", 'rb'))


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
