import csv
from dhooks import Webhook, File

CSV_dict = {}
RSI_dict_over = {}
RSI_difference = {}

#Fetches data from CSV and outputs it in CSV_dict
def extract_CSV(filename): 
    i = 0

    with open(filename, 'r') as csvfile:
        csvfile = csv.reader(csvfile)
        for row in csvfile:
            i+=1

            if i == 1: #ignores first line (contains items signification)
                continue

            CSV_dict[i] = row
            #RSI_dict[i] = row[0], row[8], row[4]

#Exctracts RSI breakpoints with timestamp using previously RSI extracted data
def extract_RSI_over():
    for i in CSV_dict.keys():
        values = float(CSV_dict[i][8])
        if values >= 80 or values <= 20:
            RSI_dict_over[i] = CSV_dict[i][0], CSV_dict[i][8]

#Exctracts the RSI difference between breakpoint and 6 hours later
def extract_difference():
    i = 0
    x = 1

    for irsi in RSI_dict_over.keys():
        #Gets breakpoint RSI
        OVER_RSI = RSI_dict_over[irsi][1]
        #Gets breakpoint timestamp
        irsi_timestamp = float(RSI_dict_over[irsi][0])

        for icsv in CSV_dict.keys():
            #Gets RSI from current CSV index
            CSV_RSI = CSV_dict[icsv][8]
            #Gets timestamp from current CSV index
            icsv_timestamp = float(CSV_dict[icsv][0])

            #Checks if current CSV index's timestamp is 6 hours later than breakpoint's timestamp
            if icsv_timestamp == irsi_timestamp+(21600):
                i+=1

                RSI_difference[i] = OVER_RSI, CSV_RSI

def compare_RSI():
    percentages_over = []
    percentages_under = []

    average_over = 0.0
    average_under = 0.0

    percentage = 0.0

    #Calculates the difference percentage between breakpoint RSI and 6H later RSI
    for i in RSI_difference.keys():
        a = float(RSI_difference[i][0])
        b = float(RSI_difference[i][1])

        #If it breaks over 80
        if float(RSI_difference[i][0]) >= 80:
            percentage = (a-b)/((a+b)/2)*100
            
            percentages_over.append(percentage)

        #If it breaks under 20
        if float(RSI_difference[i][0]) <= 20:
            percentage = (a-b)/((a+b)/2)*100

            percentages_under.append(percentage)

    #Calculates the average using recorded differences percentages 
    for i in range(len(percentages_over)):
        average_over += percentages_over[i]

    for i in range(len(percentages_under)):
        average_under += percentages_under[i]

    average_over /= len(percentages_over)
    average_under /= len(percentages_under)

    #Converts negative results to positive floats
    if average_under < 0:
        average_under = abs(average_under)
    elif average_over < 0:
        average_over = abs(average_over)

    #Prints the results
    print('Over 80: ' + str(int(average_over)) + '%')
    print('Under 20: ' + str(int(average_under)) + '%')

#Sends data to webhook
def send_webhook(webhookURL, fileName):
    hook = Webhook(webhookURL)
    to_txt = ""

    for i in RSI_difference.keys():
        to_txt += str(i) + ": " + RSI_difference[i][0] + " / " + RSI_difference[i][1] + "\n"

    with open("log.txt", "w") as f:
        f.write(to_txt)

    hook.send("**TOTAL BREAKPOINTS FOUND**: " + str(len(RSI_difference)) + "\n**File Name: **" + fileName, file=File("log.txt"))