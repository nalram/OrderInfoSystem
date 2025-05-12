"""
--------------------------------------------------------
Title       : OrderInfoSystem - Online Order Management App
Contributors: Ramya Vegi, Nalini Rajaram
Created on  : 30-Apr-2025
Version     : 1.0
File        : order_info_system.py

Description :
This is a console-based information system developed as part of a
procedural programming assignment for an electronics store.

It uses parallel arrays to:
- Load data from a CSV file
- Display records in a formatted table
- Add new customer orders
- Delete existing records
- Save updated records back to the CSV file

Developed using only procedural Python (no classes or OOP).
------------------------------------------------
"""

# --- Imports ---
import csv       # For reading and writing CSV files
import datetime  # For capturing the current date on new orders
import sys       # For exiting the application using sys.exit()

# --- Global Variables (Parallel Arrays) ---
# Each list represents one column of the order data table.
order_id = []                   # int: Unique order identifier
customer_name = []              # str: Name of the customer
item_purchased = []             # str: Item bought by the customer
quantity = []                   # int: Number of items purchased
order_date = []                 # datetime: Date of purchase in DD/MM/YYYY format
total_price = []                # float: Total cost of the order
order_status = []               # str: Status like 'Shipped', 'Delivered', 'Cancelled'

# Other global variables
column_header = ["Order_ID", "Customer_Name", "Item_Purchased",
                 "Qty", "Order_Date", "Total($)", "Status"] # Set the Column headers
file_name = 'OrderDetails.csv'  # The CSV file name used for persistence
records_loaded = False          # Flag to track whether data has been loaded to in-memory
records_not_saved = False       # Flag to track whether data added to in-memory has been saved to csv file
data_found = False              # A flag to check if any records exist in the csv file

def new_last_row_id():
    try:
        with open(file_name, mode='r', newline='') as csv_file_obj:
            csv_reader = list(csv.reader(csv_file_obj))  # Convert iterator to list

            if len(csv_reader) <= 1:
                get_new_order_id = 1001  # Only header or empty file
            else:
                last_row = csv_reader[-1]  # Last data row (not header)
                # Auto-generate a new Order ID
                get_new_order_id = int(last_row[0]) + 1

        return get_new_order_id

    except Exception as e:
        print(f"Error reading last row: {e}")
        return None

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
    global records_not_saved
    order_id.clear()
    customer_name.clear()
    item_purchased.clear()
    quantity.clear()
    order_date.clear()
    total_price.clear()
    order_status.clear()
    records_loaded = False
    records_not_saved = False

