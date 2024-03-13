# import telebot
# from telebot import TeleBot, types
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# import requests
# import math
#
# bot = telebot.TeleBot("7185006139:AAHuDttDr9T8MBPIEscn3wIkld5agDMjE9U")
#
# reply_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# reply_key.add("خرید اشتراک💴", "شارژ کیف پول⚡️", "آموزش استفاده👨🏻‍🏫","پشتیبانی👥","اشتراک های من🕰")
#
#
# tarefe1 = telebot.types.InlineKeyboardButton("یک ماهه دو کاربره ۱۰۰ گیگ (1 دلار) ", callback_data="tarefe1")
# tarefe2 = telebot.types.InlineKeyboardButton("یک ماهه دو کاربره ۱۵۰ گیگ(1.5 دلار)", callback_data="tarefe2")
# tarefe3 = telebot.types.InlineKeyboardButton("سه ماهه دو کاربره ۱۵۰ گیگ(2 دلار)", callback_data="tarefe3")
# tarefeha = telebot.types.InlineKeyboardMarkup(row_width=1)
# tarefeha.add(tarefe1, tarefe2, tarefe3)
#
#
#
# support1 = telebot.types.InlineKeyboardButton("پشتیبانی در اسرع وقت", callback_data="support")
# soalat = telebot.types.InlineKeyboardButton("سوالات متداول", callback_data="soalat")
# poshtibani = telebot.types.InlineKeyboardMarkup(row_width=2)
# poshtibani.add(support1, soalat)
#
# wallet1 = telebot.types.InlineKeyboardButton("شارژ کیف پول", callback_data="sharzh")
# buy = telebot.types.InlineKeyboardButton("خرید و کسر از کیف پول", callback_data="buy")
# kharid1 = telebot.types.InlineKeyboardMarkup(row_width=2)
# kharid1.add(buy, wallet1)
#
# amozeshkharid = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# amozeshkharid.add("ارز دیجیتال", "ووچر پرفکت مانی")
#
# amozesh = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# amozesh.add("شارژ کیف پول ", "اتصال به کانفیگ")
#
# amozeshplatform = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# amozeshplatform.add("اندروید", "ios", "windows", "mac")
#
# ersal_h = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# ersal_h.add("ارسال کد هش")
#
#
# def execute_query(query, data):
#     """این تابع برای اجرای کوئری‌هایی که نیازی به برگشت داده ندارند استفاده می‌شود."""
#     with psycopg2.connect(dbname="telegram", user="saeid", password="1111", host="localhost") as conn:
#         try:
#             with conn.cursor() as cur:
#                 cur.execute(query, data)
#                 conn.commit()
#         except Exception as e:
#             print(e)
#
#
# def execute_query_returning(query, data):
#     """این تابع یک کوئری SQL را اجرا می‌کند و داده‌های برگشتی را ریترن می‌کند."""
#     with psycopg2.connect(dbname="telegram", user="saeid", password="1111", host="localhost") as conn:
#         try:
#             with conn.cursor() as cur:
#                 cur.execute(query, data)
#                 return cur.fetchone()[0]  # فرض بر اینکه فقط یک ستون بازگردانده می‌شود
#         except Exception as e:
#             print(e)
#             return None
#
#
# @bot.message_handler(commands=["start"])
# def wellcome(message):
#     client_id = message.from_user.id
#     username = message.from_user.username or ''
#
#     sql_insert_user = '''
#     INSERT INTO users (client_code, username)
#     VALUES (%s, %s)
#     ON CONFLICT (client_code)
#     DO NOTHING;
#     '''
#     execute_query(sql_insert_user, (client_id, username))
#
#     # بررسی و دریافت user_id برای ایجاد ولت
#     sql_get_user_id = 'SELECT user_id FROM users WHERE client_code = %s;'
#     user_id = execute_query_returning(sql_get_user_id, (client_id,))
#
#     if user_id:
#         # اضافه کردن ولت برای کاربر اگر هنوز ولتی ندارد
#         sql_check_wallet = 'SELECT 1 FROM wallets WHERE user_id = %s;'
#         if not execute_query_returning(sql_check_wallet, (user_id,)):
#             sql_insert_wallet = 'INSERT INTO wallets (user_id, balance) VALUES (%s, 0);'
#             execute_query(sql_insert_wallet, (user_id,))
#
#     bot.send_message(message.chat.id, "♥️سلام دوست عزیزم\n\nبه ربات جیمبو خوش اومدی🚀\n\n👇👇لطفا یک گزینه رو انتخاب کن",
#                      reply_markup=reply_key)
#
#
# @bot.message_handler()
# def keyboard(message):
#     if message.text == "خرید اشتراک💴":
#         bot.send_message(message.chat.id, "تعرفه مورد نظر خودتون رو انتخاب کنید", reply_markup=tarefeha)
#     elif message.text == 'پشتیبانی👥':
#         bot.send_message(message.chat.id, "با مطالعه سولات متداول ممکنه به جوابت برسی", reply_markup=poshtibani)
#     elif message.text == "شارژ کیف پول⚡️":
#         sa = message.chat.id
#         user_id_for_balance = find_user_id_from_client_code(sa)
#         balancee = show_user_wallet_balance(user_id_for_balance)
#
#         bot.send_message(message.chat.id, f"مقدار موجودی شما {balancee}دلار است")
#
#     elif message.text == "آموزش استفاده👨🏻‍🏫":
#         bot.send_message(message.chat.id, "آموزش مد نظرتو انتخاب کن", reply_markup=amozesh)
#
#
# price = 0
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     global price
#     if call.data == "tarefe1":
#         price = 1
#         bot.send_message(call.message.chat.id, "لطفا یک گذینه رو انتخاب کنید", reply_markup=kharid1)
#     elif call.data == "tarefe2":
#         price = 1.5
#         bot.send_message(call.message.chat.id, "لطفا یک گذینه رو انتخاب کنید", reply_markup=kharid1)
#     elif call.data == "tarefe3":
#         price = 2
#         bot.send_message(call.message.chat.id, "لطفا یک گذینه رو انتخاب کنید", reply_markup=kharid1)
#     # elif call.data == "شارژ کیف پول":
#     #     bot.send_message(call.message.chat, "میتونید از اموزش های زیر استفاده کنید", reply_markup=amozeshkharid)
#     # elif call.data == "اتصال به کانفیگ":
#     #
#     #     bot.send_message(call.message, "میتونید از اموزش های زیر استفاده کنید", reply_markup=amozeshplatform)
#
#     elif call.data == "buy":
#         sa = call.message.chat.id
#         user_id_for_balance = find_user_id_from_client_code(sa)
#         b_balance = show_user_wallet_balance(user_id_for_balance)
#         if b_balance >= price:
#
#             if buy_payment(user_id_for_balance) == 1:
#                 if price == 1:
#                     bot.send_document(call.message.chat.id, open("/home/saeid/Documents/mmd.txt", 'r'))
#                 elif price == 1.5:
#                     bot.send_document(call.message.chat.id, open("/home/saeid/Documents/mmd.txt", 'r'))
#                 elif price == 2:
#                     bot.send_document(call.message.chat.id, open("/home/saeid/Documents/mmd.txt", 'r'))
#             else:
#                 print("kedjirkmf")
#
#
#     elif call.data == "sharzh":
#         m = ("<code>TGKK71EXdWxSbZQ5nQ4t5J2wHPL5ugLVYt</code>")
#         bot.send_message(call.message.chat.id, m, parse_mode="HTML")
#         bot.send_message(call.message.chat.id, "شما میتونید هر مبلغ دلخواهی شارژ کنید")
#         msg = bot.send_message(call.message.chat.id, "کد هش رو ارسال کنید لطفا")
#         bot.register_next_step_handler(msg, hash_recived)
#
#
# def hash_recived(message):
#     global hash1
#     hash1 = message.text
#     if len(hash1) > 64:
#         bot.send_message(message.chat.id, "کدی که وارد کردید بزرگتر است")
#     elif len(hash1) < 64:
#         bot.send_message(message.chat.id, 'کد هش را اشتباه ارسال کردید  لطفا مجدادا از کلید های پایین استفاده کنید ')
#     else:
#         bot.send_message(message.chat.id, "اندکی صبر کنید")
#
#         def fetch_trx_details(hash1, api_key, target_wallet_address):
#             url = f"https://apilist.tronscan.org/api/transaction-info?hash={hash1}&apikey={api_key}"
#             response = requests.get(url)
#             if response.status_code != 200 or response.json()['toAddress'] != target_wallet_address or response.json()[
#                 'contractRet'] != 'SUCCESS':
#                 return None, None
#             trx_amount = response.json()['contractData']['amount'] / 1_000_000
#
#             url2 = 'https://api.coingecko.com/api/v3/simple/price?ids=tron&vs_currencies=usd'
#             response2 = requests.get(url2)
#             if response2.status_code != 200:
#                 return None, None
#             tron_price = response2.json()['tron']['usd']
#             usdt = tron_price * trx_amount
#             rounded = math.ceil(usdt * 100) / 100
#             return rounded, hash1
#
#         def insert_payment_and_update_wallet(conn, rounded, hash1, message_chat_id):
#             with conn.cursor() as cur:
#                 cur.execute("SELECT EXISTS(SELECT 1 FROM payments WHERE hash_code = %s)", (hash1,))
#                 if cur.fetchone()[0]:
#                     print("hash_code قبلا در دیتابیس موجود است.")
#                     return
#
#                 # اجرای یک کوئری JOIN برای دریافت wallet_id مستقیماً با استفاده از client_code
#                 cur.execute(
#                     "SELECT w.wallet_id FROM wallets w JOIN users u ON u.user_id = w.user_id WHERE u.client_code = %s ",
#                     (message_chat_id,))
#                 wallet_id = cur.fetchone()
#                 if not wallet_id:
#                     print("wallet_id پیدا نشد.")
#                     return
#                 wallet_id = wallet_id[0]
#
#                 # اجرای دستور INSERT
#                 cur.execute("INSERT INTO payments (amount, hash_code, wallet_id) VALUES (%s, %s, %s)",
#                             (rounded, hash1, wallet_id))
#                 # بروزرسانی balance در جدول wallets
#                 cur.execute("UPDATE wallets SET balance = balance + %s WHERE wallet_id = %s",
#                             (rounded, wallet_id))
#             conn.commit()
#             print("Wallet بروزرسانی شد.")
#             bot.send_message(message.chat.id, "Wallet بروزرسانی شد.")
#
#         try:
#             conn = psycopg2.connect(dbname="telegram", user="saeid", password="1111", host="localhost")
#             api_key = "30a1c098-6be5-4561-ad20-06b34d999dce"
#             target_wallet_address = "TApqj7VRYQtt8wXcy22rhont6oECgNqCXQ"
#             rounded, hash1 = fetch_trx_details(hash1, api_key, target_wallet_address)
#             if rounded is not None:
#                 insert_payment_and_update_wallet(conn, rounded, hash1, message.chat.id)
#             else:
#                 bot.send_message(message.chat.id, "بنظر میاد یک چیز درست نیست")
#         finally:
#             conn.close()
#
#
# import psycopg2
#
#
# def show_user_wallet_balance(user_id):
#     try:
#         # ایجاد اتصال به دیتابیس
#         conn = psycopg2.connect(dbname="telegram", user="saeid", password="1111", host="localhost")
#         cur = conn.cursor()
#
#         # پیدا کردن wallet_id با استفاده از user_id
#         cur.execute("SELECT wallet_id FROM wallets WHERE user_id = %s", (user_id,))
#         wallet_id_result = cur.fetchone()
#
#         if wallet_id_result:
#             wallet_id = wallet_id_result[0]
#             # نمایش بالانس ولت
#             cur.execute("SELECT balance FROM wallets WHERE wallet_id = %s", (wallet_id,))
#             balance_result = cur.fetchone()
#
#             if balance_result:
#                 balance = balance_result[0]
#                 return balance
#             else:
#                 print("بالانس برای این ولت پیدا نشد.")
#         else:
#             print("Wallet ID پیدا نشد.")
#     except Exception as e:
#         print(f"خطا در اجرای پرس و جو: {e}")
#     finally:
#         cur.close()
#         conn.close()
#
#
# def find_user_id_from_client_code(client_code):
#     try:
#         conn = psycopg2.connect(dbname="telegram", user="saeid", password="1111", host="localhost")
#         # ایجاد یک کرسر
#         cur = conn.cursor()
#
#         # تعریف کوئری برای یافتن یوزر آیدی بر اساس نام کاربری
#         cur.execute("SELECT user_id FROM users WHERE client_code = %s", (client_code,))
#         user_id = cur.fetchone()
#
#         if user_id:
#             return user_id
#         else:
#             print("User not found")
#         # بستن کرسر و اتصال
#         cur.close()
#         conn.close()
#     except:
#         print("Client code not recorgnized")
#
#
# def buy_payment(user_id):
#     conn = psycopg2.connect(dbname="telegram", user="saeid", password="1111", host="localhost")
#     # ایجاد یک کرسر
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT wallet_id FROM wallets WHERE user_id = %s", (user_id,))
#         wallet_id = cur.fetchone()
#         price_asli = price * -1
#
#         # اجرای دستور INSERT
#         cur.execute("INSERT INTO payments (amount,wallet_id) VALUES (%s,%s)",
#                     (price_asli, wallet_id))
#
#         # بروزرسانی balance در جدول wallets
#         cur.execute("UPDATE wallets SET balance = balance + %s WHERE wallet_id = %s",
#                     (price_asli, wallet_id))
#         conn.commit()
#         return 1
#     except:
#         return 0
#
#
#
#
# bot.infinity_polling(skip_pending=True)
#
# # 7185006139:AAHuDttDr9T8MBPIEscn3wIkld5agDMjE9U
# # bot.answer_callback_query(call.id,"",show alret(true))
