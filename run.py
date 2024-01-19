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

COFFEE_LIST = ["Latte", "Americano", "Espresso", "Mocha", "Flat white", "Cappuccino", "Piccolo"]

def request_sales_data():
    """
    Request sales data input from the user
    """
    while True:
        print("Please enter your sales for today")

        print("Example: 11, 32, 24, 43, 33, 45, 10\n")

       
        input_data = []
        for coffee in COFFEE_LIST:
            coffee_sale = input("Enter sale value for today %s: " % coffee)
            input_data.append(coffee_sale)

        
        
        if data_confirmation(input_data):
            print("data is accepted and confirmed!")
            break

    return input_data

def request_cost_data():
    """
    Request cost data input from the user
    """
    while True:
        print("Please enter your cost")
        print("Example: 11, 32, 24, 43, 33, 45, 10\n")

       
        input_data = []
        for coffee in COFFEE_LIST:
            coffee_cost = input("Enter cost value for today %s: " % coffee)
            input_data.append(coffee_cost)

        
        
        if data_confirmation(input_data):
            print("data is accepted and confirmed!")
            break

    return input_data


def data_confirmation(values):
    """
    Here the length of the value imputed by the user should be thesame as the length of the 
    coffee list, if not it will raise ValueError and give opportunity to try again.
    """
    try:
        [int(value) for value in values]
        if len(values) != len(COFFEE_LIST):
            raise ValueError(
                f"length of the coffee list is expected, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"wrong data: {e}, please try again.\n")
        return False

    return True
    
def update_sales_worksheet(data):
    """
    Update sales worksheet by adding new row with the data provided
    """
    print("sales worksheet updating...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully")

def update_cost_worksheet(data):
    """
    Update cost worksheet by adding new row with the data provided
    """
    print("cost worksheet updating...\n")
    cost_worksheet = SHEET.worksheet("cost")
    cost_worksheet.append_row(data)
    print("cost worksheet updated successfully\n")


def calculate_profit(sales_data, cost_data):
    """
    Here we are comparing the cost with the sales of each kind of coffee 
    Profit here will be the difference between the sales and the cost
    (Profit = S.L - C.P)
    The negative numbers will mean a loss for that particular cofee
    """
    profit_data = [int(sales_data[i]) - int(cost_data[i]) for i in range(len(sales_data))]
    
    return profit_data

def update_profit_worksheet(profit_data):
    """
    Update profit worksheet by adding new row with the profit calculated
    """
    print("profit worksheet updating...\n")
    update_profit_worksheet = SHEET.worksheet("profit")
    update_profit_worksheet.append_row(profit_data)
    print("profit worksheet updated successfully\n")
    print("Now let's see the profit list: \n")

def print_profit_data(profit_data):
    # print(profit_data)
    for index, profit in enumerate(profit_data):
        if profit > 0:
            print(
                "You are making profit of $%s by selling %s"
                % (profit, COFFEE_LIST[index])
            )
        elif profit >= 0:
            print(
                 "You are making  no profit: what you get is $%s by selling %s"
                % (profit, COFFEE_LIST[index])
            )
        else:
            print(
                "You are making loss of $%s by selling %s"
                % (profit, COFFEE_LIST[index])
            )


def getting_last_7_entries_sales():
    """
    Getting sales data for the last seven days
    """
    print("data on last 7 days of sales_data...\n")
    sales = SHEET.worksheet("sales")

    columns = []
    for num in range (1, 8):
        column = sales.col_values(num)
        columns.append(column[-7:])

    return columns


def main():
    """
    All program functions runs here
    """
    sales_data = request_sales_data()
    cost_data = request_cost_data()
   
    update_sales_worksheet(sales_data)
    update_cost_worksheet(cost_data)

    profit_data = calculate_profit(sales_data, cost_data)
    update_profit_worksheet(profit_data)

    print_profit_data(profit_data)
    sales_columns = getting_last_7_entries_sales()
    print(sales_columns)
    
    
    

    #input("Enter the no. of days for which you want to see the data: ")
    #input("What data you need? sales/cost/profit?")

    


if __name__ == "__main__":
    main()

    



