import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join
from server.process_data.entry_management import ProcessUNFCU, ProcessBankAustria
from server.process_data.category_management import Categories
from server.app.models import Transaction
import traceback
from server.app import db

class Processor(object):

    def __init__(self, folder):
        self.folder = folder.replace('"', '').strip().rstrip()
        self.categories = Categories()
        self.startDate = datetime.now()
        self.Accounts = set()


    def process(self):
        self._process_bank(self.folder + 'UNFCU', ProcessUNFCU(self.categories))
        self._process_bank(self.folder + 'BankAustria', ProcessBankAustria(self.categories))

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
                        self._process_entry(fileName, entry)
                        entries_in_file += 1
                except Exception as e:
                    all_passed = False
                    print(traceback.print_exc())
                    print ('row ignored ' + str(row))
        print('processed', entries_in_file, fileName)

    def _process_entry(self, fileName, entry):
        self.Accounts.add(entry['Bank Name'])
        self._update_start_date(entry['Date'])
        query= Transaction.query.\
            filter(Transaction.Date == entry['Date'].strftime ('%Y-%m-%d')).\
            filter(Transaction.BankName == entry['Bank Name']).\
            filter(Transaction.Amount == entry['Amount'])
        if entry['Number'] is not None:
            query = query.filter(Transaction.TransactionNumber == entry['Number'])
        from_db = query.all()
        if len(from_db) == 0:
            new_transaction = Transaction(Description=entry['Description'], TransactionNumber=entry['Number'], \
                Currency=entry['Currency'], Amount=entry['Amount'], RunningBalance=0, \
                Date=entry['Date'], category_id=entry['category_id'], BankName=entry['Bank Name'], PaymentDate=entry['PaymentDate'], \
                Filename= fileName)
            db.session.add(new_transaction)
            db.session.commit()
            return new_transaction.id
        else:
            return from_db[0].id
        return 1
    
