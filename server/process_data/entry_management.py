from datetime import datetime
import re
import ssl

class GenericProcessor(object):
     
    def __init__(self, categories):
        self.categories = categories
        self.from_usd_to_euro = 1
    
    def convert_to_number(self, number_in_string):
        return float(str(number_in_string).strip())
    
    def get_amount(self, row):
        value = self.convert_to_number(row[self.amount_pos])
        if ((self.account_name_pos is not None and ('Visa Elite' in row[self.account_name_pos] or 'Credit Card'in row[self.account_name_pos] ))):
            return -value
        return value
        
    def process(self, row):
        if self.get_amount(row) != 0:
            entry = {}
            entry['Description'] = self.get_description(row).strip()
            entry['category_id'] = self.categories.get_category(entry['Description'])
            entry['Number'] = self.get_number(row)
            entry['Date'] = datetime.strptime ( row[self.date_pos].strip(), self.date_format)
            entry['PaymentDate'] = entry['Date']
            entry['Amount'] = self.get_amount(row)
            entry['Currency'] = self.currency
            account_name = ' - ' + row[self.account_name_pos] if self.account_name_pos is not None else " - Checking Account"
            account_number = row[self.account_number_pos] if self.account_number_pos is not None else ""
            entry['Bank Name'] = self.bank_name + account_name + account_number
            entry['Amount in EUR' ] = self.from_usd_to_euro * entry['Amount']
            return entry
        else:
            try:
                description = self.get_description(row).split(' ')
                if description[3] == '978':
                    self.from_usd_to_euro = self.convert_to_number(description[4])
            finally:
                return
        
class ProcessBankAustria(GenericProcessor):
    # Booking date    Value date    Booking Text    Internal Note    Currency    Amount    Record data    Record Number    Originator name    Originator Account    Originator's Bank Code    Payee Name    Payee Account    Payee Bank Code    Purpose Text
    def __init__(self, categories):
        self.delimiter = ';'
        self.account_name_pos = None
        self.account_number_pos = None
        self.number_pos=7
        self.record_data_pos=6
        self.date_pos=1
        self.date_format='%d.%m.%Y'
        self.amount_pos=5
        self.currency='EUR'
        self.bank_name='BankAustria'
        GenericProcessor.__init__(self, categories)
    
    def convert_to_number(self, number_in_string):
        return float(str(number_in_string).replace('.', '').replace(',', '.'))
    
    def get_description(self, row):
        return str(row[2]) + str(row[11])

    def get_number(self, row):
        if row[self.number_pos] is not None and str(row[self.number_pos]).strip() != "":
            return str(row[self.number_pos]).replace('\n', '')
        elif row[self.record_data_pos] is not None and str(row[self.record_data_pos]).strip() != "":
            return str(row[self.record_data_pos]).replace('\n', '')
        else:
            return "..."


class ProcessUNFCU(GenericProcessor):
    ['UNFCU Visa Elite ', ' 4024830900084389', ' 11/22/2017', ' 49.99', ' ', ' 2479262A62E0463Z6 SLING.COM 888-393-6312 CO', ' SLING.COM 888-393-6312 CO']
   # AccountName,  AccountNumber, TransactioDate, TransactionAmount, TransactionCheckNumber, TransactionDesc, TransactionMemo
    def __init__(self, categories):
        self.delimiter = ','
        self.account_name_pos = 0
        self.account_number_pos = 1
        self.number_pos=4
        self.date_pos=2
        self.date_format='%m/%d/%Y'
        self.amount_pos=3
        self.currency='USD'
        self.bank_name='UNFCU'
        GenericProcessor.__init__(self, categories)
    
    def get_description(self, row):
        return str(row[5]) + str(row[6])

    def get_number(self, row):
         str(row[self.number_pos]).replace('\n', '') if row[self.number_pos] is not None and str(row[self.number_pos]).strip() != "" else "..."
    
