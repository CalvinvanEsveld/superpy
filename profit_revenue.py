import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import os

now = datetime.now()
today = now.strftime("%Y-%m-%d")
now_min_one = now - timedelta(days = 1)
yesterday = now_min_one.strftime("%Y-%m-%d")
now_min_two = now - timedelta(days = 2)
day_before_yesterday = now_min_two.strftime("%Y-%m-%d")


current_dir = os.getcwd()
#This function will calculate the profit of today, yesterday or over a period of time.
def profit(period):
    profits = []
    dates = []
    with open(f'{current_dir}/sold.csv', 'r') as file1:
        reader1 = csv.reader(file1)
        next(reader1)
        sold_data = list(reader1)

    with open(f'{current_dir}/bought.csv', 'r') as file2:
        reader2 = csv.reader(file2)
        next(reader2)
        bought_data = list(reader2)

    for row1 in sold_data:
        for row2 in bought_data:
            if row1[1][:7] == period: #If period (in format mm-yyyy) add sell_price are equal, add sell_price to list1 and date to dates.
                if row1[0] == row2[0]: #Checking if product ID's match.
                    sub = float(row1[2]) - float(row2[4])
                    profits.append(sub)
                    dates.append(row1[1][5:])
            elif row1[1] == period: #If sell_date is equal to today or yesterday, add sell_price to list1.
                if row1[0] == row2[0]:
                    sub = float(row1[2]) - float(row2[4])
                    profits.append(sub)

    #Sum of list1 rounded to 2 decimals.
    sum_of_profits = sum(profits)
    sum_of_profits_rounded = round(sum_of_profits, 2)

    if period == today:
        return f'Profit of today is: €{sum_of_profits_rounded}'
    elif period == yesterday:
        return f'Profit of yesterday is: €{sum_of_profits_rounded}'
    else:
        date_object = datetime.strptime(period, "%Y-%m")
        new_date = datetime.strftime(date_object, "%B %Y")
        total_profit = f'Profit of {new_date} is: €{sum_of_profits_rounded}'   
    
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, '%m-%d'))

    #This will show a graph of profit made over a period of time.
    plt.style.use('fivethirtyeight')    
    plt.plot(sorted_dates, (list(map(float, profits))))    
    plt.xlabel('Days')
    plt.ylabel('(EURO)')
    plt.title(total_profit)
    plt.show()


#This function will calculate the revenue of today, yesterday over a period of time.
def revenue(period):
    revenues = []
    dates = []        
    with open(f'{current_dir}/sold.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)                
        for line in reader:            
            if line[1][:7] == period: #If period (in format mm-yyyy) add sell_price are equal, add sell_price to list1 and date to dates.
                revenues.append(line[2])
                dates.append(line[1][5:])
            elif line[1] == period: #If sell_date is equal to today or yesterday, add sell_price to list1.
                revenues.append(line[2])
            
        sum_of_revenues = sum(map(float, revenues))
        sum_of_revenues_rounded = round(sum_of_revenues, 2) 

        if period == today:
            return f'Revenue of today is: €{sum_of_revenues_rounded}'
        elif period == yesterday:
            return f'Revenue of yesterday is: €{sum_of_revenues_rounded}'
        else:
            date_object = datetime.strptime(period, "%Y-%m")
            new_date = datetime.strftime(date_object, "%B %Y")            
            total_revenue = f'Revenue of {new_date} is: €{sum_of_revenues_rounded}'
    
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, '%m-%d')) #Sorting dates in list dates just in case.
    
    #This will show a graph of revenue made over a period of time.
    plt.style.use('fivethirtyeight')    
    plt.plot(sorted_dates, (list(map(float, revenues))))    
    plt.xlabel('Days')
    plt.ylabel('(EURO)')
    plt.title(total_revenue)
    plt.show()

#This function will show a graph of the profit and revenue made over a period of time.
def profit_revenue(period):
    revenues = []
    profits = []
    dates = []

    #This will add the dates to the list dates and add the revenue made over a period of time to list1    
    with open(f'{current_dir}/sold.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)                
        for line in reader:            
            if line[1][:7] == period: #If period (in format mm-yyyy) add sell_price are equal, add sell_price to list1 and date to dates.
                revenues.append(line[2])
                dates.append(line[1][5:])

    #This will calulate the profit made over a period of time and add it to list2.
    with open(f'{current_dir}/sold.csv', 'r') as file1:
        reader1 = csv.reader(file1)
        next(reader1)
        data1 = list(reader1)

    with open(f'{current_dir}/bought.csv', 'r') as file2:
        reader2 = csv.reader(file2)
        next(reader2)
        data2 = list(reader2)

    for row1 in data1:
        for row2 in data2:
            if row1[1][:7] == period:
                if row1[0] == row2[0]:
                    sub = float(row1[2]) - float(row2[4])
                    profits.append(sub)

    sum_of_revenues = sum(map(float, revenues))
    sum_of_revenues_rounded = round(sum_of_revenues, 2)

    sum_of_profits = sum(profits)
    sum_of_profits_rounded = round(sum_of_profits, 2)

    date_object = datetime.strptime(period, "%Y-%m")
    new_date = datetime.strftime(date_object, "%B %Y")
    total = f'Profit and Revenue of {new_date}'

    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, '%m-%d'))
    
    #This will show a graph of profit and revenue made over a period of time.
    plt.style.use('fivethirtyeight')
    plt.plot(sorted_dates, (list(map(float, profits))), label= f'Profit €{sum_of_revenues_rounded}')
    plt.plot(sorted_dates, (list(map(float, revenues))), label= f'Revenue €{sum_of_profits_rounded}')    
    plt.xlabel('Days')
    plt.ylabel('(EURO)')
    plt.title(total)
    plt.legend()
    plt.show()





