import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
    
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
sales = SHEET.worksheet('sales')

def get_sales_data():
    '''
    Get sales figures input from the user.
    Will run a while loop to repeatedly request data until the data entered is valid.
    '''
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        #print(f"The data provided is {data_str}") was used to test code prior to declaring sales_data
        sales_data = data_str.split(",")
        #print(sales_data) was used to test code prior to declaring the validate_data Function
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data
    

def validate_data(values):
    '''
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    '''
    #print(values) was used to test code before we added the Try Except Statement
    try:
        [int(value) for value in values]   # This is a List Comprehension! If value is not an integer it will return a ValueError
        if len(values) != 6:
            raise ValueError(
            f"Exactly 6 values required, you provided {len(values)}"
        )
    except ValueError as e:
        print(f"Invalid Data: {e}, please try again.\n")
        return False
    return True

'''
def update_sales_worksheet(data):
    ***
    Update sales Worksheet, add a new row with the list data provied.
    ***
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def update_surplus_worksheet(surplus_update): #attribute surplus_update could have been left as data the same as the update_sales_worksheet function attribute.
    ***
    Update surplus Worksheet, add a new row with the surplus data provied.
    ***
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(surplus_update)
    print("Surplus worksheet updated successfully.\n")
'''

# The 2 Functions above have been refactored into 1 new function below: update_worksheet

def update_worksheet(data, worksheet):
    '''
    Receives a list of integers to be inserted into a worksheet.
    Updates the relevant worksheet with the data provided.
    '''
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully!\n")


def calculate_surplus_data(sales_row):
    '''
    Compare sales with stock and calculate the surplus for each item type
    '''
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    pprint(stock) # can be removed but was used to check that stock levels are being pulled over from the worksheet.
    stock_row = stock[-1]
    print("Please wait...")
    print(f"The last stock entry was: {stock_row}")
    print(f"The last Sales entry was: {sales_row}")

    surplus_data = []
    for stock, sales in  zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    print(surplus_data)
    return surplus_data


def get_last_5_entries_sales():
    '''
    collects columns of data from sales worksheet, collecting the last
    5 entries for each sandwich and returns the data as a list of lists.
    '''
    sales = SHEET.worksheet("sales")
    #column = sales.col_values(3)
    #print(column)

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    #pprint(columns) Used to check if was pulling only 5 values from sales worksheet
    return columns

def main():
    data = get_sales_data()
    #print(data)  was used to check data type. Was string data and needs to be integer
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    #calculate_surplus_data(sales_data) after we added the return surplus data to line 82 we changed this line to the line below
    new_surplus_data = calculate_surplus_data(sales_data)
    #print(new_surplus_data) # with this we could remove lines 71-75
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches Data Automation.\n")
#main()

sales_columns = get_last_5_entries_sales()
