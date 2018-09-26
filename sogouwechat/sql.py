MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '666'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'spiders'

import pymysql

db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8', port=MYSQL_PORT)
cursor = db.cursor()
sql_query = 'CREATE TABLE articles ( id int(11) NOT NULL, title varchar(255) NOT NULL, content text NOT NULL, date varchar(255) NOT NULL ) DEFAULT CHARSET=utf8;'
try:
    cursor.execute(sql_query)
    cursor.execute('ALTER TABLE articles ADD PRIMARY KEY (id);')
    db.commit()
except Exception as e:
    print(e.args)
    db.rollback()
