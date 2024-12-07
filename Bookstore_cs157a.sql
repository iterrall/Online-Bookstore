-- DROP DATABASE bookstore; -- to use if needed to reset

CREATE DATABASE Bookstore;
USE Bookstore;
-- Users Table
CREATE TABLE Users (
UserID INT PRIMARY KEY AUTO_INCREMENT,
FirstName VARCHAR(100) NOT NULL,
LastName VARCHAR(100) NOT NULL,
Email VARCHAR(255) UNIQUE NOT NULL,
PhoneNumber VARCHAR(15),
Address TEXT,
RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,TotalSpent DECIMAL(10, 2) DEFAULT 0.00 CHECK (TotalSpent >= 0), -- Ensure TotalSpent is always non-negative
PermissionType ENUM('Admin', 'User') DEFAULT 'User', 
CONSTRAINT TotalSpent_Positive CHECK (TotalSpent >= 0)
);
-- UserAccounts Table
CREATE TABLE UserAccounts (
AccountID INT AUTO_INCREMENT PRIMARY KEY,
UserID INT NOT NULL,
Username VARCHAR(50) UNIQUE NOT NULL,
Password VARCHAR(255) NOT NULL,
AccountStatus ENUM('Active', 'Suspended') DEFAULT 'Active',
LastLogin DATETIME DEFAULT NULL,
FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
-- Orders Table
CREATE TABLE Orders (
OrderID INT AUTO_INCREMENT PRIMARY KEY,
UserID INT NOT NULL,
OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
TotalAmount DECIMAL(10, 2) NOT NULL,
Status ENUM('Pending', 'Shipped', 'Delivered', 'Canceled') DEFAULT 'Pending',
FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
-- Books Table
CREATE TABLE Books (
BookID INT AUTO_INCREMENT PRIMARY KEY,
ISBN VARCHAR(13) UNIQUE NOT NULL,
Title VARCHAR(255) NOT NULL,
Publisher VARCHAR(255) NOT NULL,
PublicationYear YEAR,
Edition VARCHAR(50) DEFAULT NULL,
Price DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Added DEFAULT 0.00 to ensure valid data on insertion
Stock INT DEFAULT 0 CHECK (Stock >= 0), -- Ensure non-negative stock
CHECK (Price >= 0) -- Ensure non-negative price
);
-- OrderDetails Table
CREATE TABLE OrderDetails (
OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
OrderID INT NOT NULL,
BookID INT NOT NULL,
Quantity INT NOT NULL CHECK (Quantity > 0), -- Ensure positive quantity
Subtotal DECIMAL(10, 2) NOT NULL CHECK (Subtotal >= 0), -- Ensure non-negative subtotal
Discount DECIMAL(10, 2) DEFAULT 0.00, -- Discount defaults to 0
FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE,
CHECK (Quantity > 0 AND Subtotal >= 0)
);
-- Authors Table
CREATE TABLE Authors (
AuthorID INT AUTO_INCREMENT PRIMARY KEY,
Name VARCHAR(255) NOT NULL
);
-- BookAuthors Table
CREATE TABLE BookAuthors (
BookID INT NOT NULL,
AuthorID INT NOT NULL,
PRIMARY KEY (BookID, AuthorID),
FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE,
FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE CASCADE
);
-- Genres Table
CREATE TABLE Genres (
GenreID INT AUTO_INCREMENT PRIMARY KEY,
GenreName VARCHAR(100) UNIQUE NOT NULL
);
-- BookGenres Table
CREATE TABLE BookGenres (
BookID INT NOT NULL,
GenreID INT NOT NULL,
PRIMARY KEY (BookID, GenreID),
FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE,
FOREIGN KEY (GenreID) REFERENCES Genres(GenreID) ON DELETE CASCADE
);
-- Vendors Table
CREATE TABLE Vendors (
VendorID INT AUTO_INCREMENT PRIMARY KEY,
CompanyName VARCHAR(255) NOT NULL,
ContactName VARCHAR(100),
ContactEmail VARCHAR(255),
ContactPhone VARCHAR(15),
Address TEXT,
SupplyType ENUM('Books', 'E-Books', 'Logistics') NOT NULL
);
-- VendorOrders Table
CREATE TABLE VendorOrders (
VendorOrderID INT PRIMARY KEY AUTO_INCREMENT,
VendorID INT NOT NULL,
BookID INT NOT NULL,
OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
Quantity INT NOT NULL CHECK (Quantity > 0), -- Ensure positive quantity
TotalCost DECIMAL(10, 2) NOT NULL CHECK (TotalCost >= 0), -- Ensure non-negative total cost
DeliveryDate DATE DEFAULT NULL,
OrderStatus ENUM('Pending', 'Received', 'Canceled') DEFAULT 'Pending',
FOREIGN KEY (VendorID) REFERENCES Vendors(VendorID) ON DELETE CASCADE, -- Added ON DELETE CASCADE for data integrity
FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE -- Added ON DELETE CASCADE for data integrity
);
-- Notifications Table
CREATE TABLE Notifications (
NotificationID INT AUTO_INCREMENT PRIMARY KEY,
UserID INT NOT NULL,
Message TEXT NOT NULL,
NotificationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
NotificationType ENUM('OrderUpdate', 'Promotions', 'SystemAlert') DEFAULT 'SystemAlert',
FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
-- AuditLogs Table
CREATE TABLE AuditLogs (
AuditID INT AUTO_INCREMENT PRIMARY KEY,
UserID INT NOT NULL,
Action VARCHAR(100) NOT NULL,
Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
Details TEXT,
FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
-- Indexes & Performance Optimization
-- Users Table
CREATE INDEX idx_users_email ON Users (Email);
-- Books Table
CREATE INDEX idx_books_isbn ON Books (ISBN);
CREATE INDEX idx_books_title ON Books (Title);
-- Orders Table
CREATE INDEX idx_orders_userid ON Orders (UserID);
CREATE INDEX idx_orders_orderdate ON Orders (OrderDate);
-- OrderDetails Table
CREATE INDEX idx_orderdetails_orderid ON OrderDetails (OrderID);
CREATE INDEX idx_orderdetails_bookid ON OrderDetails (BookID);
-- VendorOrders Table
CREATE INDEX idx_vendororders_vendorid ON VendorOrders (VendorID);
-- Verify tables were inserted
SHOW TABLES;


-- Disable foreign key checks to allow truncating tables with dependencies
/* SET FOREIGN_KEY_CHECKS = 0;

-- Truncate tables in the correct order
TRUNCATE TABLE auditlogs;
TRUNCATE TABLE notifications;
TRUNCATE TABLE orderdetails;
TRUNCATE TABLE orders;
TRUNCATE TABLE useraccounts;
TRUNCATE TABLE bookauthors;
TRUNCATE TABLE bookgenres;
TRUNCATE TABLE books;
TRUNCATE TABLE genres;
TRUNCATE TABLE authors;
TRUNCATE TABLE vendororders;
TRUNCATE TABLE vendors;
TRUNCATE TABLE users;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
*/
