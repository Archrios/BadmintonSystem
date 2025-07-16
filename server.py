# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "django",
#     "dotenv",
#     "flask",
#     "main-py",
#     "mysql",
#     "mysql-connector-python",
#     "mysqlclient",
# ]
# ///
import socket
import threading
import databaseManagement as dbm
import utilities as util
from dotenv import load_dotenv
from mysql.connector import Error
import os
load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 3000))
connection = dbm.database_connection("localhost", "root", DB_PASSWORD, "Badminton_System")
server.listen()
def handle_connection(c):
    c.send("Username: ".encode())
    username = c.recv(1024).decode()
    c.send("Password: ".encode())
    password = c.recv(1024).decode()

    
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT * FROM user_logins WHERE email = %s AND password = %s", (username,password))

    if cursor.fetchall():
        c.send("Successful Login".encode())
    else:
        c.send("Login Failed".encode())

def attempt_booking(center, user, start_time, end_time, court):
     booking = util.convert_to_booking_string(center, user, start_time, end_time, court)
     if util.validate_booking_insertion(connection, booking):
            sql_query = f"""
            INSERT INTO 
                bookings(center_id, user_id, start_time, end_time, court_number)
            VALUES
                {booking}
            """
            dbm.execute_query(connection,sql_query)

def view_all_bookings(center, user):
    query = ("""
    SELECT * FROM bookings
    WHERE bookings.center_id =%s
    AND bookings.user_id = %s
    """, (center, user))
    return dbm.execute_query_with_return(connection, query)

def delete_booking(center, user, start_time, court):
    start_time = util.format_datetime(start_time, util.datetime_format)
    query = ("""
    DELETE FROM bookings
    WHERE bookings.center_id =%s
    AND bookings.user_id = %s
    AND bookings.start_time = %s
    AND bookings.court = %s
    """, (center, user, start_time, court))
    dbm.execute_query(connection, query)
     
def update_booking(center, user, start_time, court,  new_start_time, new_end_time):
    booking = util.convert_to_booking_string(center, user, new_start_time, new_end_time, court)
    #how tf do i validate this
    if util.validate_booking_insertion(connection, booking):
        sql_query = f"""
        INSERT INTO 
            bookings(center_id, user_id, start_time, end_time, court_number)
        VALUES
            {booking}
        """
        dbm.execute_query(connection,sql_query)
     


go = True
try:
    while go:
        client, addr = server.accept()
        threading.Thread(target = handle_connection, args = (client,)).start()
except Error as e:
        print(f"The error '{e}' occurred")
