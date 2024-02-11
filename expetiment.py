from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import text


def create_db(database_name):
    engine_create = create_engine("mysql+pymysql://root:root@localhost:3306")
    with engine_create.connect() as conn_create:
        stmt_create = text(f'create database {database_name}')
        conn_create.execute(stmt_create)
        conn_create.commit()
        conn_create.close()


def delete_db(database_name):
    engine_delete = create_engine("mysql+pymysql://root:root@localhost:3306")
    with engine_delete.connect() as conn_delete:
        stmt_delete = text(f'drop database {database_name}')
        conn_delete.execute(stmt_delete)
        conn_delete.commit()
        conn_delete.close()


def show_tables(database_name):
    engine_show_tb = create_engine(f"mysql+pymysql://root:root@localhost:3306/{database_name}")
    with engine_show_tb.connect() as conn_show_tb:
        stmt_show_tb = text('Show tables')
        result_show_tb = conn_show_tb.execute(stmt_show_tb)
        resulted_list = list()
        for element in result_show_tb:
            resulted_list.append(element)
        conn_show_tb.commit()
        conn_show_tb.close()
        return resulted_list


def values_from_table(database_name, python_table_name):
    engine_values_from_table = create_engine(f"mysql+pymysql://root:root@localhost:3306/{database_name}")
    with engine_values_from_table.connect() as conn_values_from_table:
        stmt_values_from_table = select(python_table_name)
        result_show_tb = conn_values_from_table.execute(stmt_values_from_table)
        temp_list = list()
        for element in result_show_tb:
            temp_list.append(reversed(list(element)))
        resulted_dict = dict(temp_list)
        conn_values_from_table.commit()
        conn_values_from_table.close()
        return resulted_dict


def truncate_table(database_name, table_name):
    engine_truncate_tb = create_engine(f"mysql+pymysql://root:root@localhost:3306/{database_name}")
    with engine_truncate_tb.connect() as conn_truncate_tb:
        stmt_truncate_tb = text(f'Truncate {table_name}')
        conn_truncate_tb.execute(stmt_truncate_tb)
        conn_truncate_tb.commit()
        conn_truncate_tb.close()


# def create_tables(database_name):
#     engine_create_tables = create_engine(f"mysql+pymysql://root:root@localhost:3306/{database_name}")
#
#     approved_sources = Table(
#         "approved_sources",
#         metadata_obj,
#         Column("id", Integer, primary_key=True),
#         Column("source", String(100), nullable=False),
#     )
#
#     approved_destinations = Table(
#         "approved_destinations",
#         metadata_obj,
#         Column("id", Integer, primary_key=True),
#         Column("destination", String(100), nullable=False),
#     )
#
#     approved_content = Table(
#         "approved_content",
#         metadata_obj,
#         Column("id", Integer, primary_key=True),
#         Column("content", String(100), nullable=False),
#     )
#
#     approved_packet_protocols = Table(
#         "approved_packet_protocols",
#         metadata_obj,
#         Column("id", Integer, primary_key=True),
#         Column("packet_protocol", String(100), nullable=False),
#     )
#
#     approved_app_protocols = Table(
#         "approved_app_protocols",
#         metadata_obj,
#         Column("id", Integer, primary_key=True),
#         Column("app_protocol", String(100), nullable=False),
#     )
#     metadata_obj.create_all(engine_create_tables)
#
#     list_of_tables = [approved_sources, approved_destinations, approved_content, approved_packet_protocols,
#                       approved_app_protocols, ]


if __name__ == "__main__":

    db_name = 'firewall'
    engine = create_engine(f"mysql+pymysql://root:root@localhost:3306/{db_name}")

    metadata_obj = MetaData()
    #  create_db(db_name)

    approved_sources = Table(
        "approved_sources",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("source", String(100), nullable=False),
    )

    approved_destinations = Table(
        "approved_destinations",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("destination", String(100), nullable=False),
    )

    approved_content = Table(
        "approved_content",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("content", String(100), nullable=False),
    )

    approved_packet_protocols = Table(
        "approved_packet_protocols",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("packet_protocol", String(100), nullable=False),
    )

    approved_app_protocols = Table(
        "approved_app_protocols",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("app_protocol", String(100), nullable=False),
    )
    metadata_obj.create_all(engine)

    with engine.connect() as conn:
        result = conn.execute(
            insert(approved_sources),
            [
                {"source": "192.168.0.1:7632"},
                {"source": "87.2.43.2:131"},
                {"source": "31.23.123.12:131"},
            ],
        )
        conn.commit()

    with engine.connect() as conn:
        stmt = select(approved_sources)
        result = conn.execute(stmt)
        for el in result:
            print(el)
        conn.commit()

    print(show_tables(db_name))
    print(values_from_table(db_name, approved_sources))
    truncate_table(db_name, approved_sources)
    print(values_from_table(db_name, approved_sources))
