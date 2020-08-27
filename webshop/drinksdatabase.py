from flask_mysqldb import MySQL

class Database:
    def __init__(self, flaskApp, isDocker = False, user = "root", password = "1234"):
        self.mysql = MySQL(flaskApp)
        self.can_run = False
        flaskApp.config['MYSQL_USER'] = user
        flaskApp.config['MYSQL_PASSWORD'] = password
        flaskApp.config['MYSQL_DB'] = 'WebshopEasy'
        if isDocker:
            flaskApp.config['MYSQL_HOST'] = 'db'
        else:
            flaskApp.config['MYSQL_HOST'] = 'localhost'

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
            images = self.__get_images(k[0])
            categories = self.__get_drinks_category(k[0])
            drinks.append(Drink(k[0],k[1],k[2],k[3],k[4],k[5],images,categories))
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
            drinks.append(self.__get_drink(out[0][0]))
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
    def get_all_categories(self, user, password):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT name, description, id from category")
        catergories = []
        out = cursor.fetchall()
        for k in out:
            catergories.append(Category(out[2],out[0], out[1]))
        return catergories
    
    # returns list of categories 
    def __get_categories_of_drink(self, drinkid):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT categoryId from category2item where itemid=%s"
        cursor.execute(sql, (drinkid,))
        out = cursor.fetchall()
        categories = []
        for k in out:
            categories.append(self.__get_category(k[0]))
        return categories
    
    # returns category
    def __get_category(self, categoryid):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT name, description from category where id=%s"
        cursor.execute(sql, (categoryid,))
        out = cursor.fetchall()
        return Category(categoryid, out[0][0],out[0][1])

    # returns drink
    def __get_drink(self, drinkid):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, description, price, alkoholAmount, volume from item where id=%s")
        cursor.execute(sql, (drinkid,))
        out = cursor.fetchall()
        images = self.__get_images(out[0][0])
        categories = self.__get_categories_of_drink(out[0][0])
        return Drink(out[0][0], out[0][1], out[0][2],out[0][3], out[0][4], out[0][5], images, categories)

    # returns list of images (bin)
    def __get_images(self, drinkid): 
        cursor = self.mysql.connection.cursor()
        sql = "SELECT png from image where id=%s"
        cursor.execute(sql, (drinkid,))
        out = cursor.fetchall()
        images = []
        for k in out:
            images.append(out[0][0])
        return images

    # returns orders
    def __get_orders(self, userid, is_cart):
        cursor = self.mysql.connection.cursor()
        sql = "SELECT id from order where userId=%s"
        cursor.execute(sql, (userid,))
        out = cursor.fetchall()
        orderId = out[0][0]

        cursor = self.mysql.connection.cursor()
        sql = "SELECT itemid, count from item2order where orderId=%s"
        cursor.execute(sql, (orderId,))
        out = cursor.fetchall()
        order_items = []
        for k in out:
            drink = self.__get_drink(k[0])
            order_items.append(Order_Item(drink,k[1]))

        return Order(orderId, order_items, userid)

    # returns orders
    def get_cart(self, userid):
        return self.__get_orders(userid, True)
    
    def add_to_cart(self, userid, drink):
        pass

    def add_to_orders(self, userid, drink):
        pass

    # returns orders
    def get_finished_orders(self, userid):
        return self.__get_orders(userid, False)

class Drink:
    def __init__(self, id, name, description, price, alcohol, volume, imagesbin, categories):
        self.name = name
        self.description = description
        self.price = price
        self.alcohol = alcohol
        self.volume = volume
        self.imagesbin = imagesbin
        self.categories = categories

class Category():
    def __init__(self, myid, name, description):
        self.id = myid
        self.name = name
        self.description = description


class Order_Item():
    def __init__(self, item, count):
        self.amount = count
        self.drink = item

class Order():
    def __init__(self, order_id, order_item_list, user_id):
        self.id = order_id
        self.user_id = user_id
        self.order_item_list = order_item_list
