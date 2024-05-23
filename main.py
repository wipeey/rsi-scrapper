import os
from time import sleep
from rsi import *

#Find the CSV file in current directory
def find_csv():
    csv_file = ""

    for file in os.listdir():
        if file.endswith('.csv'):
            csv_file = file

    return csv_file

def main():
    print('Welcome!') ; sleep (1)

    if(not find_csv()):
        print("Error: No CSV found!")
        pass
    else:
        print('Analying file ' + find_csv() + '...') ; sleep(0.5)

        webhook = input("Enter webhook URL (leave blank to pass): ")

        extract_CSV(find_csv())
        extract_RSI_over()
        extract_difference()

        if(not not webhook):
            send_webhook(webhook, find_csv())
            print('Created file log.txt!')
            print('Webhook sent!') ; sleep(0.3)

        print('\n==> Average difference between RSI on breakpoint and 6 hours later:\n')
        compare_RSI()
          
if __name__ == '__main__':
    main()

input('\nPress enter to exit: ')