# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 11:04:42 2020

@author: mario, pietro
"""

### MODULES

import os, configparser
import mysql.connector

### SETTINGS

MODULE_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
SW_DIR=os.path.dirname(MODULE_DIR)
config = configparser.ConfigParser()
config.read('config.ini')

### CONSTANTS

HOST=config['USERS_DATABASE']['HOST']
USER=config['USERS_DATABASE']['USER']
PASSWORD=config['USERS_DATABASE']['PASSWORD']
DATABASE=config['USERS_DATABASE']['DATABASE']

### DEFs

def show_databases():
    # Show availale databases
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    print('Databases available: ')
    for x in mycursor:
      print(x)
    mycursor.close()

def get_users():
    # Reutrn a touple (chat_id, reg_date, username, f_name)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    mycursor.close()
    return myresult

def show_users():
    # print the users in the table
    myresult=get_users()
    print('Printing all users ...')
    for x in myresult:
      print('   > ',x)

def create_table_for_users():
    # Create the covid table
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, chat_id VARCHAR(255), reg_date VARCHAR(255), username VARCHAR(255), f_name VARCHAR(255), l_name VARCHAR(255))")
    mycursor.execute("SHOW TABLES")
    print('Tables available: ')
    for x in mycursor:
      print(x)
    mycursor.close()

def add_user(chat_id,reg_date,username,f_name,l_name):
    # Insert the table
    sql = "INSERT INTO users (chat_id, reg_date, username, f_name, l_name) VALUES (%s, %s,%s,%s,%s)"
    val = (chat_id, reg_date,username,f_name,l_name)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    print('   > ',mycursor.rowcount, "record inserted.")
    mycursor.close()

def execute(sql):
    # execute MySQL command-string
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()

def test_1():
    """
    This methods to initialize a new database and show easy handles for the
    connector.
    """

    # Initialization
    show_databases()
    create_table_for_users()

    # Print last id
    mycursor = mydb.cursor()
    print("Last row id:", mycursor.lastrowid)

    # Add new user '111222333'
    add_user('111222333','2020-12-31','gio','mario','cil')

    # Print table with users
    show_users()

    # Delete by chat_id user '111222333'
    sql = "DELETE FROM users WHERE chat_id = '111222333'"
    execute(sql)
    show_users()

    # Close connector
    mydb.close()

### CLASS

class UsersDatabase:

    def get_user(chat_id):
        MYDB = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        mycursor = MYDB.cursor()
        mycursor.execute("SELECT * FROM users WHERE chat_id = " + chat_id)
        myresult = mycursor.fetchall()
        for user in myresult:
            user_dict={}
            user_dict['chat_id']=int(user[1])
            user_dict['reg_date']=user[2]
            user_dict['username']=user[3]
            user_dict['f_name']=user[4]
            user_dict['l_name']=user[5]
        mycursor.close()
        MYDB.close()
        return user_dict

    def get_user_str(chat_id):
        MYDB = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        mycursor = MYDB.cursor()
        mycursor.execute("SELECT * FROM users WHERE chat_id = " + str(chat_id))
        myresult = mycursor.fetchall()

        if len(myresult)>0:
            for user in myresult:
                user_dict={}
                user_dict['chat_id']=str(user[1])
                user_dict['reg_date']=user[2]
                user_dict['username']=user[3]
                user_dict['f_name']=user[4]
                user_dict['l_name']=user[5]

            user_str=user_dict['chat_id']
            if user_dict['username']:
                user_str=user_dict['username']+' ('+user_dict['chat_id']+')'
            if user_dict['f_name']:
                user_str=user_dict['f_name']+' ('+user_dict['chat_id']+')'
            if user_dict['f_name'] and user_dict['username']:
                user_str=user_dict['username']+' ('+user_dict['f_name']+', '+user_dict['chat_id']+')'
            if user_dict['f_name'] and user_dict['l_name']:
                user_str=user_dict['f_name']+' '+user_dict['l_name']
            if user_dict['f_name'] and user_dict['l_name'] and user_dict['username']:
                user_str=user_dict['username']+' ('+user_dict['f_name']+' '+user_dict['l_name']+')'
        else:
            user_str=str(chat_id)

        mycursor.close()
        MYDB.close()
        return user_str

    def get_users():
        MYDB = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        mycursor = MYDB.cursor()
        mycursor.execute("SELECT * FROM users")
        myresult = mycursor.fetchall()
        users=[]
        for user in myresult:
            user_dict={}
            user_dict['chat_id']=int(user[1])
            user_dict['reg_date']=user[2]
            user_dict['username']=user[3]
            user_dict['f_name']=user[4]
            user_dict['l_name']=user[5]
            users.append(user_dict)
        mycursor.close()
        MYDB.close()
        return users

    def add_user(chat_id,reg_date,username,f_name,l_name):
        MYDB = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        sql = "INSERT INTO users (chat_id, reg_date, username, f_name, l_name) VALUES (%s, %s,%s,%s,%s)"
        val = (chat_id, reg_date,username,f_name,l_name)
        mycursor = MYDB.cursor()
        mycursor.execute(sql, val)
        MYDB.commit()
        print('   > ',mycursor.rowcount, "record inserted.")
        mycursor.close()
        MYDB.close()

    def execute(sql):
        MYDB = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        mycursor = MYDB.cursor()
        mycursor.execute(sql)
        MYDB.commit()
        mycursor.close()
        MYDB.close()

### MAIN

if __name__=='__main__':

    # Database
    mydb = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
        )

    # test_1()
