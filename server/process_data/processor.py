import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join
from server.process_data.entry_management import ProcessUNFCU, ProcessBankAustria
from server.process_data.category_management import Categories
from server.db import Transaction, update_insert_transaction, update_running_balance
import traceback

class Processor(object):

    def __init__(self, folder):
        self.folder = folder.replace('"', '').strip().rstrip()
        self.categories = Categories()
        self.startDate = datetime.now()
        self.Accounts = set()

    def process(self):
        self._process_bank(self.folder + 'UNFCU', ProcessUNFCU(self.categories))
        self._process_bank(self.folder + 'BankAustria', ProcessBankAustria(self.categories))
        for a in self.Accounts:
            print('update running balance ', a)
            update_running_balance(a)

    def _update_start_date(self, date):
        if date < self.startDate:
            self.startDate = date

    def _process_bank(self, folder, inputProcessor):
        fileNames = [folder + "/" + f for f in listdir(folder) if '.csv' in f and isfile(join(folder, f))]
        for fileName in fileNames:
            self._process_file( fileName, inputProcessor)

    def _process_file(self, fileName, inputProcessor):
        all_passed = True
        entries_in_file = 0
        with open(fileName, newline='', encoding='iso-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=inputProcessor.delimiter,  dialect='excel')
            next(reader, None)  # skip the header
            for row in reader:
                try:
                    entry = inputProcessor.process(row)
                    if entry:
                        self.Accounts.add(entry['Bank Name']) #???
                        entries_in_file += 1
                        self._update_start_date(entry['Date'])
                        new_transaction_id = update_insert_transaction(transaction_id=None, description=entry['Description'], transaction_number=entry['Number'], \
                                currency=entry['Currency'], amount=entry['Amount'], amountEUR=entry['Amount in EUR'], running_balance=0, \
                                date=entry['Date'], category_id=entry['category_id'], bank_name=entry['Bank Name'], payment_date=entry['PaymentDate'])
 
                except Exception as e:
                    all_passed = False
                    print(traceback.print_exc())
                    print ('row ignored ' + str(row))
        print('processed', entries_in_file, fileName)
    
