import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join
from server.process_data.entry_management import ProcessUNFCU, ProcessBankAustria
from server.process_data.category_management import Categories
from server.database.database_connection import run_sql
from server.dto.models import Transaction, update_insert_transaction
import traceback

class Processor(object):

    def __init__(self, folder):
        self.folder = folder.replace('"', '').strip().rstrip()
        self.categories = Categories()
        self.startDate = datetime.now()

    def update_running_balance(self):
        running_balance_perBank = {}
        transactions = Transaction.query.filter(Transaction.Date >= self.startDate).filter(Transaction.BankName != 'Budget').order_by(Transaction.Date).all()
        for t in transactions:
            t.RunningBalance = running_balance_perBank.get(t.BankName, 0) + t.Amount
            update_insert_transaction(transaction_id=t.id, running_balance=t.RunningBalance)
            running_balance_perBank[t.BankName] = t.RunningBalance

    def process(self):
        self._process_bank(self.folder + 'UNFCU', ProcessUNFCU(self.categories))
        self._process_bank(self.folder + 'BankAustria', ProcessBankAustria(self.categories))
        self.update_running_balance()

    def _update_start_date(self, date):
        if date < self.startDate:
            self.startDate = date

    def _process_bank(self, folder, inputProcessor):
        fileNames = [folder + "/" + f for f in listdir(folder) if '.csv' in f and isfile(join(folder, f))]
        for fileName in fileNames:
            if fileName not in self._get_processed_files():
                self._process_file( fileName, inputProcessor)

    def _get_processed_files(self):
        sql_comand = "select distinct fileName from ProcessedFiles where completed='True'"
        return [f['fileName'] for f in run_sql(sql_comand )]

    def _mark_file_as_processed(self, fileName,numEntries, status):
        fileName = fileName.replace(self.folder, '')
        print(fileName, numEntries, status)

    def _process_file(self, fileName, inputProcessor):
        all_passed = True
        print('processing ', fileName)
        entries_in_file = 0
        with open(fileName, newline='', encoding='iso-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=inputProcessor.delimiter,  dialect='excel')
            next(reader, None)  # skip the headers
            for row in reader:
                try:
                    entry = inputProcessor.process(row)
                    if entry:
                        entries_in_file += 1
                        from_database = Transaction.query.filter(Transaction.Currency == entry['Currency']).\
                            filter(Transaction.BankName == entry['Bank Name']).\
                            filter(Transaction.Amount == entry['Amount']).\
                            filter(Transaction.Date == entry['Date'].strftime ('%Y-%m-%d') ).\
                            filter(Transaction.Description.like("%"+entry['Description'][:30]+"%")).all()
                        if len(from_database) > 1:
                            print('found more than one', entry, row, from_database)
                        elif len(from_database) == 0:
                            self._update_start_date(entry['Date'])
                            transaction_id = update_insert_transaction(transaction_id=None, description=entry['Description'], transaction_number=entry['Number'], \
                                    currency=entry['Currency'], amount=entry['Amount'], amountEUR=entry['Amount in EUR'], running_balance=0, \
                                    date=entry['Date'], category_id=entry['category_id'], bank_name=entry['Bank Name'], payment_date=entry['PaymentDate'])
                         #   print('to insert', transaction_id, entry['category_id'], entry['Bank Name'], entry['Amount in EUR'] )

                        elif len(from_database) == 1:
                            print('already in database',entry['Date'], entry['Amount in EUR'],from_database )
                except Exception as e:
                    all_passed = False
                    print(traceback.print_exc())
                    print ('row ignored ' + str(row))
        print('processed', entries_in_file, fileName)
        self._mark_file_as_processed(fileName, entries_in_file, all_passed==True)
    
