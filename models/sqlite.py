# import sqlite3
# from sqlite3 import Error
# import sqlalchemy as db

# def create_connection(db_file):

#     conn = None
    
#     try:
#         engine =  db.create_engine(f"sqlite:///{db_file}")
#         conn = engine.connect()
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
    
#     return conn

# if __name__ == '__main__':
#     create_connection(r"../sqlite.db")