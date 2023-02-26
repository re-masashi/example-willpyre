from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String
)

books_table = Table(
    "books",
    MetaData(),
    Column("author", String(100)),
    Column("name", String(100), ),
    Column("uid", String(100), primary_key=True),
    Column("author_tag", String(100)),
)

users_table = Table(
    "users",
    MetaData(),
    Column("name", String(100)),
    Column("usertag", String(100)),
    Column("password", String(400))
)
