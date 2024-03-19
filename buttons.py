from telebot import types


def get_main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("خرید اشتراک"),
        types.KeyboardButton("کیف پول"),
        types.KeyboardButton("آموزش استفاده"),
        types.KeyboardButton("پشتیبانی"),
        types.KeyboardButton("اشتراک های من"),
        types.KeyboardButton(" قیمت لحظه ای ترون"),
        types.KeyboardButton("عودت وجه"),
        types.KeyboardButton("درامدزایی"),
        types.KeyboardButton("تست یکروزه"),
    ]
    markup.add(*buttons)
    return markup


def get_tariff_buttons():
    """
    ایجاد و بازگرداندن کیبورد اینلاین برای تعرفه‌ها.
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("یک ماهه دو کاربره ۱۰۰ گیگ (1 دلار)", callback_data="tarefe30gig"),
        types.InlineKeyboardButton("یک ماهه دو کاربره ۱۵۰ گیگ (1.5 دلار)", callback_data="tarefe50gig"),
        types.InlineKeyboardButton("سه ماهه دو کاربره ۱۵۰ گیگ (2 دلار)", callback_data="tarefe70gig"),
        types.InlineKeyboardButton("سه ماهه دو کاربره ۱۵۰ گیگ (2 دلار)", callback_data="tarefe90gig"),
        types.InlineKeyboardButton("تعرفه اختصاصی (ساخت دلخواه) ", callback_data="tarefeEkhtesasi")
    ]
    markup.add(*buttons)
    return markup


def get_support_buttons():
    """
    ایجاد و بازگرداندن کیبورد اینلاین برای بخش پشتیبانی.
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("پشتیبانی در اسرع وقت", callback_data="support"),
        types.InlineKeyboardButton("سوالات متداول", callback_data="faq")
    ]
    markup.add(*buttons)
    return markup


def get_money():
    markup = types.InlineKeyboardMarkup()
    recharge_button = types.InlineKeyboardButton("شارژ کیف پول", callback_data="sharzh")
    markup.add(recharge_button)


def get_wallet_recharge_buttons():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("شارژ از ولت شخصی ترون (TRC20)", callback_data="sharzh"),
        types.InlineKeyboardButton("خریدترون از ما (پیشنهادی)", callback_data="kharid_azma"),
    ]
    markup.add(*buttons)
    return markup


def amozesh_kharid_tron_az_ma():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("آموزش خریدترون از ما", callback_data="amozesh_kharid_azma"),
    ]
    markup.add(*buttons)
    return markup


def get_education_buttons():
    """
    ایجاد و بازگرداندن کیبورد ساده برای انتخاب آموزش‌ها.
    """
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("آموزش شارژ کیف پول ترون", callback_data="ARZ"),
        types.InlineKeyboardButton("آموزش استفاده از کانفیگ ها", callback_data="Dastgah"),

    ]
    markup.add(*buttons)
    return markup


def get_education_platform_buttons():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("اندروید", callback_data="AMOZESH_android"),
        types.InlineKeyboardButton("iOS", callback_data="AMOZESH_ios"),
        types.InlineKeyboardButton("Windows", callback_data="AMOZESH_windows"),
        types.InlineKeyboardButton("Mac", callback_data="AMOZESH_mac")
    ]
    markup.add(*buttons)
    return markup
