import pymysql.cursors
import pandas.io.sql

connection = pymysql.connect(host='localhost',
                             password='root',
                             user='root',
                             db='Approved',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
    sql = f'SHOW Tables'
    cursor.execute(sql)
    print(cursor.fetchall())
    connection.close()
