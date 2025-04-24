"""
------------------------------------------------
OrderInfoSystem: Online Order Management App
Information system for an electronics store
Developed for procedural programming assignment
------------------------------------------------
"""

# Importing the csv module for reading and writing .csv files
import csv

# Set the Column headers
column_header = ["Order_ID", "Customer_Name", "Item_Purchased", "Qty", "Order_Date", "Total($)", "Status"]

# Empty Global Parallel Arrays (Columns)
order_id = []           # int: Unique order identifier
customer_name = []      # str: Name of the customer
item_purchased = []     # str: Item bought by the customer
quantity = []           # int: Number of items purchased
order_date = []         # datetime: Date of the order
total_price = []        # float: Total cost of the order
order_status = []       # str: Status like 'Shipped', 'Delivered', 'Cancelled'
records_loaded = False  # Track if CSV was loaded

# Function to clear old data if already loaded in the parallel array
def clear_array():
    global records_loaded
    order_id.clear()
    customer_name.clear()
    item_purchased.clear()
    quantity.clear()
    order_date.clear()
    total_price.clear()
    order_status.clear()
    records_loaded = False

# Function to load records
# Reads order data from the OrderDetails.csv file and loads it into the parallel arrays.
def load_records():

    global records_loaded

    try:

        # Open the csv file in to an object file
        with open('OrderDetails.csv', newline='') as csv_file_obj:

            #Read the object file
            csv_reader = csv.reader(csv_file_obj)

            # Skip the first row (header)
            next(csv_reader)

            # Clear old data if already loaded
            clear_array()

            # loop through the rest of the rows and stores in the parallel arrays
            for row in csv_reader:
                order_id.append(int(row[0]))
                customer_name.append(row[1])
                item_purchased.append(row[2])
                quantity.append(int(row[3]))
                order_date.append(row[4])
                total_price.append(float(row[5]))
                order_status.append(row[6])

        print("\nRecords successfully loaded from 'OrderDetails.csv'.")
        records_loaded = True
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        # Clear old data if already loaded
        clear_array()

# Function to display main menu
def display_menu():

    while True:
        print(f"\n{'Online Order Details':^25}  ")
        print("=" * 25)
        print(f"{'Main Menu':^25}  ")
        print("-" * 25)
        print("1. Load records")
        print("2. Display")
        print("3. Add record")
        print("4. Delete record")
        print("5. Save records")
        print("6. Exit")
        choice = input()

        if choice == "1":
            load_records()
        elif choice == "2":
            print("2")
        elif choice == "3":
            print("3")
        elif choice == "4":
            print("4")
        elif choice == "5":
            print("5")
        elif choice == "6":
            break
        else:
            print("Please enter valid number (1 - 6) from the menu.")


# To display main menu
display_menu()