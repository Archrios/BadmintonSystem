# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "django",
#     "dotenv",
#     "flask",
#     "mysql",
#     "mysql-connector-python",
#     "mysqlclient",
#     "rich",
# ]
# ///
import databaseManagement as dbm
import utilities
import random
from rich import print
from dotenv import load_dotenv
import os

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
create_db_query = "CREATE DATABASE Badminton_System"
if __name__ == "__main__":
    
    connection = dbm.database_connection("localhost", "root", DB_PASSWORD, "Badminton_System")
    
    #init tables
    # dbm.execute_query(connection, dbm.drop_all_tables)
    # dbm.execute_query(connection, dbm.create_user_logins_table)
    # print("user logins table created")
    # dbm.execute_query(connection, dbm.create_users_table)
    # print("users table created")
    # dbm.execute_query(connection, dbm.create_badmintonCenters_table)
    # print("badminton Centers table created")
    # dbm.execute_query(connection, dbm.create_bookings_table)
    # print("bookings table created")
    # dbm.execute_query(connection, dbm.create_user_logins)
    # print("user logins table populated")
    # dbm.execute_query(connection, dbm.create_users)
    # print("users table populated")
    # dbm.execute_query(connection, dbm.create_badmintonCenters)
    # print("badminton centers table populated")
    # utilities.generate_bookings(100, connection)
    # print(f"after: {utilities.rows_in_table(connection, "bookings")}")

    
