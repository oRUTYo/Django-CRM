import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root',
    auth_plugin='mysql_native_password'
)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE dcrmproject")

print('Работает.')
