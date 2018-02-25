import csv
from datetime import date
from os import listdir
from os.path import isfile, join
from server.process_data.bank_processor import ProcessUNFCU, ProcessBankAustria, Categories
from server.database.database_connection import run_select, run_update
from server.dto.transaction_management import update_transaction_number, get_transaction, insert_transaction

class Processor(object):

    def __init__(self, folder):
        self.entries = []
        self.folder = folder.replace('"', '').strip().rstrip()
        self.processedFiles = self.getProcessedFiles()
        self.categories = Categories()

    def process(self):
        self.processBank(self.folder + 'UNFCU', ProcessUNFCU(self.categories))
        self.processBank(self.folder + 'BankAustria', ProcessBankAustria(self.categories))
        return self.entries

    def processBank(self, folder, inputProcessor):
        fileNames = self.getAllFiles(folder)       
        for fileName in fileNames:
            if fileName not in self.processedFiles:
                self.processFile( fileName, inputProcessor)

    def getProcessedFiles(self):
        sql_comand = "select distinct fileName from ProcessedFiles where completed='True'"
        return [f['fileName'] for f in run_select(sql_comand )]

    def mark_file_as_processed(self, fileName,numEntries, status):
        fileName = fileName.replace(self.folder, '')
        print(fileName, numEntries, status)
       # sql_comand = 'insert into ProcessedFiles(fileName, processedDate, numEntries, status) values (?,?,?,?)'
       # return run_update(sql_comand, (fileName, date.today, status))

    def getAllFiles(self, folder):
        fileNames = [folder + "/" + f for f in listdir(folder) if '.csv' in f and isfile(join(folder, f))]
        return fileNames

    def processFile(self, fileName, inputProcessor):
        entries_in_file = []
        to_be_inserted = []
        all_passed = True
        print('processing ', fileName)
        with open(fileName, newline='', encoding='iso-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=inputProcessor.delimiter,  dialect='excel')
            next(reader, None)  # skip the headers
            for row in reader:
                try:
                    entry = inputProcessor.process(row)
                    if entry:
                        from_database = get_transaction(entry['Currency'], entry['Bank Name'], entry['Amount'], entry['Date_str'], entry['Description'][:30])
                        if len(from_database) == 1:
                            update_transaction_number(entry['Number'], from_database[0]['TransactionNumber'], from_database[0]['id'])
                        if len(from_database) > 1 and entry['Number'] != '...' and  entry['Number'] != None:
                            from_database = get_transaction(entry['Currency'], entry['Bank Name'], entry['Amount'], entry['Date_str'], entry['Description'][:30],entry['Number'])
                            if len(from_database) == 1:
                                update_transaction_number(entry['Number'], from_database[0]['TransactionNumber'], from_database[0]['id'])
                            if len(from_database) > 1:
                                print('found more than one', entry, row, from_database)
                        elif len(from_database) == 0:
                            insert_transaction( entry['Category'], entry['SubCategory'], entry['Type'], entry['Description'], \
                                                entry['Number'], entry['Currency'], entry['Amount'], \
                                                entry['Bank Name'], entry['Amount in EUR'] , \
                                                entry['Date_str'], entry['Date'] )
                            to_be_inserted.append(entry)
                        entries_in_file.append(entry)
                except Exception as e:
                    all_passed = False
                    print(traceback.print_exc())
                    print ('row ignored ' + str(row), entry)
        
        self.mark_file_as_processed(fileName, len(entries_in_file), all_passed==True)
        self.entries.append(entries_in_file)
        print('to be inserted', len(to_be_inserted))
      #  print(t.['Date']+ "-" t.['Amount']  for t in to_be_inserted )


                        
