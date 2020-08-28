from flask_mysqldb import MySQL

class Database:
    def __init__(self, flaskApp, isDocker = False, user = "root", password = "1234"):
        self.can_run = False
        flaskApp.config['MYSQL_USER'] = user
        flaskApp.config['MYSQL_PASSWORD'] = password
        flaskApp.config['MYSQL_DB'] = 'WebshopEasy'
        if isDocker:
            flaskApp.config['MYSQL_HOST'] = 'db'
        else:
            flaskApp.config['MYSQL_HOST'] = 'localhost'
        self.mysql = MySQL(flaskApp)
    
    def can_connect(self):
        if self.mysql.connection == None:
            return False
        return True

    def begin(self):
        self.mysql.connection.begin()
        self.can_run = True

    def commit(self):
        self.mysql.connection.commit()
        self.can_run = False
    
    def revert(self):
        self.mysql.connection.revert()
        self.can_run = False

    # returns list of Drinks 
    # TODO: implement search (.. where)
    def get_drinks_search(self, searchterm):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, description, price, alkoholAmount, volume from item")
        drinks = []
        out = cursor.fetchall()
        for k in out:
            categories = self.__get_drinks_category(k[0])
            drinks.append(Drink(k[0],k[1],k[2],k[3],k[4],k[5],categories))
        return drinks


    # returns list of Drinks | category is of class category
    def get_drinks_by_category(self, category):
        catecor_id = category.id
        cursor = self.mysql.connection.cursor()
        sql = "SELECT itemId from category2item where categoryId=%s"
        cursor.execute(sql, (catecor_id,))
        out = cursor.fetchall()
        drinks = []
        for k in out:
            drinks.append(self.get_drink(out[0][0]))
        return drinks

    # returns User Id, or -1
    def is_password_correct(self, user, password):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT password, id from user where username=%s"
        cursor.execute(sql, (user,))
        out = cursor.fetchall()
        if len(out) < 1:
            return -1
        passw = out[0][0]
        uid = out[0][1]
        # No encryption 'cause we like to live dangerously!
        if password == passw:
            return uid
        else:
            return -1

    # returns nothing
    def create_user(self, user, password):
        if not self.can_run:
            raise Exception("Start Database with .begin()")
        if len(user) < 3 or len(password) < 3:
            raise Exception("Username or password too short")
        if self.does_user_exist(user):
            raise Exception("User does already exist")
        cursor = self.mysql.connection.cursor()
        sql = "INSERT into user (username, password) VALUES (%s, %s) "
        cursor.execute(sql, (user,password))

    # returns bool
    def does_user_exist(self, user):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT id from user where username = %s"
        cursor.execute(sql, (user,))
        out = cursor.fetchall()
        if len(out) > 1:
            return True
        return False
    
    # returns nothing
    def change_password(self, user, password):
        if not self.can_run:
            raise Exception("Start Database with .begin()")
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE user SET password = %s WHERE username = %s"
        cursor.execute(sql, (password,user))

    # returns list of categories 
    def get_all_categories(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT name, description, id from category")
        catergories = []
        out = cursor.fetchall()
        for k in out:
            catergories.append(Category(k[2], k[0], k[1]))
        return catergories
    
    # returns list of categories 
    def __get_categories_of_drink(self, drinkid):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT categoryId from category2item where itemid=%s"
        cursor.execute(sql, (drinkid,))
        out = cursor.fetchall()
        categories = []
        for k in out:
            categories.append(self.get_category(k[0]))
        return categories
    
    # returns category
    def get_category(self, categoryid):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT name, description from category where id=%s"
        cursor.execute(sql, (categoryid,))
        out = cursor.fetchall()
        return Category(categoryid, out[0][0],out[0][1])

    # returns drink
    def get_drink(self, drinkid):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT id, name, description, price, alkoholAmount, volume from item where id=%s"
        cursor.execute(sql, (drinkid,))
        out = cursor.fetchall()
        categories = self.__get_categories_of_drink(out[0][0])
        return Drink(out[0][0], out[0][1], out[0][2],out[0][3], out[0][4], out[0][5], categories)

    # returns list of images (bin)
    def get_images(self, drink): 
        cursor = self.mysql.connection.cursor()
        sql = "SELECT png from image where id=%s"
        cursor.execute(sql, (drink.id,))
        out = cursor.fetchall()
        images = []
        for k in out:
            images.append(out[0][0])
        return images

    # returns orders
    def __get_orders(self, userid):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT id, isPlaced from order where userId=%s"
        cursor.execute(sql, (userid,))
        out = cursor.fetchall()

        orders = []
        for k in out:
            orderId = k[0]
            is_placed = k[1]

            cursor = self.mysql.connection.cursor()
            sql = "SELECT itemid, count from item2order where orderId=%s"
            cursor.execute(sql, (orderId,))
            out2 = cursor.fetchall()
            order_items = []
            for o in out2:
                drink = self.get_drink(o[0])
                order_items.append(Order_Item(drink,o[1]))

            orders.append(Order(orderId, order_items, userid, is_placed))
        return orders

    # returns orders
    def get_cart(self, userid):
        orders = self.__get_orders(userid)
        if not orders[-1].is_placed:
            return orders[-1]
        raise Exception("Cart not found")

    # doesn't return anything (amount kann auch negativ sein)
    def add_to_cart(self, userid, drink, amount=1):
        if not self.can_run:
            raise Exception("Start Database with .begin()")
        warenkorb = None
        try:
            warenkorb = self.get_cart.id
        except:
            warenkorb = self.__create_cart(userid)
        self.__update_count_cart_item(warenkorb.id, drink.id, amount)
    
    # doesn't return anything 
    def __update_count_cart_item(self, orderid, itemid, update_add):
        if not self.can_run:
            raise Exception("Start Database with .begin()")
        cursor = self.mysql.connection.cursor()
        sql = "SELECT count from item2order WHERE itemId = %s AND orderId = %s"
        cursor.execute(sql, (itemid,orderid))
        out = cursor.fetchall()
        if len(out) == 0:
            # item doesn't exist in item2order
            if update_add <= 0:
                return
            sql = "INSERT into item2order (itemId, orderId, count) VALUES (%s, %s, %s) "
            cursor.execute(sql, (itemid,orderid, update_add))
        else:
            # item exists in item2order
            count = out[0][0]
            if count > 0:
                sql = "UPDATE item2order SET count = %s WHERE itemId = %s and orderId = %s"
                cursor.execute(sql, (count + update_add, itemid, orderid))
            else:
                sql = "DELETE FROM item2order WHERE itemId = %s and orderId = %s"
                cursor.execute(sql, (itemid,orderid))
    
    # returns nothing raises exception
    def remove_from_cart(self, userid, drink, amount = 1):
        return self.add_to_cart(userid, drink, -amount)
    
    # returns cart (order)
    def __create_cart(self, userid):
        if not self.can_run:
            raise Exception("Start Database with .begin()")
        cursor = self.mysql.connection.cursor()
        sql = "INSERT into order (userId, isPlaced) VALUES (%s, %s) "
        cursor.execute(sql, (userid, False))
    
    # returns nothing
    def buy_cart(self, userid):
        if not self.can_run:
            raise Exception("Start Database with .begin()")
        cart = self.get_cart(userid)
        cursor = self.mysql.connection.cursor()
        sql = "UPDATE order SET isPlaced = %s WHERE id = %s "
        cursor.execute(sql, (True, cart.id))
        self.__create_cart()

    # returns orders
    def get_finished_orders(self, userid):
        orders = self.__get_orders(userid)
        if orders[-1].is_placed:
            return orders
        return orders[:-1]

class Drink:
    def __init__(self, myid, name, description, price, alcohol, volume, categories):
        self.id = int(myid)
        self.name = str(name)
        self.description = str(description)
        self.price = float(price)
        self.alcohol = float(alcohol)
        self.volume = float(volume)
        self.categories = categories

class Category():
    def __init__(self, myid, name, description):
        self.id = int(myid)
        self.name = str(name)
        self.description = str(description)

class Order_Item():
    def __init__(self, item, count):
        self.amount = int(count)
        self.drink = item

class Order():
    def __init__(self, order_id, order_item_list, user_id, is_placed):
        self.id = int(order_id)
        self.user_id = int(user_id)
        self.order_item_list = order_item_list
        self.is_placed = bool(is_placed)
