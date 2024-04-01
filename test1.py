import sqlite3

def data_fetch():

    conn = sqlite3.connect('messages.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM messages_received ORDER BY id DESC LIMIT 1')

    recent_row = cursor.fetchone()

    print('last row', recent_row)

    cursor.close()
    conn.close()
    print(recent_row)


data_fetch()