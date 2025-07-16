badminton_centers_array = [
    ["Epic Racquet Sports Club", "604-285-5521", "4551 Number 3 Rd unit 140", "Richmond", "BC", "V6X 2C3", "1000", "2300", 11],
    ["ClearOne Badminton Centre", "604-370-9078", "2368 No 5 Rd Unit 160", "Richmond", "BC", "V6X 2T1", "1000", "2300", 7],
    ["Ace Badminton Centre", "604-233-0077", "9151 Van Horne Way", "Richmond", "BC", "V6X 1W2", "0900", "2300", 12],
    ["Stage 18 Badminton Centre", "604-278-3233", "2351 No 6 Rd #170", "Richmond", "BC", "V6V 1P3", "0900", "2200", 18],
    ["Drive Badminton Centre", "604-285-2638", "4551 Number 3 Rd #138", "Richmond", "BC", "V6X 2C3", "1000", "2300", 10],
    ["West Coast Badminton Academy", "604-561-0333", "5900 No 6 Rd #150", "Richmond", "BC", "V6V 1Z1", "1000", "2200", 6]
]
users_array = [
    ["Jeffrey", "604-123-4567", "jeffery@gmail.com"],
    ["Michelle Wagner", "604-458-5780", "tester@hotmail.com"],
    ["Amanda Moyer", "778-234-8654", "moyerA@gmail.com"],
    ["Amy Cochran", "604-258-0969", "amyyyy@yahoo.com"],
    ["Denise Guerrero", "604-945-4679", "deGuerrero@gmail.com"],
    ["Jason Lee", "778-348-4579", "pokeman@gmail.com"],
    ["Terrance Taylor", "604-469-4589", "terranceTaylor@gmail.com"],
    ["William Nguyen", "604-857-0636", "willIam@aol.com"],
    ["Michael Conway", "778-424-0074", "mikehathaway@gmail.com"],
    ["Michael Yoon", "604-993-2683", "michaelYoon@gmail.com"]
]
import random
from databaseManagement import execute_query, execute_query_with_return
from faker import Faker
import datetime
fake = Faker()
"""def generate_users(qty: int):
    users = """"""
    for i in range(0, qty):
        users +=  fake.name()
"""

time_format = '%Y-%m-%d %H%M'
datetime_format ='%Y-%m-%d %H:%M:%S'

from typing import List, Tuple
import ast

#checks against the database to verify if there are any other bookings already in the
#desired timeslot or intersecting with it
def validate_booking_insertion(connection, booking: str) -> bool:
    #maybe fix this thing below: no need for matrix
    #print(booking)
    data = list(ast.literal_eval(f"[{booking}]"))
    #print(f"VALIDATION of {data}")
    start = datetime.datetime.strptime(data[0][2], datetime_format)
    #print(f"start: {start}")
    end = datetime.datetime.strptime(data[0][3], datetime_format)
    #print(f"end: {end}")
    sql_query = f"""SELECT * FROM bookings
    WHERE 
    (bookings.center_id = {data[0][0]} AND bookings.court_number = {data[0][4]})
    AND 
    (('{start}' > bookings.start_time AND bookings.end_time > '{start}')
    OR('{end}' > bookings.start_time AND bookings.end_time > '{end}')
    OR( bookings.start_time > '{start}' AND '{end}' > bookings.start_time)
    OR( bookings.end_time > '{start}' AND '{end}' > bookings.end_time)
    OR('{start}' = bookings.start_time)
    OR('{end}' = bookings.end_time)
    )
    """
    result = execute_query_with_return(connection, sql_query)
    print(f"NUMBER OF RESULTS IS: {len(result)}")
    #print(result)
    return (len(result) == 0)

def rows_in_table(connection, table_name: str) -> int:
    return  execute_query_with_return(connection, f"SELECT COUNT(*) FROM {table_name}")

def format_datetime(inputDate, format)->str:
    if isinstance(inputDate, str):
        try:
            dt = datetime.fromisoformat(inputDate)
        except ValueError:
            try:
                dt = datetime.strptime(inputDate, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    dt = datetime.strptime(inputDate, '%Y-%m-%d %H:%M')
                except ValueError:
                    raise ValueError("Unsupported datetime string format.")
    elif isinstance(inputDate, datetime):
        dt = inputDate
    else:
        raise TypeError("Input must be a datetime object or a string.")
    return dt.strftime(format)

def convert_to_booking_string(center, user, start_time, end_time, court) -> str:
    return f"({center}, {user}, \"{format_datetime(start_time)}\", \"{format_datetime(end_time)}\", \"{court}\""
    

#function to randomly generate a quantity of bookings using the pre made array of users and badminton centers
def generate_bookings(qty:int, connection):
    for count in range(0,qty):
        center = random.randint(1,6)
        user = random.randint(1,10)
        date = str(fake.date_this_month())
        end_time = int(badminton_centers_array[center-1][7])
        start_time = (random.randint(int(badminton_centers_array[center-1][6])//100, end_time//100)*100)-100
        booking_length = random.randint(1,3)*100
        if start_time+booking_length <= end_time:
            end_time = start_time+booking_length 
        booking = f"({center}, {user}, \"{datetime.datetime.strptime(date + " " +str(start_time),time_format)}\", \"{datetime.datetime.strptime(date + " " +str(end_time),time_format)}\", \"{random.randint(1,int(badminton_centers_array[center-1][8]))}\")"
        print(f"Trying to validate: {booking}")
        if validate_booking_insertion(connection, booking):
            print(f"row {count_added} added")
            count_added = count_added + 1
            sql_query = f"""
            INSERT INTO 
                bookings(center_id, user_id, start_time, end_time, court_number)
            VALUES
                {booking}
            """
            execute_query(connection,sql_query)
            #print(sql_query)