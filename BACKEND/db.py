import MySQLdb


def connect_db():
    return MySQLdb.connect(host='localhost', user='root', database='school', password='Jeeban@12345')