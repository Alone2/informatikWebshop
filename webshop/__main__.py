from flask import Flask
from webshop import drinksdatabase
import time
import sys

# import mysql.connector

# wait till database is up
time.sleep(5)

# db = mysql.connector.connect(
#   	host="db",
#   	database="webshop",
#   	user="root",
#   	passwd="1234",
#     auth_plugin='mysql_native_password'
# )


app = Flask(__name__)
app.secret_key = "87zihkjnl"
db = None

@app.route("/")
def hello():
    # cursor = db.cursor()
    # sql = "SELECT password from user where username=%s"
    # cursor.execute(sql, ("lel",))
    # return cursor.fetchall()
    db.begin()
    db.create_user("test2","test")
    out = str(db.is_password_correct("test2","test"))
    db.commit()
    return out

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If using Docker
        if sys.argv[1] == "True":
            db = drinksdatabase.Database(app, True)
            app.run(host="0.0.0.0", port=8080)
            sys.exit()
    db = drinksdatabase.Database(app)
    app.run(host="0.0.0.0", port=8080)
