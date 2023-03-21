# Imports
import argparse
import csv
import os
from datetime import datetime, timedelta
import pandas as pd
from rich import print
from rich_tools import df_to_table
from profit_revenue import profit_revenue, profit, revenue
from export import export_data

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='action', metavar='', description='valid subcommands', help='Actions you want to take')

#These are the commandline arguments for buying a product.
parser_buy = subparsers.add_parser('buy', help='Buy a product')
parser_buy.add_argument('--product_name', metavar='', help='Enter product name')
parser_buy.add_argument('--count', metavar='', help="Number of products")
parser_buy.add_argument('--buy_date', metavar='', required=False, help="The date the product was bought format: YYYY-MM-DD")
parser_buy.add_argument('--buy_price', metavar='', type=float, help="The price the product was bought for")
parser_buy.add_argument('--expiration_date', metavar='', help="The expiration date of the product format: YYYY-MM-DD")

#These are the commandline arguments for selling a product.
parser_sell = subparsers.add_parser('sell', help='Sell a product')
parser_sell.add_argument('--id', metavar='', help="Bought product ID")
parser_sell.add_argument('--sell_date', metavar='', help="Date product sold")
parser_sell.add_argument('--sell_price', type=float, metavar='', help="Selling price")

#This is the commandline argument for showing the inventory report.
parser_report = subparsers.add_parser('report', help='Show inventory report')

#These are the commandline arguments for advancing time.
parser_advance_time = subparsers.add_parser('advance-time', help='Advance time')
parser_advance_time.add_argument('--day', metavar='', help="Advancing time by 1 or 2 days")

#These are the commandline arguments for exporting data from one csv file to another csv file.
parser_export_data = subparsers.add_parser('export-data', help='Export data from report.csv to a destination file based on product name')
parser_export_data.add_argument('--source', metavar='', help="The path of de source csv file with data")
parser_export_data.add_argument('--destination', metavar='', help="The path of de destination csv file")
parser_export_data.add_argument('--product_name', metavar='', help='Enter product name')

#These are the commandline arguments for time period for revenue, profit and profit and revenue.
#Show revenue
parser_report_revenue = subparsers.add_parser('report-revenue', help='Will show revenue of today, yesterday or over a period of time')
parser_report_revenue.add_argument('--period', metavar='', help="Time period: today, yesterday or date format: 2023-03")
#Show profit
parser_report_profit = subparsers.add_parser('report-profit', help='Will show profit of today, yesterday or over a period of time')
parser_report_profit.add_argument('--period', metavar='', help="Time period: today, yesterday or date format: 2023-03")
#Show profit and revenue over a period of time.
parser_profit_revenue = subparsers.add_parser('profit-revenue', help='Will show profit of today, yesterday or over a period of time')
parser_profit_revenue.add_argument('--period', metavar='', help="Time period: today, yesterday or date format: 2023-03")
args = parser.parse_args()

