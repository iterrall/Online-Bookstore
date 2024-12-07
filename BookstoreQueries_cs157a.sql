-- View data in each table
SELECT * FROM Users;
SELECT * FROM Books;
SELECT * FROM Orders;
SELECT * FROM OrderDetails;
SELECT * FROM Vendors;
SELECT * FROM VendorOrders;
SELECT * FROM Authors;
SELECT * FROM BookAuthors;
SELECT * FROM Genres;
SELECT * FROM BookGenres;
SELECT * FROM Notifications;
SELECT * FROM AuditLogs;

-- Count the Rows in Each Table
SELECT 'Users' AS TableName, COUNT(*) AS RowCount FROM Users
UNION
SELECT 'UserAccounts', COUNT(*) FROM UserAccounts
UNION
SELECT 'Orders', COUNT(*) FROM Orders
UNION
SELECT 'Books', COUNT(*) FROM Books
UNION
SELECT 'OrderDetails', COUNT(*) FROM OrderDetails
UNION
SELECT 'Authors', COUNT(*) FROM Authors
UNION
SELECT 'BookAuthors', COUNT(*) FROM BookAuthors
UNION
SELECT 'Genres', COUNT(*) FROM Genres
UNION
SELECT 'BookGenres', COUNT(*) FROM BookGenres
UNION
SELECT 'Vendors', COUNT(*) FROM Vendors
UNION
SELECT 'VendorOrders', COUNT(*) FROM VendorOrders
UNION
SELECT 'Notifications', COUNT(*) FROM Notifications
UNION
SELECT 'AuditLogs', COUNT(*) FROM AuditLogs;

