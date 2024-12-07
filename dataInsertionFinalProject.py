import mysql.connector
from mysql.connector import Error


class BookstoreDatabaseInserter:
    def __init__(self, db_config):
        """Initialize with database configuration."""
        self.db_config = db_config
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        """Close the database connection."""
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")

    def bulk_insert_data(self, table_name, fields, data):
        """Insert data into a table using bulk insert."""
        try:
            query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(fields))})"
            self.cursor.executemany(query, data)
            print(f"Data inserted into {table_name} successfully.")
        except Error as e:
            print(f"Error inserting into {table_name}: {e}")

    def commit_changes(self):
        """Commit the changes to the database."""
        try:
            self.conn.commit()
            print("Changes committed to the database.")
        except Error as e:
            print(f"Error committing changes: {e}")


if __name__ == "__main__":
    # Database connection configuration
    db_config = {
        'host': 'localhost',
        'user': '****', # Update this as per your MySQL setup
        'password': '****',  # Update this as per your MySQL setup
        'database': 'Bookstore'
    }

    inserter = BookstoreDatabaseInserter(db_config)
    inserter.connect()

    try:
        # Data definitions
        data_definitions = {
            'Users': (
                ['UserID', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'Address', 'RegistrationDate', 'TotalSpent', 'PermissionType'],
                [
                    (1, 'John', 'Doe', 'john.doe@example.com', '1234567890', '123 Elm St, NY', '2023-01-01', 1000.00,
                     'Admin'),
                    (
                    2, 'Jane', 'Smith', 'jane.smith@example.com', '9876543210', '456 Oak St, CA', '2023-02-15', 1300.00,
                    'User'),
                    (
                    3, 'Emily', 'Johnson', 'emily.j@example.com', '1112223333', '789 Pine St, TX', '2023-03-20', 650.00,
                    'User'),
                    (4, 'Michael', 'Clark', 'michael.c@example.com', '3334445555', '101 Maple St, FL', '2023-05-10',
                     200.00, 'User'),
                    (5, 'Aliyah', 'Brown', 'aliyah.b@example.com', '5556667777', '202 Spruce St, NV', '2023-06-15',
                     400.00, 'Admin'),
                    (6, 'David', 'Kim', 'david.k@example.com', '2228889999', '303 Cedar St, OR', '2023-07-25', 350.00,
                     'User'),
                    (7, 'Sarah', 'Lee', 'sarah.l@example.com', '4445556666', '404 Birch St, WA', '2023-08-05', 50.00,
                     'User'),
                    (8, 'Christopher', 'White', 'christopher.w@example.com', '7778889990', '505 Palm St, AZ',
                     '2023-09-12', 600.00, 'Admin'),
                    (9, 'Maria', 'Garcia', 'maria.g@example.com', '6667778888', '606 Redwood St, CO', '2023-10-19',
                     75.00, 'User'),
                    (10, 'William', 'Taylor', 'william.t@example.com', '8889990000', '707 Aspen St, MA', '2023-11-01',
                     900.00, 'User')
                ]
            ),
            'Books': (
                ['BookID', 'ISBN', 'Title', 'Publisher', 'PublicationYear', 'Edition', 'Price', 'Stock'],
                [
                    (1, '9780062316035', 'American Gods', 'William Morrow', 2001, '1st', 15.99, 50),
                    (2, '9780451418450', 'The Shining', 'Signet', 1977, '1st', 9.99, 500),
                    (3, '9780385504206', 'The Da Vinci Code', 'Doubleday', 2003, '1st', 14.99, 25),
                    (4, '9780345410253', 'Kindred', 'Beacon Press', 1979, '1st', 12.99, 32),
                    (5, '9780345538933', 'The Fifth Season', 'Orbit Books', 2015, '1st', 15.99, 5),
                    (6, '9780374531325', 'Beloved', 'Alfred A. Knopf', 1987, '1st', 14.99, 17),
                    (7, '9780374532667', 'Half of a Yellow Sun', 'Alfred A. Knopf', 2006, '1st', 15.99, 20),
                    (8, '9780061120084', 'To Kill a Mockingbird', 'HarperCollins', 1960, '1st', 10.99, 40),
                    (9, '9780140177398', 'Of Mice and Men', 'Penguin Books', 1937, '1st', 7.99, 100),
                    (10, '9780143127741', '1984', 'Houghton Mifflin Harcourt', 1949, '1st', 8.99, 80),
                    (None, '9780062065254', 'Homegoing', 'Knopf', 2016, '1st', 16.99, 0),
                    (None, '9780525559474', 'The Night Watchman', 'Harper Perennial', 2020, '1st', 15.99, 0),
                    (None, '9781594634024', 'The Hate U Give', 'Balzer + Bray', 2017, '1st', 18.99, 0),
                    (None, '9780812993547', 'An American Marriage', 'Algonquin Books', 2018, '1st', 17.99, 0),
                    (None, '9780593203414', 'The City We Became', 'Orbit Books', 2020, '1st', 19.99, 0),
                    (None, '9780593318170', 'Such a Fun Age', 'Berkley', 2019, '1st', 14.99, 0),
                    (None, '9780062316097', 'Anansi Boys', 'William Morrow', 2005, '1st', 16.99, 30),
                    (None, '9780385504207', 'Angels and Demons', 'Doubleday', 2000, '1st', 13.99, 150),
                    (None, '9780062316110', 'Neverwhere', 'HarperCollins', 1996, '1st', 14.99, 40),
                    (None, '9781451673319', 'The Institute', 'Scribner', 2019, '1st', 14.99, 60),
                    (None, '9780395559682', 'The Bluest Eye', 'Knopf', 1970, '1st', 13.99, 100),
                    (None, '9780452295264', 'The Dark Tower: The Gunslinger', 'Penguin Books', 1982, '1st', 12.99, 120),
                    (None, '9780452295271', 'The Dark Tower: The Drawing of the Three', 'Penguin Books', 1987, '1st',
                     14.99, 75),
                    (None, '9780316031137', 'Americanah', 'Anchor Books', 2013, '1st', 16.99, 25),
                    (None, '9781608199393', 'The Underground Railroad', 'Doubleday', 2016, '1st', 17.99, 10),
                    (None, '9780735212196', 'The Water Dancer', 'Random House', 2019, '1st', 18.99, 15),
                    (None, '9781101911443', 'Purple Hibiscus', 'Algonquin Books', 2003, '1st', 12.99, 50),
                    (None, '9780525559481', 'The Nickel Boys', 'Doubleday', 2019, '1st', 19.99, 20),
                    (None, '9780143127742', 'The Circle', 'Hachette Book Group', 2013, '1st', 13.99, 85),
                    (None, '9781400067682', 'Room', 'Little, Brown and Company', 2010, '1st', 15.99, 30),
                    (None, '9780399591452', 'The Vanishing Half', 'Riverhead Books', 2020, '1st', 17.99, 40)
                ]
            ),
            'Orders': (
                ['OrderID', 'UserID', 'OrderDate', 'TotalAmount', 'Status'],
                [
                    (1, 1, '2023-11-05 10:00:00', 31.98, 'Pending'),  # November 2023
                    (2, 2, '2023-12-22 14:30:00', 9.99, 'Shipped'),  # December 2023
                    (3, 3, '2024-01-15 12:15:00', 89.96, 'Pending'),
                    (4, 1, '2024-02-04 09:45:00', 15.99, 'Canceled'),
                    (5, 2, '2024-03-25 16:30:00', 30.98, 'Shipped'),
                    (6, 3, '2024-10-18 11:00:00', 29.98, 'Delivered'),
                    (7, 4, '2024-07-12 12:00:00', 12.99, 'Pending'),
                    (8, 5, '2023-10-14 14:00:00', 15.99, 'Shipped'),  # October 2023
                    (9, 6, '2024-11-02 13:45:00', 44.97, 'Delivered'),  # November 2024
                    (10, 7, '2023-11-19 15:15:00', 31.98, 'Pending'),  # November 2024
                    (11, 3, '2024-11-15 10:30:00', 16.99, 'Pending'),
                    (12, 7, '2022-11-22 14:15:00', 15.99, 'Shipped'),
                    (13, 2, '2023-09-25 12:45:00', 18.99, 'Pending'),
                    (14, 5, '2023-01-28 09:30:00', 17.99, 'Delivered'),
                    (15, 1, '2024-11-29 16:00:00', 19.99, 'Pending'),
                    (16, 4, '2024-10-30 11:15:00', 14.99, 'Shipped'),
                    (None, 7, '2022-11-22 14:15:00', 15.99, 'Shipped'),
                    (None, 2, '2023-09-25 12:45:00', 18.99, 'Pending'),
                    (None, 5, '2023-01-28 09:30:00', 17.99, 'Delivered'),
                    (None, 1, '2024-11-29 16:00:00', 19.99, 'Pending'),
                    (None, 4, '2024-10-30 11:15:00', 14.99, 'Shipped')
                ]
            ),
            'OrderDetails': (
                ['OrderDetailID', 'OrderID', 'BookID', 'Quantity', 'Subtotal', 'Discount'],
                [
                    (1, 1, 1, 2, 31.98, 0.00),
                    (2, 2, 2, 1, 9.99, 0.00),
                    (3, 3, 3, 3, 44.97, 5.00),
                    (4, 3, 4, 2, 25.98, 0.00),
                    (5, 4, 5, 1, 15.99, 0.00),
                    (6, 5, 6, 2, 29.98, 0.00),
                    (7, 6, 7, 1, 15.99, 0.00),
                    (8, 7, 8, 1, 10.99, 0.00),
                    (9, 8, 9, 2, 15.98, 0.00),
                    (10, 9, 10, 3, 26.97, 5.00),
                    (11, 11, 11, 1, 16.99, 0.00),
                    (12, 12, 12, 1, 15.99, 0.00),
                    (13, 13, 13, 1, 18.99, 0.00),
                    (14, 14, 14, 1, 17.99, 0.00),
                    (15, 15, 15, 1, 19.99, 0.00),
                    (16, 16, 16, 1, 14.99, 0.00),
                    (None, 2, 2, 1, 9.99, 0.00),
                    (None, 3, 3, 3, 44.97, 5.00),
                    (None, 3, 4, 2, 25.98, 0.00),
                    (None, 4, 5, 1, 15.99, 0.00),
                    (None, 5, 6, 2, 29.98, 0.00),
                    (None, 6, 7, 1, 15.99, 0.00),
                    (None, 7, 8, 1, 10.99, 0.00),
                    (None, 8, 9, 2, 15.98, 0.00),
                    (None, 7, 8, 1, 10.99, 0.00),
                ]
            ),
            'Authors': (
                ['AuthorID', 'Name'],
                [
                    (1, 'Neil Gaiman'),
                    (2, 'Stephen King'),
                    (3, 'Dan Brown'),
                    (4, 'Octavia E. Butler'),
                    (5, 'N.K. Jemisin'),
                    (6, 'Toni Morrison'),
                    (7, 'Chimamanda Ngozi Adichie')
                ]
            ),
            'BookAuthors': (
                ['BookID', 'AuthorID'],
                [
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7)
                ]
            ),
            'Genres': (
                ['GenreID', 'GenreName'],
                [
                    (1, 'Fantasy'),
                    (2, 'Horror'),
                    (3, 'Thriller'),
                    (4, 'Science Fiction'),
                    (5, 'History'),
                    (6, 'Literary Fiction'),
                    (7, 'Contemporary Fiction')
                ]
            ),
            'BookGenres': (
                ['BookID', 'GenreID'],
                [
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7)
                ]
            ),
            'Notifications': (
                ['NotificationID', 'UserID', 'Message', 'NotificationDate', 'NotificationType'],
                [
                    (1, 1, 'Welcome to our bookstore!', '2024-12-01 08:00:00', 'SystemAlert'),
                    (2, 2, 'Your order has been shipped!', '2024-12-02 14:30:00', 'OrderUpdate'),
                    (3, 3, 'Your order has been delivered.', '2024-12-03 16:45:00', 'OrderUpdate'),
                    (4, 1, 'Special discount for you!', '2024-12-04 09:15:00', 'Promotions')
                ]
            ),
            'AuditLogs': (
                ['UserID', 'Action', 'Timestamp', 'Details'],
                [
                    (1, 'User logged in', '2024-12-01 08:00:00', 'User successfully logged in after entering correct credentials'),
                    (2, 'Order placed', '2024-12-02 14:30:00', 'User placed an order for book \"Python Programming\"'),
                    (3, 'Order shipped', '2024-12-03 16:45:00', 'Order #12345 has been shipped'),
                    (1, 'System Alert', '2024-12-04 09:15:00', 'System generated alert regarding low stock of book \"Data Science 101\"')
                ]
            ),
            'UserAccounts': (
                ['UserID', 'Username', 'Password', 'AccountStatus', 'LastLogin'],
                [
                    (1, 'johndoe', 'hashed_password1', 'Active', '2023-12-04 09:15:00'),
                    (2, 'janesmith', 'hashed_password2', 'Active', '2023-11-25 14:30:00'),
                    (3, 'emilyj', 'hashed_password3', 'Active', '2023-10-28 17:00:00'),
                    (4, 'michael_c', 'hashed_password4', 'Active', '2023-11-28 17:00:00'),
                    (5, 'aliyah.b', 'hashed_password5', 'Active', '2023-11-18 12:00:00'),
                    (6, 'david_k', 'hashed_password6', 'Active', '2023-12-02 10:45:00'),
                    (7, 'sarah_l', 'hashed_password7', 'Suspended', None),
                    (8, 'christopher.w', 'hashed_password8', 'Active', '2023-11-10 08:15:00'),
                    (9, 'maria_g', 'hashed_password9', 'Active', '2023-11-29 19:00:00'),
                    (10, 'william_t', 'hashed_password10', 'Active', '2023-12-01 15:30:00')
                ]
            ),

            'Vendors': (
                ['VendorID', 'CompanyName', 'ContactName', 'ContactEmail', 'ContactPhone', 'Address', 'SupplyType'],
                [
                    (1, 'Global Book Distributors', 'Laura Peterson', 'laura.p@example.com', '1234567890',
                     '123 Market St, NY', 'Books'),
                    (2, 'E-Library Supplies', 'Daniel Lee', 'daniel.l@example.com', '9876543210', '456 Main St, CA',
                     'E-Books'),
                    (3, 'Quick Logistics', 'Michael Johnson', 'michael.j@example.com', '1112223333', '789 Broad St, TX',
                     'Logistics'),
                    (4, 'BookDepot Inc.', 'Sarah Brown', 'sarah.b@example.com', '3334445555', '101 Elm St, FL', 'Books'),
                    (5, 'Digital Reads Co.', 'Emily Davis', 'emily.d@example.com', '5556667777', '202 Cedar St, NV',
                     'E-Books'),
                    (6, 'Prime Logistics', 'John Taylor', 'john.t@example.com', '2228889999', '303 Maple St, OR',
                     'Logistics'),
                    (7, 'WorldWide Books', 'Chloe Wilson', 'chloe.w@example.com', '4445556666', '404 Birch St, WA',
                     'Books'),
                    (8, 'E-Books Direct', 'David Martinez', 'david.m@example.com', '7778889990', '505 Palm St, AZ',
                     'E-Books'),
                    (9, 'Rapid Delivery Services', 'Samantha Clark', 'samantha.c@example.com', '6667778888',
                     '606 Pine St, CO', 'Logistics'),
                    (10, 'Book Haven', 'Benjamin White', 'benjamin.w@example.com', '8889990000', '707 Aspen St, MA',
                     'Books')
                ]
            ),
            'VendorOrders': (
                ['VendorOrderID', 'VendorID', 'BookID', 'OrderDate', 'Quantity', 'TotalCost', 'DeliveryDate',
                 'OrderStatus'],
                [
                    (1, 1, 1, '2024-01-05 10:00:00', 50, 800.00, '2024-01-10', 'Received'),
                    (2, 2, 2, '2024-02-12 14:30:00', 100, 1500.00, '2024-02-20', 'Received'),
                    (3, 3, 3, '2024-03-18 09:15:00', 25, 375.00, '2024-03-25', 'Received'),
                    (4, 4, 4, '2024-04-10 11:45:00', 40, 520.00, '2024-04-15', 'Canceled'),
                    (5, 5, 5, '2024-05-22 16:30:00', 10, 150.00, '2024-05-30', 'Pending'),
                    (6, 6, 6, '2024-06-15 13:00:00', 20, 300.00, '2024-06-25', 'Received'),
                    (7, 7, 7, '2024-07-09 10:30:00', 15, 240.00, '2024-07-15', 'Pending'),
                    (8, 8, 1, '2024-08-04 08:15:00', 60, 960.00, '2024-08-12', 'Received'),
                    (9, 9, 2, '2024-09-20 14:45:00', 30, 450.00, '2024-09-27', 'Pending'),
                    (10, 10, 3, '2024-10-11 12:20:00', 50, 750.00, '2024-10-18', 'Canceled')
                ]
            )

        }

        # Perform bulk inserts
        for table, (fields, data) in data_definitions.items():
            inserter.bulk_insert_data(table, fields, data)

        inserter.commit_changes()

    except Exception as e:
        print(f"An error occurred during the insertion process: {e}")

    finally:
        inserter.disconnect()

