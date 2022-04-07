import MySQLdb.cursors
import MySQLdb
from main import mysql

def fetchUserexists(username, password):
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applogin.accounts WHERE username = %s AND password = %s', (username, password,))
    # Fetch one record and return result
    account = cursor.fetchone()
    cursor.close()
    return account

def fetchInsertUser(username, password, email, folder_name):
    # Account doesnt exists and the form data is valid, now insert new account into applogin.accounts table
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO applogin.accounts VALUES (NULL,\'user\',%s, %s, %s, %s)', (username, password, email, folder_name,))
    mysql.connection.commit()

def fetchUserId(sessionid):
    # We need all the account info for the user so we can display it on the profile page
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applogin.accounts WHERE id = %s', (sessionid,))
    account = cursor.fetchone()
    cursor.close()
    return account

def fetchFolderName(id, username):
    # We need all the account info for the user so we can display it on the profile page
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applogin.accounts WHERE id = %s AND username = %s', (id, username,))
    account = cursor.fetchone()
    return account

def fetchListUser():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applogin.accounts')
    users = cursor.fetchone()
    return users

def fetchCountUsers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(*) FROM applogin.accounts')
    users = cursor.fetchone()
    return users

def fetchCheckUser(id, username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applogin.accounts WHERE id = %s AND username = %s', (id, username,))
    account = cursor.fetchone()
    return account

def fetchUsernames():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT username FROM applogin.accounts')
    users = cursor.fetchone()
    return users