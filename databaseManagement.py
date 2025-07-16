from mysql import connector
from mysql.connector import Error, OperationalError


def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
#connection = dbm.create_connection("localhost", "root", DB_PASSWORD)
#dbm.create_database(connection, create_db_query)

def database_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(f"Connection to MySQL DB '{db_name}' successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("---Query executed successfully")
        if query == drop_all_tables:
            print("All tables dropped")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_query_with_return(connection, query):
    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute(query)
        connection.commit()
        #print("---Query executed successfully, returning")
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

create_user_logins_table = """
CREATE TABLE IF NOT EXISTS user_logins(
    email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
    PRIMARY KEY (email)
)
"""

create_users_table = """
CREATE TABLE IF NOT EXISTS users(
    user_id INT AUTO_INCREMENT, 
    name TEXT NOT NULL, 
    phone_number VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NOT NULL UNIQUE,
    FOREIGN KEY (email) REFERENCES user_logins(email) ON DELETE CASCADE, 
    PRIMARY KEY (user_id)
)
"""

create_badmintonCenters_table = """
CREATE TABLE IF NOT EXISTS badmintonCenters(
    center_id INT AUTO_INCREMENT,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    address_line1 TEXT NOT NULL, 
    address_line2 TEXT,
    city TEXT NOT NULL,
    province TEXT NOT NULL,
    postalCode TEXT NOT NULL,
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    court_count INT NOT NULL,
    PRIMARY KEY (center_id)
)
"""

create_bookings_table = """
CREATE TABLE IF NOT EXISTS bookings(
    center_id INT NOT NULL,
    user_id INT NOT NULL,
    start_time DATETIME NOT NULL, 
    end_time DATETIME NOT NULL,
    court_number INT NOT NULL,
    PRIMARY KEY (center_id, start_time, court_number),
    FOREIGN KEY (center_id) REFERENCES badmintonCenters(center_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""

create_badmintonCenters = """
INSERT INTO
    badmintonCenters(name, phone_number, address_line1, city, province, postalCode, opening_time, closing_time, court_count)
VALUES
    ("Epic Racquet Sports Club", "604-285-5521", "4551 Number 3 Rd unit 140", "Richmond", "BC", "V6X 2C3", "100000", "230000", 11),
    ("ClearOne Badminton Centre", "604-370-9078", "2368 No 5 Rd Unit 160", "Richmond", "BC", "V6X 2T1", "100000", "230000", 7),
    ("Ace Badminton Centre", "604-233-0077", "9151 Van Horne Way", "Richmond", "BC", "V6X 1W2", "090000", "230000", 12),
    ("Stage 18 Badminton Centre", "604-278-3233", "2351 No 6 Rd #170", "Richmond", "BC", "V6V 1P3", "090000", "220000", 18),
    ("Drive Badminton Centre", "604-285-2638", "4551 Number 3 Rd #138", "Richmond", "BC", "V6X 2C3", "100000", "230000", 10),
    ("West Coast Badminton Academy", "604-561-0333", "5900 No 6 Rd #150", "Richmond", "BC", "V6V 1Z1", "100000", "220000", 6)
"""
#

create_users = """
INSERT INTO
    users(name, phone_number, email)
VALUES
    ("Jeffrey", "604-123-4567", "jeffery@gmail.com"),
    ("Michelle Wagner", "604-458-5780", "tester@hotmail.com"),
    ("Amanda Moyer", "778-234-8654", "moyerA@gmail.com"),
    ("Amy Cochran", "604-258-0969", "amyyyy@yahoo.com"),
    ("Denise Guerrero", "604-945-4679", "deGuerrero@gmail.com"),
    ("Jason Lee", "778-348-4579", "pokeman@gmail.com"),
    ("Terrance Taylor", "604-469-4589", "terranceTaylor@gmail.com"),
    ("William Nguyen", "604-857-0636", "willIam@aol.com"),
    ("Michael Conway", "778-424-0074", "mikehathaway@gmail.com"),
    ("Michael Yoon", "604-993-2683", "michaelYoon@gmail.com")
"""

create_user_logins = """
INSERT INTO
    user_logins(email, password)
VALUES
    ("jeffery@gmail.com", "tester123"),
    ("tester@hotmail.com", "ilovebadminton"),
    ("moyerA@gmail.com", "testtesttest"),
    ("amyyyy@yahoo.com", "password"),
    ("deGuerrero@gmail.com", "Hunter2"),
    ("pokeman@gmail.com", "original151best"),
    ("terranceTaylor@gmail.com", "123456"),
    ("willIam@aol.com", "drowssap"),
    ("mikehathaway@gmail.com", "asdfg123"),
    ("michaelYoon@gmail.com", "yonex100zz")
"""

create_bookings = """
INSERT INTO 
    bookings(center_id, user_id, date, start_time, end_time, court_number)
VALUES
    (1, 1, "2025-07-05", "1700", "1900", 5),
    (1, 1, "2025-07-05", "1700", "1900", 6),
    (1, 1, "2025-07-05", "1700", "1900", 7)
"""

#sql query examples
select_users = """
SELECT * FROM users
"""

select_bookings = """
SELECT * FROM bookings
WHERE court_number = 6
"""

update_booking = """
UPDATE 
    bookings
SET
    court_number = 4
WHERE 
    center_id = 1 AND user_id = 1 AND date = "2025-07-05" AND start_time = "1700" AND court_number = 7
"""

delete_booking = """
DELETE FROM 
    bookings
WHERE
    center_id = 1 AND user_id = 1 AND date = "2025-07-05" AND start_time = "1700" AND court_number = 4
"""

drop_all_tables = """
DROP TABLE IF EXISTS users, badmintonCenters, bookings, user_logins
"""