# Function to load records
# Reads order data from the OrderDetails.csv file and loads it into the parallel arrays.
def load_records():
    """
    Load order records from the CSV file into parallel arrays.
    If records already exist in-memory, they will be cleared first.
    Sets 'records_loaded' to True if successful.
    """

    global records_loaded
    global data_found

    # Check if there is unsaved data in memory before loading from the csv file
    if records_not_saved:
        while True:
            print("\nWARNING: You have unsaved records in memory.")
            confirm = input("Loading now will discard them. Do you want to proceed? (Y/N): ").strip().lower()
            if confirm == 'y':
                # Clear in-memory data
                break
            elif confirm == 'n':
                print("Loading cancelled. Returning to main menu.")
                return # Don't load records
            print("Invalid input. Please enter 'Y' for yes or 'N' for no.")

    try:

        # Open the csv file in to an object file
        with open(file_name, mode='r', newline='') as csv_file_obj:

            #Read the object file
            csv_reader = csv.reader(csv_file_obj)

            # Skip the first row (header)
            header = next(csv_reader, None)

            # Check for file empty
            if header is None:
                print("\nThe file is empty!")
            else:
                data_found = True

            # check if file not empty
            if data_found:

                # Clear in-memory data
                clear_array()

                row_count = 0  # Initialize row count

                # loop through the rest of the rows and stores in the parallel arrays
                for row in csv_reader:

                    # Set flag if at least one row is found
                    data_found = True

                    order_id.append(int(row[0]))
                    customer_name.append(row[1])
                    item_purchased.append(row[2])
                    quantity.append(int(row[3]))
                    order_date.append(row[4])
                    total_price.append(float(row[5]))
                    order_status.append(row[6])
                    row_count += 1  # Increment row count

                # Check if at least one record found after the header
                if data_found and row_count > 0:
                    print("\n" + str(row_count) + " records successfully loaded from 'OrderDetails.csv'.")
                    records_loaded = True
                else:
                    print("\nThe file has no data rows after the header.")

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

    global records_not_saved  # Flag to track whether data added to in-memory has been saved to csv file

    print("\nAdd New Order")
    print("-" * 30)

    # Auto-generate a new Order ID
    if order_id:
        new_id = order_id[-1] + 1 # Increment Order ID based on the last entry in the parallel array
    else:
        new_id = new_last_row_id() # If array is empty, get the last ID from the CSV file and increment

    # Get customer name
    while True:
        name = input("Enter customer name: ")
        # To check if customer name is empty
        if name.strip():
            break
        print("Customer name cannot be empty. Please try again.")

    # Get item purchased
    while True:
        item = input("Enter item purchased: ")
        # To check if item purchased is empty
        if item.strip():
            break
        print("Item purchased cannot be empty. Please try again.")

    # Get order quantity
    while True:
        try:
            qty = int(input("Enter quantity: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for quantity.")

    # Set order date to current system date
    date = datetime.datetime.now().strftime("%d/%m/%Y")

    # Get total price
    while True:
        try:
            price = float(input("Enter total price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for price.")

    """
    # Get Order status
    valid_status = ["Shipped", "Delivered", "Cancelled"]

    while True:
        status = input("Enter order status (Shipped/Delivered/Cancelled): ").strip().capitalize()
        if status in valid_status:
            break
        else:
            print("Invalid status. Please enter Shipped, Delivered, or Cancelled.")
    """

    # Display menu for selecting order status
    status_options = {
        "1": "Shipped",
        "2": "Delivered",
        "3": "Cancelled"
    }

    while True:
        print("\nSelect Order Status:")
        for key, value in status_options.items():
            print(f"{key}. {value}")

        choice = input("Enter the number corresponding to the status: ").strip()

        if choice in status_options:
            status = status_options[choice]
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # Append to the parallel array
    order_id.append(int(new_id))
    customer_name.append(name)
    item_purchased.append(item)
    quantity.append(qty)
    order_date.append(date)
    total_price.append(price)
    order_status.append(status)

    print("\nRecord added successfully!")
    records_not_saved = True

# Function to delete record
# Deletes a specific order from the arrays based on the entered Order ID.
def delete_record():

    global records_not_saved

    print("\nDelete Record")
    print("-" * 20)

    while True:
        try:
            del_order_id = int(input("Enter the Order ID to delete: ").strip())
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
            records_not_saved = True
        else:
            print("\nDeletion cancelled.")
    else:
        print(f"\nOrder ID: {del_order_id} not found.")

# Function to save records
# Saves all current records from the parallel arrays to OrderDetails.csv.
def save_records():

    global records_not_saved  # Flag to track whether data added to in-memory has been saved to csv file
    global data_found

    try:

        # Check opening file in write or append mode
        if not records_loaded and data_found:
            print("Note: Your new entries will be added to the existing records in the file.")
            set_file_mode = 'a' # Append mode if records were not loaded
        else:
            set_file_mode = 'w' # Overwrite mode if records were loaded

        with open(file_name, mode=set_file_mode, newline='') as csv_file_obj:
            csv_writer = csv.writer(csv_file_obj)

            # Write header only in write ('w') mode
            if set_file_mode == 'w':
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

        if set_file_mode == 'a':
            print("\nRecords successfully appended to 'OrderDetails.csv'.")
        else:
            print("\nRecords successfully saved to 'OrderDetails.csv'.")
        records_not_saved = False

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
        choice = input("Enter the number (1 - 6) corresponding to the menu: ").strip()
        #choice = input().strip()

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
            if not check_empty() or records_not_saved:
                save_records()
        elif choice == "6":

            while True:
                confirm = input("Are you sure you want to exit the application? (Y/N): ").strip().lower()
                if confirm == 'y':
                    # Clear in-memory data
                    clear_array()
                    sys.exit()  # Fully exits the program
                elif confirm == 'n':
                    print("Exit cancelled. Returning to main menu.")
                    break
                print("Invalid input. Please enter 'Y' for yes or 'N' for no.")
        else:
            print("Please enter valid number (1 - 6) from the menu.")

# To display main menu
display_menu()