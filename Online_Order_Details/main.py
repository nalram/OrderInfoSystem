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

# Function to check for empty array before performing display / delete / save operations
def check_empty():

    # Check for empty array
    if not order_id:
        print("No records found. Please add or load records first.")
        return True  # It is empty
    return False     # It is not empty

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

# Function to display records
# Displays all order records from the parallel array on to the screen in a formatted table.
def display_records():

    # Print  Application Title
    print(f"\n{'Online Order Details':^100}")
    print("=" * 110)

    # Print column headers
    print(f"{column_header[0]:>8}  {column_header[1]:<25} {column_header[2]:<25} "
          f"{column_header[3]:>5}  {column_header[4]:<12} {column_header[5]:>10}  {column_header[6]:<12}")
    print("-" * 110)

    # Print each row
    for i in range(len(order_id)):
        # Format:
        print(f"{order_id[i]:>8d}  "
              f"{customer_name[i][:24]:<25} "
              f"{item_purchased[i][:24]:<25} "
              f"{quantity[i]:>5d}  "
              f"{order_date[i]:<12} "
              f"{total_price[i]:>10.2f}  "
              f"{order_status[i][:14]:<15}")

# Function to add record
# Allows the user to input a new order and appends it to the parallel arrays.
def add_record():

    print("\nAdd New Order")
    print("-" * 30)

    # Auto-generate a new Order ID
    new_id = order_id[-1] + 1 if order_id else 1001  # start from 1001 if empty

    # Get user input for each field
    name = input("Enter customer name: ")
    item = input("Enter item purchased: ")

    while True:
        try:
            qty = int(input("Enter quantity: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for quantity.")

    date = input("Enter order date (DD-MM-YYYY): ")

    while True:
        try:
            price = float(input("Enter total price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for price.")

    status = input("Enter order status (Shipped/Delivered/Cancelled): ")

    # Append to the parallel array
    order_id.append(new_id)
    customer_name.append(name)
    item_purchased.append(item)
    quantity.append(qty)
    order_date.append(date)
    total_price.append(price)
    order_status.append(status)

    print("\nRecord added successfully!")


# Function to delete record
# Deletes a specific order from the arrays based on the entered Order ID.
def delete_record():

    print("\nDelete Record")
    print("-" * 20)

    while True:
        try:
            del_order_id = int(input("Enter the Order ID to delete: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for Order ID.")

    if del_order_id in order_id:
        index = order_id.index(del_order_id)

        # Show the record details before confirming deletion
        print("\nRecord to be deleted:")
        print("-" * 80)
        print(f"Order ID   : {order_id[index]}")
        print(f"Customer   : {customer_name[index]}")
        print(f"Item       : {item_purchased[index]}")
        print(f"Quantity   : {quantity[index]}")
        print(f"Date       : {order_date[index]}")
        print(f"Total Price: {total_price[index]:.2f}")
        print(f"Status     : {order_status[index]}")
        print("-" * 50)

        confirm = input("Are you sure you want to delete this record? (Y/N): ").strip().lower()
        if confirm == 'y':
            # Remove the item at the same index from all parallel arrays
            order_id.pop(index)
            customer_name.pop(index)
            item_purchased.pop(index)
            quantity.pop(index)
            order_date.pop(index)
            total_price.pop(index)
            order_status.pop(index)

            print(f"\nOrder ID: {del_order_id} deleted successfully!")
        else:
            print("\nDeletion cancelled.")
    else:
        print(f"\nOrder ID: {del_order_id} not found.")

# Function to save records
# Saves all current records from the parallel arrays to OrderDetails.csv.
def save_records():

    if not records_loaded:
        print("You haven't loaded the existing records.")
        confirm = input("Saving now will overwrite the file and keep only current records. Continue? (Y/N): ").strip().lower()
        if confirm != 'y':
            print("Save cancelled.")
            return

    try:
        with open('OrderDetails.csv', mode='w', newline='') as csv_file_obj:
            csv_writer = csv.writer(csv_file_obj)

            # Write the header row
            csv_writer.writerow(column_header)

            # Write each row from parallel arrays
            for i in range(len(order_id)):
                csv_writer.writerow([
                    order_id[i],
                    customer_name[i],
                    item_purchased[i],
                    quantity[i],
                    order_date[i],
                    total_price[i],
                    order_status[i]
                ])

        print("\nRecords successfully saved to 'OrderDetails.csv'.")

    except Exception as e:
        print(f"\nError saving records: {e}")


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
            if not check_empty():
                display_records()
        elif choice == "3":
            add_record()
        elif choice == "4":
            if not check_empty():
                delete_record()
        elif choice == "5":
            if not check_empty():
                save_records()
        elif choice == "6":
            break
        else:
            print("Please enter valid number (1 - 6) from the menu.")


# To display main menu
display_menu()