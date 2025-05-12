"""
--------------------------------------------------------
Title       : OrderInfoSystem - Online Order Management App - Prototype
Contributors: Ramya Vegi, Nalini Rajaram
Created on  : 28-Apr-2025
Version     : 1.0
File        : orderform_prototype.py

Description :
This is a console-based information system developed as part of a
procedural programming assignment for an electronics store.

It uses parallel arrays to:
- Load data from a CSV file
- Display records in a formatted table

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

# call functions to load display csv file
load_records()

if not check_empty():
    display_records()