current_dir = os.getcwd()
#This will create the bought.csv file if not exists.
if not os.path.exists(f'{current_dir}/bought.csv'):

    header = ['id', 'product_name', 'count', 'buy_date', 'buy_price', 'expiration_date']
 
    with open('bought.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(header)

#This will create the report.csv file if not exsists.
if not os.path.exists(f'{current_dir}/report.csv'):

    header = ['id', 'product_name', 'count', 'buy_price', 'expiration_date']

    with open('report.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(header)

#This will create the sold.csv file if not exists.
if not os.path.exists(f'{current_dir}/sold.csv'):

    header = ['bought_id', 'sell_date', 'sell_price']

    with open('sold.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(header)


#This function lets us add products to the bought.csv and report.csv file with ID's.
def bought(product_name, count, buy_date, buy_price, expiration_date):
    
    with open(f'{current_dir}/bought.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        last_id = 0
        for line in reader:            
            if line != []:
                last_id = int(line[0])
        new_id = last_id + 1

    with open(f'{current_dir}/bought.csv', 'a') as file1, open(f'{current_dir}/report.csv', 'a') as file2:
        writer1 = csv.writer(file1)
        writer2 = csv.writer(file2)
        writer1.writerow([new_id, product_name, count, buy_date, buy_price, expiration_date])
        writer2.writerow([new_id, product_name, count, buy_price, expiration_date])



    #This will show a table of report.csv
    data = pd.read_csv(f'{current_dir}/report.csv')
    table = df_to_table(data)
    return print(table)


#This function lets us delete products that are expired, the products that are not expired are removed from inventory and added to sold.py.
def sell(id, sell_date, sell_price):     
    product_ids = []
    report_rows = []    
    with open(f'{current_dir}/report.csv', 'r') as readFile:
        reader = csv.reader(readFile)        
        for row in reader:
            report_rows.append(row)
            product_ids.append(row[0])                                
            if row[0] == id:                
                date = datetime.strptime(row[4], "%Y-%m-%d")                   
                if date <= datetime.now(): # If expiration date in report.csv is less or equal than current date, product is expired and will be removed from report.csv and will not be added to sold.csv
                    report_rows.remove(row)
                    print('Product is expired!')
                elif date >= datetime.now(): #If not, product will be removed from report.csv and will be added to sold.csv
                    with open(f'{current_dir}/report.csv', 'r') as readFile:
                        reader = csv.reader(readFile)                                    
                        for row in reader:                          
                            if row[0] == id:
                                report_rows.remove(row)
                                with open(f'{current_dir}/sold.csv', 'a') as file:
                                    writer = csv.writer(file)       
                                    writer.writerow([id, sell_date, sell_price])
                                        
        if id not in product_ids: #If product not in stock. Show message
                print('Product not in stock')

        #This will write the list csv_rows in report.csv
        with open(f'{current_dir}/report.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(report_rows)


#These variables are used for the funcions advance_time, revenue and profit.
now = datetime.now()
today = now.strftime("%Y-%m-%d")
now_min_one = now - timedelta(days = 1)
yesterday = now_min_one.strftime("%Y-%m-%d")
now_min_two = now - timedelta(days = 2)
day_before_yesterday = now_min_two.strftime("%Y-%m-%d")



#This function will advance time by 1 or 2 days. (yesterday or the day before yesterday)
def advance_time(day):
    bought_rows = []
    report_rows = []
    with open(f'{current_dir}/sold.csv', 'r') as source:
        reader = csv.reader(source)
        next(reader)       
        for sell_row in reader:
            if sell_row[1] > day: #If date in sell.csv is higher or equal to day('1'= yesterday, '2'= day_before_yesterday).
                 with open(f'{current_dir}/bought.csv', 'r') as source:
                    reader = csv.reader(source)
                    next(reader)
                    for bought_row in reader:
                        if sell_row[0] == bought_row[0]:#IF ID's of both files match, it will remove the buy_date of the product so the rows will match with the columns in report.csv.
                            bought_row.pop(3)
                            bought_rows.append(bought_row)               
    
    with open(f'{current_dir}/report.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            report_rows.append(line)
                
    #This will add the list rows to report.csv
    if line not in bought_rows:
        with open(f'{current_dir}/report.csv', 'a') as destination:
            writer = csv.writer(destination)
            for row in bought_rows:
                writer.writerow(row)

    #This will show a table of report.csv
    data = pd.read_csv(f'{current_dir}/report.csv')
    table = df_to_table(data)
    return print(table)


#This function will show an inventory report of products currently in stock.    
def report_inventory():    
    sold_rows = []
    report_rows = []
    with open(f'{current_dir}/sold.csv', 'r') as file1:
        reader1 = csv.reader(file1)
        next(reader1)
        for line1 in reader1:
            sold_rows.append(line1)
        
    with open(f'{current_dir}/report.csv', 'r') as file2:
        reader2 = csv.reader(file2)
        next(reader2)
        for line2 in reader2:
            report_rows.append(line2)

    #Checking if the products that are sold up to and including today will be removed from report.csv after the function advance_time has been used.
    for line1 in sold_rows:
        for line2 in report_rows:
            if line1[0] == line2[0]:
                report_rows.remove(line2)

    #Writing rows in report_rows to report.csv.
    with open(f'{current_dir}/report.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['id','product_name','count','buy_price','expiration_date'])
        writer.writerows(report_rows)

    #This will show a table of report.csv
    data = pd.read_csv(f'{current_dir}/report.csv')
    table = df_to_table(data)
    return print(table)


if __name__ == "__main__":
    if args.action == "buy":
        bought(args.product_name, args.count, args.buy_date, args.buy_price, args.expiration_date)
    elif args.action == "sell":
        sell(args.id, args.sell_date, args.sell_price)
    elif args.action == "report":
        report_inventory()
    elif args.action == "advance-time":
        if args.day == '1':
            advance_time(yesterday)
        elif args.day == '2':
            advance_time(day_before_yesterday)
    elif args.action == 'export-data':
        export_data(args.source, args.destination, args.product_name)
    elif args.action == "report-revenue":
        if args.period == "today":
            print(revenue(today))
        elif args.period == "yesterday":
            print(revenue(yesterday))
        else:
            revenue(args.period)
    elif args.action == "report-profit":
        if args.period == "today":
            print(profit(today))
        elif args.period == "yesterday":
            print(profit(yesterday))
        else:
            profit(args.period)
    elif args.action == 'profit-revenue':
        profit_revenue(args.period)
    

    



 
