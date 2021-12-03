from app import app, db


def create_new_user(username, hash):
    new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username,
                             hash=hash)
    return new_user_id


def get_user(username):
    user = db.execute("SELECT * FROM users WHERE username = ?", username)

    return user
