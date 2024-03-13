import psycopg2

# تنظیمات اتصال به دیتابیس را می‌توانید بر اساس نیاز خود تغییر دهید
DATABASE = "telegram"
USER = "saeid"
PASSWORD = "1233212321321123"
HOST = "49.13.88.213"


def connect_db():
    """
    برقراری اتصال به پایگاه داده و بازگرداندن اتصال.
    """
    return psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)


def save_user_and_create_wallet(client_code, username):
    conn = connect_db()
    cur = conn.cursor()
    # ابتدا بررسی می‌کنیم که آیا کاربر با client_code مشخص قبلا در جدول users وجود دارد
    cur.execute("SELECT user_id FROM users WHERE client_code = %s;", (client_code,))
    user_id = cur.fetchone()
    if not user_id:
        # اگر کاربر وجود ندارد، آن را اضافه می‌کنیم
        cur.execute("INSERT INTO users (client_code, username) VALUES (%s, %s) RETURNING user_id;",
                    (client_code, username))
        user_id = cur.fetchone()[0]  # بازگرداندن user_id برای ایجاد ولت
        # سپس برای او یک ولت ایجاد می‌کنیم
        cur.execute("INSERT INTO wallets (user_id, balance) VALUES (%s, 0);", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


def execute_query(query, data=None):
    """
    اجرای یک کوئری بدون بازگشت داده.
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, data)
            conn.commit()


def execute_query_returning(query, data=None):
    """
    اجرای کوئری و بازگشت یک سطر از نتایج.
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, data)
            return cur.fetchone()


def show_user_wallet_balance(user_id):
    """
    نمایش موجودی کیف پول کاربر با استفاده از user_id.
    """
    query = "SELECT balance FROM wallets WHERE user_id = %s;"
    result = execute_query_returning(query, (user_id,))
    if result:
        return result[0]
    else:
        return None


def find_user_id_from_client_code(client_code):
    """
    یافتن user_id با استفاده از client_code.
    """
    query = "SELECT user_id FROM users WHERE client_code = %s;"
    result = execute_query_returning(query, (client_code,))
    if result:
        return result[0]
    else:
        print("User not found")
        return None


def buy_payment(user_id, amount):
    """
    بروزرسانی موجودی کیف پول کاربر پس از خرید.
    """
    conn = None
    try:
        conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
        cur = conn.cursor()
        cur.execute("SELECT wallet_id FROM wallets WHERE user_id = %s", (user_id,))
        wallet_id = cur.fetchone()

        cur.execute("SELECT balance FROM wallets WHERE wallet_id = %s", (wallet_id,))
        if cur.fetchone() is None:
            print("Wallet ID not found.")
            return False
        # کسر مبلغ از موجودی کیف پول
        cur.execute("UPDATE wallets SET balance = balance - %s WHERE user_id = %s", (amount, user_id))

        # ثبت پرداخت در جدول payments
        cur.execute("INSERT INTO payments (wallet_id, amount) VALUES (%s, %s)", (wallet_id, -amount))

        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error in buy_payment: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
