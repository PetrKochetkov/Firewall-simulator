import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import text


def create_db(database_name):
    engine_create = create_engine("mysql+pymysql://root:root@localhost:3306")
    with engine_create.connect() as conn_create:
        stmt_create = text(f'create database {database_name}')
        conn_create.execute(stmt_create)
        conn_create.commit()


def delete_db(database_name):
    engine_delete = create_engine("mysql+pymysql://root:root@localhost:3306")
    with engine_delete.connect() as conn_delete:
        stmt_delete = text(f'drop database {database_name}')
        conn_delete.execute(stmt_delete)
        conn_delete.commit()


def show_tables(database_name):
    engine_show_tb = create_engine(f"mysql+pymysql://root:root@localhost:3306/{database_name}")
    with engine_show_tb.connect() as conn_show_tb:
        stmt_show_tb = text('Show tables')
        result_show_tb = conn_show_tb.execute(stmt_show_tb)
        resulted_list = list()
        for element in result_show_tb:
            resulted_list.append(element)
        conn_show_tb.commit()
        return resulted_list


db_name = 'firewall'
metadata_obj = MetaData()
engine = create_engine(f"mysql+pymysql://root:root@localhost:3306/{db_name}")

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(30)), )

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(30), nullable=False), )

metadata_obj.create_all(engine)


with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "spongebob", "fullname": "Spongebob Squarepants"},
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()

with engine.connect() as conn:
    stmt = select(user_table)
    result = conn.execute(stmt)
    for el in result:
        print(el)
    conn.commit()

print(show_tables(db_name))

