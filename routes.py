import willpyre
import jinja2
import re
import os
import mimetypes
import hashlib
from willpyre.structure import Response404, Redirect, Cookie
from sqlalchemy import (
    create_engine,
    select,
    insert,
)
from tables import users_table, books_table
from dbutils import login_check, get_user
from itsdangerous import URLSafeSerializer

engine = create_engine("sqlite:///DB.sqlite", echo=True)

serializer = URLSafeSerializer("secret-key", salt="Himalayan")

db_salt = "onlypartly".encode('utf-8')
router = willpyre.Router()
environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))

templates = {
    "index": environment.get_template("index.html"),
    "login": environment.get_template("login.html"),
    "signup": environment.get_template("signup.html"),
    "pop": environment.get_template("pop")
}


async def is_logged_in(req) -> bool:
    if req.cookies.get('sessionid') == None:
        return False
    return True


@router.get('/')
async def index(req, res):
    select_stmt = select(books_table)
    products = []

    with engine.connect() as conn:
        for row in conn.execute(select_stmt):
            print(row)
            products += [
                {
                    "author": row[0],
                    "author_tag": row[2],
                    "name": row[1],
                    "uid": row[3],
                    "price": "$0"
                }
            ]

    loggedin = await is_logged_in(req)
    res.body = templates["index"].render(loggedin=loggedin, showcase=products)
    return res

@router.get('/static/:*filepath')
async def file_hosting(req, res):
    filepath = req.params.get('filepath')
    path = 'static/'
    for part in filepath:
        path += part+'/'
    re.sub("\.\./", "", path) # prevent users from climbing up the directory
    path = path[:-1]
    if os.path.exists(path):
        res.body = open(path).read()
        res.headers["connection"] = "close" # No need of keep-alive
        res.content_type = mimetypes.guess_type(path)[0]
    else:
        res = Response404()
    return res

@router.get('/login')
async def login_get(req, res):
    if await is_logged_in(req):
        return Redirect('/')
    res.body = templates["login"].render()
    return res

@router.post('/login')
async def login_post(req, res):
    if await is_logged_in(req):
        return Redirect('/', status=303)

    user = await get_user(req.body.get('tag', "")[1:])
    if user == None:
        return Redirect('/signup', status=303)
    if await login_check(req.body.get('tag')[1:], req.body.get('password'), user):
        res.cookies["sessionid"] = Cookie(
            serializer.dumps(
            users[0]["usertag"]), 
            http_only=False, 
            secure=False, 
            max_age=3600000)
        return Redirect('/', status=303)
    res.body = "Wrong usertag or password"
    return res

@router.get('/signup')
async def signup_get(req, res):
    res.body = templates["signup"].render()
    return res


@router.post('/signup')
async def signup_post(req, res):
    if await is_logged_in(req):
        return Redirect('/', status=303)
    user = await get_user(req.body.get('tag', ""))
    if user_count != None:
        return Redirect('/login', status=303)

    insert_stmt = insert(users_table).values(name=req.body.get('username'),
                                             usertag=req.body.get('tag')[1:],
                                             password=hashlib.sha512(req.body.get('password').encode('utf-8')+db_salt).hexdigest())
    with engine.connect() as conn:
        result = conn.execute(insert_stmt)
        conn.commit()
        print("user created")
    return Redirect('/login', status=303)


@router.get('/pop')
async def pop_get(req, res):
    res.body = templates["pop"].render()
    return res

