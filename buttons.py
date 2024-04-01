from telebot import types


def get_main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("خرید اشتراک🛍"),
        types.KeyboardButton("داشبورد جیمبو 🖥"),
        types.KeyboardButton("اکانت تستی رایگان🔥"),
        types.KeyboardButton("عودت وجه❌"),
        types.KeyboardButton("آموزش استفاده💿📖"),
        types.KeyboardButton("پشتیبانی👥"),
        types.KeyboardButton("اشتراک های من🔋"),
        types.KeyboardButton("قیمت لحظه ای ترون🌐"),
        types.KeyboardButton("درآمدزایی⚡💵"),

    ]
    markup.add(*buttons)
    return markup


def button_validate():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.KeyboardButton("ارسال شماره", request_contact=True),
        types.KeyboardButton("ارسال ایمیل "),
        types.KeyboardButton("برگشت"),
    ]
    markup.add(*buttons)
    return markup


def get_back_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.KeyboardButton("برگشت"),

    ]
    markup.add(*buttons)
    return markup


def get_tariff_buttons():
    """
    ایجاد و بازگرداندن کیبورد اینلاین برای تعرفه‌ها.
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("دوکاربره ۳۰ گیگ ۴۰ روزه ۱۱ ترون (۷۲ هزارتومان)", callback_data="tarefe30gig"),
        types.InlineKeyboardButton("دوکاربره ۵۰ گیگ۴۰  روزه ۱۷ ترون  (۱۱۳ هزار تومان)", callback_data="tarefe50gig"),
        types.InlineKeyboardButton("دوکاربره ۷۰ گیگ ۴۰ روزه ۲۲ ترون  (۱۴۸ هزار تومان)", callback_data="tarefe70gig"),
        types.InlineKeyboardButton("دوکاربره ۹۰ گیگ ۴۰ روزه ۲۷ ترون  (۱۸۹ هزارتومان)", callback_data="tarefe90gig"),
        types.InlineKeyboardButton("دوکاربره ۱۲۰ گیگ ۴۰ روزه ۳۱ ترون  (۲۱۷ هزار تومان)", callback_data="tarefe120gig"),
        types.InlineKeyboardButton("تعرفه اختصاصی (ساخت دلخواه) ", callback_data="Ekhtesasi")
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
    recharge_button = types.InlineKeyboardButton("شارژ داشبورد جیمبو", callback_data="sharzh")
    markup.add(recharge_button)


def get_wallet_recharge_buttons():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("از ولت خودت داشبورد جیمبو رو شارژ کن (TRC20)", callback_data="sharzh"),
        types.InlineKeyboardButton("از ما بخر ترون و داشبورتو شارژ کن(پیشنهادی)", callback_data="kharid_azma"),
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
        types.InlineKeyboardButton("آموزش شارژ داشبورد جیمبو ترون", callback_data="ARZ"),
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
        # types.InlineKeyboardButton("Mac", callback_data="AMOZESH_mac")
    ]
    markup.add(*buttons)
    return markup


def ekhtesasiii():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("شروع ساخت", callback_data="make_config"),

    ]
    markup.add(*buttons)
    return markup


def discount():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("کد تخفیف داری ؟", callback_data="discount"),
        types.InlineKeyboardButton("ادامه خرید", callback_data="edame_kharid"),

    ]
    markup.add(*buttons)
    return markup


def edame():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("ادامه فرایند خرید", callback_data="edame_kharid"),

    ]
    markup.add(*buttons)
    return markup


def tarefe_ekhtesai_buy():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("خرید این تعرفه", callback_data="EEEE"),
        types.InlineKeyboardButton("اصلاح ", callback_data="make_config"),

    ]
    markup.add(*buttons)
    return markup


def tarefe_ekhtesai_agent():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("خرید این تعرفه", callback_data="EEEE2"),

    ]
    markup.add(*buttons)
    return markup



def qr():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("گرفتن تصویر qr", callback_data="qqq"),

    ]
    markup.add(*buttons)
    return markup