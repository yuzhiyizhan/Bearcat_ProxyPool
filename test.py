import sqlite3

conn = sqlite3.connect('proxies.db')
c = conn.cursor()
a = c.execute('SELECT proxies FROM proxies')
for i in a:
    print(i)
conn.close()
