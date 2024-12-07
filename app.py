from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': '****', # Update this as per your MySQL setup
    'password': '****', # Update this as per your MySQL setup
    'database': 'Bookstore'
}

# Fetch customer orders
def get_customer_orders():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            Orders.OrderID,
            CONCAT(Users.FirstName, ' ', Users.LastName) AS UserName,
            Orders.OrderDate,
            Orders.TotalAmount,
            Orders.Status
        FROM Orders
        INNER JOIN Users ON Orders.UserID = Users.UserID
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Fetch vendor orders
def get_vendor_orders():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            VendorOrders.VendorOrderID,
            Vendors.CompanyName,
            Books.Title AS BookName,
            VendorOrders.OrderDate,
            VendorOrders.Quantity,
            VendorOrders.TotalCost,
            VendorOrders.OrderStatus
        FROM VendorOrders
        INNER JOIN Vendors ON VendorOrders.VendorID = Vendors.VendorID
        INNER JOIN Books ON VendorOrders.BookID = Books.BookID
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/customer-orders')
def customer_orders():
    return jsonify(get_customer_orders())

@app.route('/api/vendor-orders')
def vendor_orders():
    return jsonify(get_vendor_orders())

if __name__ == '__main__':
    app.run(debug=True)
