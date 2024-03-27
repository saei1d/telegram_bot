from main import bot
from database import *
admin_pro = [366470485, 6696631466]

def handle_admin_settings(message):
    if message.from_user.id in admin_pro:
        bot.send_message(message.chat.id, 'Admin delete settings menu.')
        msg = bot.send_message(message.chat.id, "client_code ra vared konid baraye delete")
        bot.register_next_step_handler(msg, search_client_code_for_delete)

    else:
        bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')

def search_client_code_for_delete(message):
    deleted_client = message.text
    print("mnbgvfdfghj")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET deleted = TRUE WHERE client_code = %s", (deleted_client,))
    conn.commit()
    bot.send_message(message.chat.id,"کاربر شما تماما محدود شد")




# @bot.message_handler(commands=['admin/undelete'])
# def handle_admin_settings(message):
#     if message.from_user.id in admin_pro:
#         bot.send_message(message.chat.id, 'Admin undelete settings menu.')
#         msg = bot.send_message(message.chat.id, "client_code ra vared konid baraye undelete")
#         bot.register_next_step_handler(msg, search_client_code_for_undelete)
#
#     else:
#         bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')
#
# def search_client_code_for_undelete(message):
#     deleted_client = message.text
#     conn = connect_db()
#     cur = conn.cursor()
#     cur.execute("UPDATE users SET deleted = FALSE WHERE client_code = %s", (deleted_client,))
#     conn.commit()
#     bot.send_message(message.chat.id,"کاربر شما تماما رفع محدودیت شد")
#
# @bot.message_handler(commands=['admin'])
# def handle_admin_settings(message):
#     if message.from_user.id in admin_pro:
#         bot.send_message(message.chat.id, 'Admin settings menu.')
#         msg = bot.send_message(message.chat.id, "client_code ra vared konid")
#         bot.register_next_step_handler(msg, search_client_code)
#
#     else:
#         bot.send_message(message.chat.id, 'از دکمه های اماده زیر استفاده کنید لطفا')
#
#
# def search_client_code(message):
#     client_searched = str(message.text)
#     conn = connect_db()
#     cur = conn.cursor()
#     cur.execute("SELECT user_id,join_by_code,referral_code,phone_number,email  FROM users WHERE client_code =%s",
#                 (client_searched,))
#     user = cur.fetchone()
#     user_id = user[0]
#
#     cur.execute("SELECT balance,all_buy  FROM wallets WHERE user_id =%s",
#                 (user_id,))
#     wallet = cur.fetchone()
#     if user:
#         balance = wallet[0]
#         all_buy = wallet[1]
#         join_by_code = user[1]
#         referral_code = user[2]
#         phone_number = user[3]
#         email = user[4]
#         user_configss = show_configs(client_searched)
#         print(user_configss(client_searched))
#         for mmd in user_configss:
#             bot.send_message(message.chat.id, mmd)
#         bot.send_message(message.chat.id,
#                          f' یوزر آیدی{user_id},دعوت شده توسط {join_by_code} کد رفرال {referral_code} شماره موبایل{phone_number}و ایمیل {email} و کیف پول این شخص در حال حاضر مقدار {balance} و در کل به مقدار {all_buy} ترون شارژ شده است')
#     else:
#         bot.send_message(message.chat.id, "karbar shenasaei nashod")
#
