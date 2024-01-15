import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('coffee_cafe')

def request_sales_data():
    """
    Request sales data input from the user
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be seven numbers, separated by commas")
        print("Example: 11, 32, 24, 43, 33, 45, 10\n")

        input_data = input("Enter your data here: ")
        
        sales_data = input_data.split(",")
        if data_confirmation(sales_data):
            print("data is accepted and confirmed!")
            break

    return sales_data

def data_confirmation(values):
    """
    In the try, all string values are converted into integer.
    also raises ValueError if string cannot be converted to integer
    or if they are not exactly 7 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 7:
            raise ValueError(
                f"exactly 7 values is expected, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"wrong data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    Updating sales worksheet in the new role with the data provided
    """
    print("Sales worksheet updating...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_profit(sales_row):
    """
    Here we are comparing the cost with the sales of each kind of coffee 
    Profit here will be the difference between the sales and the cost
    (Profit = S.L - C.P)
    The negative numbers will mean a loss for that particular cofee
    """
    print("Calculating the profit data...\n")
    cost = SHEET.worksheet("cost").get_all_values()
    cost_row = cost[-1]
    print(cost_row)

def main():
    """
    All program functions runs here
    """
    data = request_sales_data()
    sales_data = [int(numbers) for numbers in data]
    update_sales_worksheet(sales_data)
    calculate_profit(sales_data)

main()

