import csv


#This function will export data from report.csv to a destination file based on a product name.
def export_data(source, destination, condition):
    
    with open(source, 'r') as source_file:
        reader = csv.reader(source_file)
        data = list(reader)

    # Filter the data based on the condition
    export_data = [row for row in data if condition in row[1]]
    report = ['id','product_name','count','buy_price','expiration_date']

    # Open the destination CSV file and write the export data
    with open(destination, 'w', newline='') as destination_file:
        writer = csv.writer(destination_file)        
        writer.writerow(report)
        writer.writerows(export_data)
        

if __name__ == 'main':
    export_data()