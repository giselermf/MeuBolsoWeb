import csv
from datetime import date
from os import listdir
from os.path import isfile, join
from server.process_data.entry_management import ProcessUNFCU, ProcessBankAustria
from server.process_data.category_management import Categories
from server.database.database_connection import run_select, run_update
from server.dto.transaction_management import get_transaction, insert_transaction, get_all_transactions, update_transaction
import traceback

class Processor(object):

    def __init__(self, folder):
        self.folder = folder.replace('"', '').strip().rstrip()
        self.categories = Categories()
        self.running_balance_perBank = {}

    def process(self):
        self._process_bank(self.folder + 'UNFCU', ProcessUNFCU(self.categories))
        self._process_bank(self.folder + 'BankAustria', ProcessBankAustria(self.categories))
        self._update_running_balance()

    def _process_bank(self, folder, inputProcessor):
        fileNames = [folder + "/" + f for f in listdir(folder) if '.csv' in f and isfile(join(folder, f))]
        for fileName in fileNames:
            if fileName not in self._get_processed_files():
                self._process_file( fileName, inputProcessor)

    def _get_processed_files(self):
        sql_comand = "select distinct fileName from ProcessedFiles where completed='True'"
        return [f['fileName'] for f in run_select(sql_comand )]

    def _mark_file_as_processed(self, fileName,numEntries, status):
        fileName = fileName.replace(self.folder, '')
        print(fileName, numEntries, status)
       # sql_comand = 'insert into ProcessedFiles(fileName, processedDate, numEntries, status) values (?,?,?,?)'
       # return run_update(sql_comand, (fileName, date.today, status))

    def _update_transaction_number(self, new_transaction_number, current_transaction_number, id):
        if new_transaction_number != '...' and new_transaction_number != None and new_transaction_number != current_transaction_number and len(new_transaction_number) < 16:
            update_transaction(id=id, transaction_number=new_transaction_number)

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
                        from_database = get_transaction(entry['Currency'], entry['Bank Name'], entry['Amount'], entry['Date_str'], entry['Description'][:30])
                        if len(from_database) == 1:
                            self._update_transaction_number(entry['Number'], from_database[0]['TransactionNumber'], from_database[0]['id'])
                        if len(from_database) > 1 and entry['Number'] != '...' and  entry['Number'] != None:
                            from_database = get_transaction(entry['Currency'], entry['Bank Name'], entry['Amount'], entry['Date_str'], entry['Description'][:30],entry['Number'])
                            if len(from_database) == 1:
                                self._update_transaction_number(entry['Number'], from_database[0]['TransactionNumber'], from_database[0]['id'])
                            if len(from_database) > 1:
                                print('found more than one', entry, row, from_database)
                        elif len(from_database) == 0:
                            insert_transaction( entry['Category'], entry['SubCategory'], entry['Type'], entry['Description'], \
                                                entry['Number'], entry['Currency'], entry['Amount'], \
                                                entry['Bank Name'], entry['Amount in EUR'] , \
                                                entry['Date_str'], entry['Date'] )
                except Exception as e:
                    all_passed = False
                    print(traceback.print_exc())
                    print ('row ignored ' + str(row), entry)
        
        self._mark_file_as_processed(fileName, entries_in_file, all_passed==True)

    def _update_bank_balance(self, bankName, balance):
        self.running_balance_perBank[bankName] = balance

    def _update_running_balance(self):
        transactions = get_all_transactions(oder_by = "BankName,Date,Id")
        for t in transactions:
            t['RunningBalance'] = self.running_balance_perBank.get(t['BankName'], 0) + t['Amount']
            update_transaction(id=t['id'], RunningBalance =  t['RunningBalance'] )
            self._update_bank_balance(t['BankName'], t['RunningBalance'])
    
