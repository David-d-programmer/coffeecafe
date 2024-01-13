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
    request sales data input from the user
    """

    print("Please enter sales data from the last market")
    print("Data should be seven numbers, separated by commas")
    print("Example: 11, 32, 24, 43, 33, 45, 10\n")

    input_data = input("Enter your data here: ")
    
    sales_data = input_data.split(",")
    data_confirmation(sales_data)

def data_confirmation(values):
    """
    In the try, all string values are converted into integer.
    also raises ValueError if string cannot be converted to integer
    or if they are not exactly 7 values.
    """
    try:
        if len(values) != 7:
            raise ValueError(
                f"exactly 7 values is expected, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"wrong data: {e}, please try again.\n")

request_sales_data()


