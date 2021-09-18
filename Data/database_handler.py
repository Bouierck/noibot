import os 
import sqlite3

class DatabaseHandler():
    def __init__(self, database_name : str):
        self.con= sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row 


    def create_person(self, username : str, password : str):
        cursor = self.con.cursor()
        query = f"INSERT INTO access (username,password) VALUES ('{username}', '{password}');"
        cursor.execute(query)
        cursor.close()
        self.con.commit()

    def password_for(self, username : str) -> str:
        cursor = self.con.cursor()
        query = f"SELECT password FROM access WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0])["password"]

    def user_exists_with(self, username: str) -> bool:
        cursor = self.con.cursor()
        query = f"SELECT password FROM access WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        cursor.close()
        return len(result)==1


    def stock_increment(self, nom_element: str, quantite: int, boutique: str, date: str):
        cursor = self.con.cursor()
        query = f"INSERT INTO stock (nom_element,quantite,boutique,date) VALUES ('{nom_element}', '{quantite}','{boutique}', '{date}');"
        cursor.execute(query)
        cursor.close()
        self.con.commit()

    def stock_show(self):
        i = 0
        cursor = self.con.cursor()
        query = f"SELECT id_stock,nom_element,quantite,boutique,date FROM stock WHERE id_stock is not null;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        while(i < len(result)):
            print(dict(result[i])["nom_element"])
            print(dict(result[i])["quantite"])
            print(dict(result[i])["boutique"])
            print(dict(result[i])["date"])
            
            i=i+1
        return result

    def stock_delete(self, id_stock: int):
        cursor = self.con.cursor()
        query = f"DELETE FROM stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock))
        cursor.close()
        self.con.commit()
        print("Article Supprimé!")

    def get_url_from_table(self):
        cursor = self.con.cursor()
        query = f"SELECT url from url_link;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0])["url"]

    def modify_url(self, url):
        cursor = self.con.cursor()
        query = f"UPDATE url_link set url = ?;"
        cursor.execute(query, (url,))
        cursor.close()
        self.con.commit()
        print("Successfully updated\n")

    def in_reserv(self, id_stock):
        cursor = self.con.cursor()
        query = f"SELECT quantite_resa from reservation where id_stock = ?;"
        cursor.execute(query, (id_stock,))
        result = cursor.fetchall()
        cursor.close()
        if(dict(result[0])["quantite_resa"] > 0):
            return 1
        else:
            print("\nOut of Stock\n")
            return 0
            
    def id_stock_to_id_resa(self, id_stock):
        cursor = self.con.cursor()
        query = f"SELECT id_resa from reservation where id_stock = ?;"
        cursor.execute(query, (id_stock,))
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0])["id_resa"]

    def get_reserv(self, id_stock):
        cursor = self.con.cursor()
        query = f"UPDATE reservation SET quantite_resa = quantite_resa - 1 WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        result = cursor.fetchall()
        cursor.close()
        self.con.commit()
        print("Objet Reservé!")
        return 1

    def get_name_from_id_stock(self, id_stock):
        cursor = self.con.cursor()
        query = f"SELECT nom_element FROM stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        name_id = cursor.fetchall()
        cursor.close()
        return dict(name_id[0])["nom_element"]


    def get_name_from_id_resa(self, id_resa):
        cursor = self.con.cursor()
        query = f"SELECT nom_element FROM stock WHERE id_stock = (SELECT id_stock FROM reservation WHERE id_resa =?);"
        cursor.execute(query, (id_resa,))
        name_id = cursor.fetchall()
        cursor.close()
        return dict(name_id[0])["nom_element"]


    def reservation_increment(self, id_stock, quantite ):
        cursor = self.con.cursor()
        query = f"INSERT INTO reservation (quantite_resa,id_stock) VALUES ('{quantite}','{id_stock}');"
        cursor.execute(query)
        cursor.close()
        self.con.commit()
        print("Ajout d'une Reservation pour l'article : " + id_stock)

    def stock_exists(self, id_stock):
        cursor = self.con.cursor()
        query = f"SELECT nom_element FROM stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        result = cursor.fetchall()
        cursor.close()
        if(dict(result[0])["nom_element"] != ""):
            return 1
        else:
            return 0

    def reservation_show(self):
        i = 0
        cursor = self.con.cursor()
        query = f"SELECT id_resa,quantite_resa,id_stock FROM reservation WHERE id_resa is not null;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        while(i < len(result)):
            print(dict(result[i])["id_resa"])
            print(dict(result[i])["quantite_resa"])
            print(dict(result[i])["id_stock"])
            
            i=i+1
        return result

    def liste_reservation_show(self):
        i = 0
        cursor = self.con.cursor()
        query = f"SELECT id_lresa,user,quantite,id_resa FROM liste_resa WHERE id_lresa is not null;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        while(i < len(result)):
            print(dict(result[i])["id_resa"])
            print(dict(result[i])["quantite"])
            
            i=i+1
        return result



    def ajout_liste_reservation(self, user, id_resa: int, quantite: int):
        cursor = self.con.cursor()
        query = f"SELECT user,id_resa FROM liste_resa WHERE id_lresa is not null;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        if(bool(result) == True):
            if( str(dict(result[0])["user"]) == str(user) and str(dict(result[0])["id_resa"]) == str(id_resa)):
                cursor = self.con.cursor()
                query = f"UPDATE liste_resa SET quantite = quantite + ? WHERE id_resa = ? and user = ?;"
                cursor.execute(query, (quantite,id_resa,user))
                cursor.close()
                self.con.commit()
                print("Mis à jour d'une Reservation pour le user : " + str(user) + "de l'item : " + str(id_resa))
            else: 
                cursor = self.con.cursor()
                query = f"INSERT INTO liste_resa (user,quantite,id_resa) VALUES ('{user}','{quantite}','{id_resa}');"
                cursor.execute(query)
                cursor.close()
                self.con.commit()
                print("Ajout d'une Reservation pour le user : " + str(user) + "de l'item : " + str(id_resa))
        if(bool(result) == False):
                cursor = self.con.cursor()
                query = f"INSERT INTO liste_resa (user,quantite,id_resa) VALUES ('{user}','{quantite}','{id_resa}');"
                cursor.execute(query)
                cursor.close()
                self.con.commit()
                print("Ajout d'une Reservation pour le user : " + str(user) + "de l'item : " + str(id_resa))






