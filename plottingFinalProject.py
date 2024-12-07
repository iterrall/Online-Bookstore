import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Replace with your DB host
        user="root",  # Replace with your DB username
        password="root",  # Replace with your DB password
        database="Bookstore"  # Replace with your DB name
    )

# Fetch data using SQL queries
def fetch_data(query):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)  # Fetch data as dictionaries for easy use
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return pd.DataFrame(data)


# Plotting and table generation
def generate_plots_and_tables():
    # Fetch total sales by user
    sales_by_user_query = """
    SELECT CONCAT(FirstName, ' ', LastName) AS User, SUM(TotalAmount) AS TotalSales
    FROM Users U
    JOIN Orders O ON U.UserID = O.UserID
    GROUP BY U.UserID
    ORDER BY TotalSales DESC;
    """
    sales_by_user_df = fetch_data(sales_by_user_query)
    print("Sales by User:")
    print(sales_by_user_df)

    # Plot total sales by user
    plt.figure(figsize=(10, 6))
    plt.bar(sales_by_user_df['User'], sales_by_user_df['TotalSales'], color='skyblue')
    plt.title("Total Sales by User")
    plt.xlabel("User")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    def plot_top_customers(sales_by_user_df, top_n=5):
        top_customers_df = sales_by_user_df.head(top_n)

        plt.figure(figsize=(10, 6))
        plt.bar(top_customers_df['User'], top_customers_df['TotalSales'], color='darkorange')
        plt.title(f"Top {top_n} Customers by Revenue", fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel("Customer", fontsize=14)
        plt.ylabel("Total Sales ($)", fontsize=14)
        plt.xticks(rotation=45, fontsize=12, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    # Call this function
    plot_top_customers(sales_by_user_df)

    # Fetch book sales count
    book_sales_query = """
    SELECT B.Title AS Book, SUM(OD.Quantity) AS TotalSold
    FROM Books B
    JOIN OrderDetails OD ON B.BookID = OD.BookID
    GROUP BY B.BookID
    ORDER BY TotalSold DESC;
    """
    book_sales_df = fetch_data(book_sales_query)
    print("Book Sales Count:")
    print(book_sales_df)

    # Plot book sales count
    plt.figure(figsize=(10, 6))
    plt.bar(book_sales_df['Book'], book_sales_df['TotalSold'], color='orange')
    plt.title("Book Sales Count")
    plt.xlabel("Book")
    plt.ylabel("Total Sold")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Fetch genre-wise revenue
    genre_revenue_query = """
    SELECT G.GenreName AS Genre, SUM(OD.Subtotal) AS TotalRevenue
    FROM Genres G
    JOIN BookGenres BG ON G.GenreID = BG.GenreID
    JOIN OrderDetails OD ON BG.BookID = OD.BookID
    GROUP BY G.GenreID
    ORDER BY TotalRevenue DESC;
    """
    genre_revenue_df = fetch_data(genre_revenue_query)
    print("Genre-wise Revenue:")
    print(genre_revenue_df)

    # Plot genre-wise revenue
    plt.figure(figsize=(10, 6))
    plt.pie(
        genre_revenue_df['TotalRevenue'],
        labels=genre_revenue_df['Genre'],
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.tab20.colors
    )

    plt.title("Revenue by Genre")
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular
    plt.tight_layout()
    plt.show()

    # Sales by Month
    monthly_sales_query = """
       SELECT DATE_FORMAT(OrderDate, '%Y-%m') AS Month, SUM(TotalAmount) AS TotalSales
       FROM Orders
       GROUP BY Month
       ORDER BY Month;
       """
    monthly_sales_df = fetch_data(monthly_sales_query)
    print("Monthly Sales Breakdown:")
    print(monthly_sales_df)

    # Bar chart for monthly sales
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_sales_df['Month'], monthly_sales_df['TotalSales'], color='green')
    plt.title("Monthly Sales Breakdown")
    plt.xlabel("Month")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    def check_vendors_table():
        vendors_query = "SELECT * FROM Vendors;"
        vendors_df = fetch_data(vendors_query)
        if vendors_df.empty:
            print("The Vendors table is empty.")
        else:
            print("Contents of the Vendors Table:")
            print(vendors_df)

    # Call the function to check Vendors table
    check_vendors_table()

    # Sales by Vendor (Pie Chart for the latest month)
    vendor_sales_query = """
    SELECT V.CompanyName AS Vendor, SUM(VO.TotalCost) AS TotalSales
    FROM Vendors V
    JOIN VendorOrders VO ON V.VendorID = VO.VendorID
    WHERE VO.OrderDate >= '2024-01-01'  -- Use the latest relevant date
    GROUP BY V.VendorID
    ORDER BY TotalSales DESC;
    """

    # Fetch data and check for empty results
    vendor_sales_df = fetch_data(vendor_sales_query)
    if vendor_sales_df.empty:
        print("No vendor sales data available for the latest month. Please verify the query or the database contents.")
        return  # Exit the function to avoid further errors
    vendor_sales_df = fetch_data(vendor_sales_query)

    if not vendor_sales_df.empty:
        print("Vendor Sales Data:")
        print(vendor_sales_df)

        # Pie chart for vendor sales
        plt.figure(figsize=(8, 8))
        plt.pie(
            vendor_sales_df['TotalSales'],
            labels=vendor_sales_df['Vendor'],
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Paired.colors
        )
        plt.title("Vendor Sales Breakdown (2024)")
        plt.axis('equal')  # Equal aspect ratio ensures the pie is circular
        plt.tight_layout()
        plt.show()
    else:
        print("No vendor sales data available for the latest month.")

    # Time Series Plot for Monthly Sales
    def plot_time_series(monthly_sales_df):
        if monthly_sales_df.empty:
            print("No sales data available for the time series plot.")
            return

            # Convert 'Month' column to datetime for proper plotting
        monthly_sales_df['Month'] = pd.to_datetime(monthly_sales_df['Month'])

        # Sort data by month to ensure correct time order
        monthly_sales_df = monthly_sales_df.sort_values('Month')

        # Plotting
        plt.figure(figsize=(14, 8))
        plt.plot(
            monthly_sales_df['Month'],
            monthly_sales_df['TotalSales'],
            marker='o',
            color='teal',
            linestyle='-',
            linewidth=2,
            label="Monthly Sales"
        )

        # Beautify plot
        plt.title("Monthly Sales Trend", fontsize=18, fontweight='bold', color='darkblue')
        plt.xlabel("Month", fontsize=14, fontweight='bold')
        plt.ylabel("Total Sales ($)", fontsize=14, fontweight='bold')
        plt.grid(visible=True, linestyle='--', alpha=0.6)

        # Format x-axis with written month names
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%B %Y'))  # Month Year format
        plt.xticks(fontsize=10, rotation=45, ha='right')

        # Customize y-axis ticks
        plt.yticks(fontsize=12)

        # Add legend
        plt.legend(fontsize=12, loc='upper left')

        # Add a light background for better contrast
        plt.gca().set_facecolor('#f9f9f9')

        # Adjust layout
        plt.tight_layout()

        # Show plot
        plt.show()

    plot_time_series(monthly_sales_df)

    def plot_cumulative_sales(monthly_sales_df):
        if monthly_sales_df.empty:
            print("No data available for cumulative sales.")
            return

        monthly_sales_df['Month'] = pd.to_datetime(monthly_sales_df['Month'])
        monthly_sales_df = monthly_sales_df.sort_values('Month')
        monthly_sales_df['CumulativeSales'] = monthly_sales_df['TotalSales'].cumsum()

        plt.figure(figsize=(12, 6))
        plt.plot(
            monthly_sales_df['Month'],
            monthly_sales_df['CumulativeSales'],
            marker='o',
            color='purple',
            linewidth=2,
            label="Cumulative Sales"
        )
        plt.title("Cumulative Sales Over Time", fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel("Month", fontsize=14)
        plt.ylabel("Cumulative Sales ($)", fontsize=14)
        plt.grid(linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%B %Y'))
        plt.xticks(rotation=45, fontsize=10, ha='right')
        plt.tight_layout()
        plt.show()

    # Call this function
    plot_cumulative_sales(monthly_sales_df)

    def plot_genre_sales_heatmap():
        query = """
            SELECT 
                DATE_FORMAT(O.OrderDate, '%Y-%m') AS Month,
                G.GenreName AS Genre,
                SUM(OD.Subtotal) AS Revenue
            FROM Orders O
            JOIN OrderDetails OD ON O.OrderID = OD.OrderID
            JOIN Books B ON OD.BookID = B.BookID
            JOIN BookGenres BG ON B.BookID = BG.BookID
            JOIN Genres G ON BG.GenreID = G.GenreID
            GROUP BY Month, Genre
            ORDER BY Month, Genre;
        """
        genre_sales_df = fetch_data(query)

        if genre_sales_df.empty:
            print("No data available for heatmap.")
            return

        # Pivot data for heatmap
        heatmap_data = genre_sales_df.pivot(index='Genre', columns='Month', values='Revenue').fillna(0)

        heatmap_data = heatmap_data.apply(pd.to_numeric, errors='coerce')  # Convert to numeric, replace errors with NaN
        heatmap_data = heatmap_data.fillna(0)  # Replace NaN with 0 (or use another strategy based on your needs)

        # Create the heatmap
        plt.figure(figsize=(12, 8))
        plt.title("Heatmap of Monthly Sales by Genre", fontsize=16, fontweight='bold')
        sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Revenue ($)'})
        plt.xlabel("Month", fontsize=14)
        plt.ylabel("Genre", fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Call the function
    plot_genre_sales_heatmap()

    def plot_delivery_time_analysis():
        query = """
            SELECT 
                TIMESTAMPDIFF(DAY, OrderDate, DeliveryDate) AS DeliveryTime,
                V.CompanyName AS Vendor
            FROM VendorOrders VO
            JOIN Vendors V ON VO.VendorID = V.VendorID
            WHERE VO.OrderStatus = 'Received';
        """
        delivery_time_df = fetch_data(query)

        if delivery_time_df.empty:
            print("No data available for delivery time analysis.")
            return

        plt.figure(figsize=(12, 6))

        # Set Seaborn style
        sns.set(style="whitegrid")

        # Create the boxplot
        sns.boxplot(
            x='Vendor',
            y='DeliveryTime',
            data=delivery_time_df,
            palette="coolwarm",  # Change color palette for a better look
            width=0.5,  # Adjust box width
            fliersize=6,  # Adjust size of outliers
            linewidth=1.5  # Increase the line width of the boxes
        )

        # Title and labels styling
        plt.title(
            "Delivery Time Analysis by Vendor",
            fontsize=18,
            fontweight='bold',
            color='darkslategray',  # Use a darker color for readability
            pad=20
        )
        plt.xlabel("Vendor", fontsize=14, labelpad=10)
        plt.ylabel("Delivery Time (Days)", fontsize=14, labelpad=10)

        # Rotate and style x-ticks
        plt.xticks(rotation=45, fontsize=12, ha='right')

        # Add gridlines for better readability
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Clean up top and right spines for aesthetics
        sns.despine(top=True, right=True)

        # Adjust layout for better spacing
        plt.tight_layout()

        # Show the plot
        plt.show()

    # Call the function
    plot_delivery_time_analysis()

# Run the analysis
generate_plots_and_tables()
