import sys
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("coffee_cafe")

COFFEE_LIST = [
    "Latte",
    "Americano",
    "Espresso",
    "Mocha",
    "Flat white",
    "Cappuccino",
    "Piccolo",
]


def request_sales_data():
    """
    Request sales data input from the user
    """
    while True:
        print("Please! enter your sales for today")

        print("Example: latte 20")

        input_data = []
        for coffee in COFFEE_LIST:
            coffee_sale = input("Enter sales value for today %s: " % coffee)
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
        print("Please! enter your cost for today")
        
        print("Example: americano 60")

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


def update_worksheet(data, worksheet):
    """
    Accepts the list of data to  be updated in the worksheet
    updates the worksheet with the data provided.
    """
    print(f"cost {worksheet} worksheet updating...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_profit(sales_data, cost_data):
    """
    Here we are comparing the cost with the sales of each kind of coffee
    Profit here will be the difference between the sales and the cost
    (Profit = S.L - C.P)
    The negative numbers will mean a loss for that particular cofee
    """
    profit_data = [
        int(sales_data[i]) - int(cost_data[i]) for i in range(len(sales_data))
    ]

    return profit_data


def print_profit_data(profit_data):
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


def display_past_data(no_of_days):
    """
    Getting sales data for the past given no of days.
    """
    print(f"data on last {no_of_days} days of sales_data...\n")
    sales = SHEET.worksheet("sales")
    cost = SHEET.worksheet("cost")
    profit = SHEET.worksheet("profit")

    sales_data = sales.get_all_values()[1:]
    cost_data = cost.get_all_values()[1:]
    profit_data = profit.get_all_values()[1:]

    no_of_days_in_sheet = len(sales_data)
    final_no_of_days = (
        no_of_days if no_of_days < no_of_days_in_sheet else no_of_days_in_sheet
    )
    start_index = no_of_days_in_sheet - final_no_of_days

    sales_data = sales_data[start_index:]
    cost_data = cost_data[start_index:]
    profit_data = profit_data[start_index:]
    

    table = []
    for d in range(final_no_of_days):
        sales = sales_data[d]
        cost = cost_data[d]
        profit = profit_data[d]
        table.append([f"Day {d+1}"] + sales)
       
    print(tabulate(table, headers=COFFEE_LIST))


def get_todays_data():
    """
    where all our function runs!
    """
    sales_data = request_sales_data()
    cost_data = request_cost_data()

    profit_data = calculate_profit(sales_data, cost_data)
    update_worksheet(profit_data, "profit")
    
    update_worksheet(sales_data, "sales")
    update_worksheet(cost_data, "cost")
    

    

    print_profit_data(profit_data)


_USER_OPTIONS = """
1. Enter today's sales and cost data.
2. View last 7 days records
3. View last 30 days records
4. Enter custom days to see past data.
5. Exit
"""


def main():
    """
    A loop to always give us the list of options we have.
    """
    while True:
        user_input = input(_USER_OPTIONS)

        if user_input == "1":
            get_todays_data()
        elif user_input == "2":
            display_past_data(no_of_days=7)
        elif user_input == "3":
            display_past_data(no_of_days=30)
        elif user_input == "4":
            no_of_days = input(
                "Enter no. of days for which you want to see the data:"
            )

            invalid = True
            while invalid:
                try:
                    no_of_days = int(no_of_days)
                    invalid = False
                except ValueError:
                    print("Invalid input.. Please try again..")

            display_past_data(no_of_days=no_of_days)
        elif user_input == "5":
            sys.exit()

    
if __name__ == "__main__":
    main()