-- 1. Sales for November 2024 and comparison with previous periods 
-- (Assigned Query 1)
-- Total Sales for November 2024:
SELECT SUM(TotalAmount) AS Nov2024_Sales
FROM Orders
WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2024;
-- Total Sales for November 2023:
SELECT SUM(TotalAmount) AS Nov2023_Sales
FROM Orders
WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2023;
-- Total Sales for October 2024:
SELECT SUM(TotalAmount) AS Oct2024_Sales
FROM Orders
WHERE MONTH(OrderDate) = 10 AND YEAR(OrderDate) = 2024;
-- Compare November 2024 to Previous Periods:
SELECT 
    'November 2024' AS Period,
    (SELECT SUM(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2024) AS November2024Sales,
    (SELECT SUM(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2023) AS November2023Sales,
    (SELECT SUM(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 10 AND YEAR(OrderDate) = 2024) AS October2024Sales;
-- More comprehensive comparison of November 2024 to Previous Periods:
SELECT 
    'November 2024' AS Period,
    November2024Sales,
    November2023Sales,
    October2024Sales,
    November2024Count,
    November2023Count,
    November2024Average,
    November2023Average,
    CASE 
        WHEN November2023Sales > 0 
        THEN ((November2024Sales - November2023Sales) / November2023Sales) * 100 
        ELSE NULL 
    END AS PercentageDifference
FROM (
    SELECT
        (SELECT SUM(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2024) AS November2024Sales,
        (SELECT SUM(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2023) AS November2023Sales,
        (SELECT SUM(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 10 AND YEAR(OrderDate) = 2024) AS October2024Sales,
        (SELECT COUNT(*) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2024) AS November2024Count,
        (SELECT COUNT(*) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2023) AS November2023Count,
        (SELECT AVG(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2024) AS November2024Average,
        (SELECT AVG(TotalAmount) FROM Orders WHERE MONTH(OrderDate) = 11 AND YEAR(OrderDate) = 2023) AS November2023Average
) AS Summary;
-- 2. Identify the best seller and the worst seller 
-- (Assigned Query 2)
-- Best Seller:
SELECT 
    B.BookID, B.Title, SUM(OD.Quantity) AS TotalSold
FROM 
    OrderDetails OD
JOIN 
    Books B ON OD.BookID = B.BookID
GROUP BY 
    B.BookID, B.Title
ORDER BY 
    TotalSold DESC
LIMIT 1;
-- Worst Seller:
SELECT 
    B.BookID, B.Title, SUM(OD.Quantity) AS TotalSold
FROM 
    OrderDetails OD
JOIN 
    Books B ON OD.BookID = B.BookID
GROUP BY 
    B.BookID, B.Title
ORDER BY 
    TotalSold ASC
LIMIT 1;
-- 3. Identify the most and least profitable vendors
-- (Assigned Query 3)
-- Most Profitable Vendor:
SELECT 
    V.VendorID, V.CompanyName, SUM(VO.TotalCost) AS TotalProfit
FROM 
    VendorOrders VO
JOIN 
    Vendors V ON VO.VendorID = V.VendorID
GROUP BY 
    V.VendorID, V.CompanyName
ORDER BY 
    TotalProfit DESC
LIMIT 1;
-- Least Profitable Vendor:
SELECT 
    V.VendorID, V.CompanyName, SUM(VO.TotalCost) AS TotalProfit
FROM 
    VendorOrders VO
JOIN 
    Vendors V ON VO.VendorID = V.VendorID
GROUP BY 
    V.VendorID, V.CompanyName
ORDER BY 
    TotalProfit ASC
LIMIT 1;
-- 4. Automatic inventory order when threshold is reached 
-- (Assigned Query 4)
-- Inventory Threshold Check:
SELECT 
    B.BookID, B.Title, B.Stock, V.VendorID, V.CompanyName
FROM 
    Books B
JOIN 
    VendorOrders VO ON B.BookID = VO.BookID
JOIN 
    Vendors V ON VO.VendorID = V.VendorID
WHERE 
    B.Stock <= 5; -- Adjust the threshold as needed
-- Auto Order Insert:
SELECT COUNT(*) AS BeforeCount FROM VendorOrders;

INSERT INTO VendorOrders (VendorID, BookID, Quantity, TotalCost, OrderStatus)
SELECT 
    V.VendorID, B.BookID, 10 AS Quantity, B.Price * 10 AS TotalCost, 'Pending' AS OrderStatus
FROM 
    Books B
JOIN 
    VendorOrders VO ON B.BookID = VO.BookID
JOIN 
    Vendors V ON VO.VendorID = V.VendorID
WHERE 
    B.Stock <= 5; -- Adjust threshold and quantity

SELECT COUNT(*) AS AfterCount FROM VendorOrders;

-- 5. Items not sold in the past 3 months 
-- (Assigned Query 5)
-- Identify Unsold Items:
SELECT 
    B.BookID, B.Title, B.Stock, B.Price
FROM 
    Books B
LEFT JOIN 
    OrderDetails OD ON B.BookID = OD.BookID
LEFT JOIN 
    Orders O ON OD.OrderID = O.OrderID
WHERE 
    (O.OrderDate IS NULL OR O.OrderDate < NOW() - INTERVAL 3 MONTH);
-- Sale Discount on Unsold Items:
-- Create a temporary table or subquery for books sold in the past 3 months
WITH BooksSoldLast3Months AS (
    SELECT DISTINCT od.BookID
    FROM OrderDetails od
    INNER JOIN Orders o ON od.OrderID = o.OrderID
    WHERE o.OrderDate >= NOW() - INTERVAL 3 MONTH
)

-- List books not in the above results and apply a discount for the sale
SELECT 
    b.BookID,
    b.Title,
    b.Price AS OriginalPrice,
    (b.Price * 0.8) AS SalePrice -- Example: 20% discount
FROM Books b
LEFT JOIN BooksSoldLast3Months bs ON b.BookID = bs.BookID
WHERE bs.BookID IS NULL; -- Only books not sold in the past 3 months

-- 6. Trigger: Automatically update the TotalSpent field in Users table after a new order
-- (Extra Query 1)
-- Check BEFORE implementing trigger
-- Check the TotalSpent value for the user 
SELECT TotalSpent 
FROM Users 
WHERE UserID = 1;
-- Create Trigger to update TotalSpent:
DELIMITER $$

CREATE TRIGGER UpdateTotalSpent
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
    UPDATE Users
    SET TotalSpent = TotalSpent + NEW.TotalAmount
    WHERE UserID = NEW.UserID;
END $$

DELIMITER ;
-- Check AFTER implementing trigger
-- Insert a test order to verify the trigger 
INSERT INTO Orders (UserID, TotalAmount, Status) VALUES (1, 50.00, 'Pending');
-- Check the TotalSpent value for the user 
SELECT TotalSpent 
FROM Users 
WHERE UserID = 1;
-- 7. Retrieve the top 5 users by spending and their percentile rank.
-- (Extra Query 2)
SELECT
    UserID,
    CONCAT(FirstName, ' ', LastName) AS FullName,
    TotalSpent,
    RANK() OVER (ORDER BY TotalSpent DESC) AS UserRank,
    ROUND(PERCENT_RANK() OVER (ORDER BY TotalSpent DESC), 2) AS PercentileRank
FROM
    Users
ORDER BY
    UserRank
LIMIT 5;
-- 8. Updating Tables: Apply a bulk discount to all books in a specific genre  
-- (Extra Query 3)
-- Apply 15% Discount to All Books in the "History" Genre:
-- check price before updating:
SELECT BookID, Price
FROM Books
WHERE BookID IN (
    SELECT BG.BookID
    FROM BookGenres BG
    JOIN Genres G ON BG.GenreID = G.GenreID
    WHERE G.GenreName = 'History'
);
-- Execute the update query
UPDATE Books
SET Price = Price * 0.85
WHERE BookID IN (
    SELECT BG.BookID
    FROM BookGenres BG
    JOIN Genres G ON BG.GenreID = G.GenreID
    WHERE G.GenreName = 'History'
);

-- Query the updated data to confirm query worked
SELECT BookID, Price
FROM Books
WHERE BookID IN (
    SELECT BG.BookID
    FROM BookGenres BG
    JOIN Genres G ON BG.GenreID = G.GenreID
    WHERE G.GenreName = 'History'
);
-- 9. Query for Advanced Joins: Find users who have placed more than 5 orders but haven't logged in for 6 months  
-- (Extra Query 4)
-- Complex Join Query:
SELECT U.UserID, U.FirstName, U.LastName, U.Email, COUNT(O.OrderID) AS TotalOrders
FROM Users U
JOIN Orders O ON U.UserID = O.UserID
LEFT JOIN UserAccounts UA ON U.UserID = UA.UserID
WHERE UA.LastLogin < NOW() - INTERVAL 2 MONTH
GROUP BY U.UserID, U.FirstName, U.LastName, U.Email
HAVING TotalOrders > 2;
-- 10. Generating Reports with Aggregates and Ranking: Top 3 users with the highest spending in 2024 
-- (Extra Query 5)
SELECT U.UserID, U.FirstName, U.LastName, U.Email, SUM(O.TotalAmount) AS TotalSpent2024
FROM Users U
JOIN Orders O ON U.UserID = O.UserID
WHERE YEAR(O.OrderDate) = 2024
GROUP BY U.UserID, U.FirstName, U.LastName, U.Email
ORDER BY TotalSpent2024 DESC
LIMIT 3;
-- 11. Stored Procedure: Automatically reorder books below a specified stock threshold 
-- (Extra Query 6)
-- Create Stored Procedure:
DELIMITER $$

CREATE PROCEDURE AutoReorderBooks(threshold INT, reorderQty INT)
BEGIN
    INSERT INTO VendorOrders (VendorID, BookID, Quantity, TotalCost, OrderStatus)
    SELECT 
        V.VendorID, B.BookID, reorderQty, B.Price * reorderQty, 'Pending'
    FROM Books B
    JOIN VendorOrders VO ON B.BookID = VO.BookID
    JOIN Vendors V ON VO.VendorID = V.VendorID
    WHERE B.Stock < threshold;
END $$

DELIMITER ;

-- Execute Procedure:
CALL AutoReorderBooks(10, 50); -- Reorder books with stock below 10, adding 50 units

-- check worked: 
SHOW PROCEDURE STATUS WHERE Db = 'bookstore';
-- 12. Find the best-selling books and the percentage contribution to total sales.
-- (Extra Query 7)
WITH TotalSales AS (
    SELECT SUM(od.Quantity) AS OverallQuantitySold 
    FROM OrderDetails od
),
BookSales AS (
    SELECT 
        b.BookID, 
        b.Title, 
        SUM(od.Quantity) AS TotalQuantitySold 
    FROM 
        OrderDetails od
    JOIN 
        Books b ON od.BookID = b.BookID 
    GROUP BY 
        b.BookID, b.Title
)
SELECT 
    bs.BookID, 
    bs.Title, 
    bs.TotalQuantitySold, 
    ROUND((bs.TotalQuantitySold / ts.OverallQuantitySold) * 100, 2) AS ContributionPercentage 
FROM 
    BookSales bs, TotalSales ts
ORDER BY 
    bs.TotalQuantitySold DESC;
-- 13. Query for Notifications: Notify users about undelivered orders for more than 30 days 
-- (Extra Query 8)
-- Identify Undelivered Orders:
-- check before:
SELECT COUNT(*) FROM Notifications;

INSERT INTO Notifications (UserID, Message, NotificationType)
SELECT 
    O.UserID,
    CONCAT('Your order #', O.OrderID, ' placed on ', O.OrderDate, ' is still undelivered. Please contact support.'),
    'OrderUpdate'
FROM Orders O
WHERE O.Status != 'Delivered' AND O.OrderDate < NOW() - INTERVAL 30 DAY;

-- check after:
SELECT COUNT(*) FROM Notifications;
-- 14. List all users with their total spending, rank them, and include their percentile.
-- (Extra Query 9)
WITH UserSpending AS (
    SELECT
        UserID,
        CONCAT(FirstName, ' ', LastName) AS FullName,
        TotalSpent,
        RANK() OVER (ORDER BY TotalSpent DESC) AS UserRank,
        NTILE(100) OVER (ORDER BY TotalSpent DESC) AS Percentile
    FROM
        Users
)
SELECT *
FROM UserSpending;
-- 15. Find books that are out of stock and their last sale date.
-- (Extra Query 10)
SELECT 
    b.BookID, 
    b.Title, 
    b.Stock, 
    MAX(o.OrderDate) AS LastSoldDate 
FROM 
    Books b
LEFT JOIN 
    OrderDetails od ON b.BookID = od.BookID
LEFT JOIN 
    Orders o ON od.OrderID = o.OrderID
WHERE 
    b.Stock = 0
GROUP BY 
    b.BookID, b.Title, b.Stock;
-- 16. Retrieve all orders placed in November 2024 and include their total discount.
-- (Extra Query 11)
WITH OrderDiscounts AS (
    SELECT
        o.OrderID,
        COALESCE(SUM(od.Discount), 0.00) AS TotalDiscount
    FROM
        Orders o
    JOIN
        OrderDetails od ON o.OrderID = od.OrderID
    WHERE
        MONTH(o.OrderDate) = 11 AND YEAR(o.OrderDate) = 2024
    GROUP BY
        o.OrderID
)
SELECT
    o.OrderID,
    o.UserID,
    o.OrderDate,
    o.TotalAmount,
    o.Status,
    COALESCE(d.TotalDiscount, 0.00) AS TotalDiscount
FROM
    Orders o
LEFT JOIN
    OrderDiscounts d ON o.OrderID = d.OrderID;
-- 17. Get the total revenue for each month of 2024, including the cumulative total.
-- (Extra Query 12)
WITH MonthlyRevenue AS (
    SELECT 
        MONTH(OrderDate) AS Month, 
        YEAR(OrderDate) AS Year, 
        SUM(TotalAmount) AS MonthlyRevenue 
    FROM 
        Orders 
    WHERE 
        YEAR(OrderDate) = 2024 
    GROUP BY 
        YEAR(OrderDate), MONTH(OrderDate)
)
SELECT 
    Month, 
    Year, 
    MonthlyRevenue, 
    SUM(MonthlyRevenue) OVER (ORDER BY Year, Month) AS CumulativeRevenue 
FROM 
    MonthlyRevenue;
-- 18. Retrieve all books written by a specific author ('Neil Gaiman') along with their genres.
-- (Extra Query 13)
SELECT 
    b.BookID, 
    b.Title, 
    GROUP_CONCAT(g.GenreName) AS Genres 
FROM 
    Books b
JOIN 
    BookAuthors ba ON b.BookID = ba.BookID
JOIN 
    Authors a ON ba.AuthorID = a.AuthorID 
LEFT JOIN 
    BookGenres bg ON b.BookID = bg.BookID
LEFT JOIN 
    Genres g ON bg.GenreID = g.GenreID 
WHERE 
    a.Name = 'Neil Gaiman'
GROUP BY 
    b.BookID, b.Title;
-- 19. Find users with pending orders and the number of their pending orders.
-- (Extra Query 14)
SELECT 
    u.UserID, 
    CONCAT(u.FirstName, ' ', u.LastName) AS FullName, 
    COUNT(o.OrderID) AS PendingOrdersCount 
FROM 
    Users u
JOIN 
    Orders o ON u.UserID = o.UserID 
WHERE 
    o.Status = 'Pending'
GROUP BY 
    u.UserID, FullName;
-- 20. Calculate the total discount given and the average discount per order.
-- (Extra Query 15)
SELECT 
    SUM(Discount) AS TotalDiscountGiven, 
    AVG(Discount) AS AverageDiscountPerOrder 
FROM 
    OrderDetails;
-- 21. List genres and the percentage of total books in each genre.
-- (Extra Query 16)
WITH GenreCounts AS (
    SELECT 
        g.GenreName, 
        COUNT(bg.BookID) AS NumberOfBooks 
    FROM 
        Genres g
    LEFT JOIN 
        BookGenres bg ON g.GenreID = bg.GenreID 
    GROUP BY 
        g.GenreName
), 
TotalBooks AS (
    SELECT COUNT(*) AS TotalBooks 
    FROM BookGenres
)
SELECT 
    gc.GenreName, 
    gc.NumberOfBooks, 
    ROUND((gc.NumberOfBooks / tb.TotalBooks) * 100, 2) AS Percentage 
FROM 
    GenreCounts gc, TotalBooks tb;
-- 22. Find the most expensive order and its breakdown.
-- (Extra Query 17)
WITH MostExpensiveOrder AS (
    SELECT
        OrderID,
        TotalAmount
    FROM
        Orders
    WHERE
        TotalAmount = (SELECT MAX(TotalAmount) FROM Orders)
    LIMIT 1
)
SELECT
    o.OrderID,
    o.UserID,
    o.TotalAmount
FROM
    Orders o
WHERE
    o.OrderID = (SELECT OrderID FROM MostExpensiveOrder);
-- 23. List books ordered more than once, including the last order date.
-- (Extra Query 18)
SELECT 
    b.BookID, 
    b.Title, 
    COUNT(od.OrderDetailID) AS TimesOrdered, 
    MAX(o.OrderDate) AS LastOrderDate 
FROM 
    Books b
JOIN 
    OrderDetails od ON b.BookID = od.BookID 
JOIN 
    Orders o ON od.OrderID = o.OrderID
GROUP BY 
    b.BookID, b.Title 
HAVING 
    TimesOrdered > 1;
-- 24. List authors, the number of books they've written that store has, and the average price of their books.
-- (Extra Query 19)
SELECT 
    a.Name AS AuthorName, 
    COUNT(ba.BookID) AS NumberOfBooks, 
    ROUND(AVG(b.Price), 2) AS AverageBookPrice 
FROM 
    Authors a
LEFT JOIN 
    BookAuthors ba ON a.AuthorID = ba.AuthorID 
LEFT JOIN 
    Books b ON ba.BookID = b.BookID 
GROUP BY 
    a.AuthorID, a.Name;
-- 25. Find users who registered in 2023, including how many orders they placed.
-- (Extra Query 20)
SELECT 
    u.UserID, 
    CONCAT(u.FirstName, ' ', u.LastName) AS FullName, 
    u.RegistrationDate, 
    COUNT(o.OrderID) AS OrdersPlaced 
FROM 
    Users u
LEFT JOIN 
    Orders o ON u.UserID = o.UserID 
WHERE 
    YEAR(u.RegistrationDate) = 2023 
GROUP BY 
    u.UserID, FullName, u.RegistrationDate;


