import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    email TEXT,
    name TEXT,
    created_at TEXT
);

CREATE TABLE Orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    created_at TEXT,
    status TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    stock INTEGER
);

CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);
""")


cursor.executemany("INSERT INTO Users VALUES (?, ?, ?, ?)", [
    (1, 'anna@example.com', 'Anna', '2023-01-01'),
    (2, 'oleg@example.com', 'Oleg', '2023-02-10')
])

cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?)", [
    (1, 'Laptop', 1200.00, 10),
    (2, 'Mouse', 25.00, 100),
    (3, 'Keyboard', 45.00, 50)
])

cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?)", [
    (1, 1, '2023-05-10', 'completed'),
    (2, 1, '2023-05-12', 'pending'),
    (3, 2, '2023-06-01', 'completed')
])

cursor.executemany("INSERT INTO OrderItems VALUES (?, ?, ?, ?, ?)", [
    (1, 1, 1, 1, 1200.00),  
    (2, 1, 2, 2, 25.00),   
    (3, 3, 3, 3, 45.00)    
])

conn.commit()

query1 = """
SELECT 
    Users.name AS user_name,
    Orders.id AS order_id,
    SUM(OrderItems.quantity * OrderItems.unit_price) AS total_amount
FROM Orders
INNER JOIN Users ON Users.id = Orders.user_id
INNER JOIN OrderItems ON OrderItems.order_id = Orders.id
WHERE Orders.status = 'completed'
GROUP BY Users.name, Orders.id;
"""

query2 = """
SELECT 
    Products.name AS product_name,
    SUM(OrderItems.quantity) AS total_sold
FROM Products
INNER JOIN OrderItems ON OrderItems.product_id = Products.id
INNER JOIN Orders ON Orders.id = OrderItems.order_id
WHERE Orders.status = 'completed'
GROUP BY Products.name
HAVING SUM(OrderItems.quantity) > 1;
"""


def show_results(title, q):
    print(title)
    rows = cursor.execute(q).fetchall()
    for row in rows:
        print(row)
    print()

show_results("Результати SELECT #1 (до UPDATE)", query1)
show_results("Результати SELECT #2 (до UPDATE)", query2)

cursor.execute("UPDATE Orders SET status = 'completed' WHERE id = 2")
conn.commit()
print("UPDATE виконано! (Order #2 тепер completed)\n")

show_results("Результати SELECT #1 (після UPDATE)", query1)
show_results("Результати SELECT #2 (після UPDATE)", query2)

conn.close()
