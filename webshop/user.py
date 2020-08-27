import drinksdatabase

def logout(session):
    session.pop("userid", None)

def login(username, password, session, db):
    userid = db.is_password_correct(username, password)
    if userid != -1:
        session["userid"] = userid
        return True
    return False

def is_logged_in(session):
    if "userid" in session:
        return True
    return False

def get_userid(db, session):
    if "userid" in session:
        return session["userid"]
    else:
        raise Exception("No userid")
