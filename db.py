import psycopg2
from psycopg2._psycopg import connection, cursor


def get_cursor():
    db_info = {
        'host': '130.185.121.250',
        'database': 'irvani',
        'user': 'postgres',
        'password': 'testp4ss'
    }

    conn: connection = psycopg2.connect(db_info)
    cur: cursor = conn.cursor()

    return conn, cur


def update_users(user_id, **kwargs):
    conn, cur = get_cursor()

    updates = ', '.join([f"{key} = %s" for key in list(kwargs.keys())])
    cur.execute(f"UPDATE users SET {updates} WHERE id = %s", tuple(user_id) + tuple(kwargs.values()))
    conn.commit()


def update_invoices(invoice_id, **kwargs):
    conn, cur = get_cursor()

    updates = ', '.join([f"{key} = %s" for key in list(kwargs.keys())])
    cur.execute(f"UPDATE invoices SET {updates} WHERE id = %s", tuple(invoice_id) + tuple(kwargs.values()))
    conn.commit()


def get_new_invoices(day_limit: int, *data):
    conn, cur = get_cursor()

    wanted_data = ", ".join(data) or "*"
    cur.execute(f"SELECT {wanted_data} FROM invoices WHERE created_at < NOW() - INTERVAL '{day_limit}'")
    return [{i[0]: i[1] for i in zip(data, j)} for j in cur.fetchall()]


def get_user(user_id):
    conn, cur = get_cursor()

    cur.execute('SELECT * FROM users WHERE id = %s', tuple(user_id))
    try:
        return cur.fetchone()
    except:
        return


def get_invoice(invoice_id):
    conn, cur = get_cursor()

    cur.execute('SELECT * FROM invoices WHERE id = %s', tuple(invoice_id))
    try:
        return cur.fetchone()
    except:
        return