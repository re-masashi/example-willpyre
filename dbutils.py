from tables import users_table, books_table
from sqlalchemy import (
    create_engine,
    select,
    insert,
)
import hashlib

db_salt = "onlypartly".encode('utf-8')

engine = create_engine("sqlite:///DB.sqlite", echo=True)

async def login_check(usertag: str, password: str, user: dict) -> bool :
    if usertag != user["usertag"]:
        return False
    digest = hashlib.sha512(password.encode('utf-8')+db_salt).hexdigest()
    if digest != user["password"]:
        return False
    return True

async def get_user(usertag: str)->dict:
	'''
	Gets the user from DB. Doesn't check if user isn't there"
	'''
	select_stmt = select(users_table).where(
	    users_table.c.usertag == usertag)

	with engine.connect() as conn:
	    user_cur = conn.execute(select_stmt)
	    users = []
	    for user in user_cur:
	        print(user)
	        users += [{
	            "name": user[0],
	            "usertag": user[1],
	            "password": user[2]
	        }]
	if users == []:
		return None
	return users[0]