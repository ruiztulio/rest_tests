import psycopg2
import psycopg2.extras
import random
from datetime import (timedelta, date)

pg_user = "testrest"
pg_pass = "123"
pg_host ="localhost"
pg_dbname ="rest_sales"
pg_port =5432

conn = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                    (pg_host, pg_dbname, pg_pass, pg_user, pg_port))
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

start_date = date(2012, 1, 1)
day = timedelta(days = 1)

for i in xrange(0, 100):
    cur.execute("insert into products (name, quantity, code, price) values(%s, %s, %s, %s)",
                ("producto %s"%i, random.randint(1, 50), str(random.randint(100, 1000)), 2000*random.random()))
conn.commit()
print "Se agregaron los productos..."

for i in xrange(0, 30):
    cur.execute("insert into clients (name, address, phone, vat) values(%s, %s, %s, %s)",
                ("Cliente %s"%i, "Direccion %s"%i, str(random.randint(20000, 100000)), str(random.randint(10000000, 100000000))))
conn.commit()
print "Se agregaron los clientes..."

cur.execute("select id from clients")
all_clients = cur.fetchall()
cur.execute("select id from products")
all_products = cur.fetchall()
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

for i in xrange(0, 400):
    client = all_clients[random.randint(0, len(all_clients)-1)]
    sale_id = cur.execute("insert into sales (client_id, sale_date) values(%s, %s) returning id",
                (client[0], start_date, ))
    sale_id = cur.fetchone()[0]
    print "Generando venta ", sale_id
    n_products = random.randint(1, 30)
    for j in xrange(n_products):
        product_id = all_products[random.randint(0, len(all_products)-1)][0]
        cur.execute("insert into sales_lines (sale_id, product_id, quantity) values(%s, %s, %s)",
                    (sale_id, product_id, random.randint(1, 10)))
    conn.commit()
    if random.randint(0, 20) > 10:
        start_date = start_date + day
conn.commit()
print "Todas las ventas generadas."
