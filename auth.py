
import sqlite3
import bcrypt

def register_user(name,email,password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute(
        "Select email from users where email=?",
        (email,)
    )
    existing_user = cursor.fetchone()
    if existing_user:
        connection.close()
        return False
    else:
        hashed_pass=bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )  
        cursor.execute(
            "INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",
            (name,email,hashed_pass.decode("utf-8"))
        ) 
        connection.commit()
    connection.close() 
    return True
def login_user(email, password):
    user_id = None
    connection=sqlite3.connect("users.db") 
    cursor = connection.cursor()
    cursor.execute(
        "Select user_id,password_hash from users where email =?",
        (email,)
    ) 
    user = cursor.fetchone()
    if user:
        password_correct = bcrypt.checkpw(
            password.encode("utf-8"),
            user[1].encode("utf-8")
            )
        if password_correct:
            user_id = user[0]
        else:
            user_id= None  
    connection.close()  
    return user_id         
       