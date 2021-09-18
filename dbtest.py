
#Lien BDD
from Data.database_handler import DatabaseHandler

database_handler = DatabaseHandler("database.db")

def register():
    print("---Register---")
    username = input("Username : ")
    password = input("Password :")

    database_handler.create_person(username, password)

def login():
    print("---Login---")
    username = input("Username : ")
    password = input("Password :")

    if database_handler.user_exists_with(username) and password == database_handler.password_for(username):
        menu_connected()
    else:
        print("not logged in")

def menu_not_connected():
    while True:
        print("hello")
        login()
        return

def menu_connected():
    while True:
        print("Successfully Connected")
        return

menu_not_connected()