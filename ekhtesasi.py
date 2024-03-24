

from main import bot


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
