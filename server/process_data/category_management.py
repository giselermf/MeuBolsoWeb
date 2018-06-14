from server.dto.category_management import get_all_categories
from server.dto.transaction_management import get_all_transactions, update_transaction
import re

class Categories(object): 
    def __init__(self):
        categories = {}
        try: 
            all_categories = get_all_categories()
            for e in all_categories:
                category =  e['id']
                value = e['description']
                if category in categories:
                    categories[category].append(value)
                else:
                    categories[category] = [value,]
        except Exception as e:
            print('categories not found', e)
        finally:
            self.generate_regex(categories)
        
    def generate_regex(self, categories):
        self.categories_regex = {}
        for key, value in categories.items():
            regex = ''
            for v in value:
                regex += v + "|"
            regex = regex[:-1]
            self.categories_regex[regex] = key
    
    def get_category(self, description):
        description = " ".join(description.split()).lower() # remove extra spaces between words
        category_id = [self.categories_regex[k] for k in self.categories_regex if re.search(" ".join(k.split()).lower(), description)]
        if len(category_id) == 0:
            category_id = [self.categories_regex[k] for k in self.categories_regex if re.search(" ".join(k.split()).lower(), 'others')]
        return category_id[0] 

class Categorization(object):

    def __init__(self):
        self.categories = Categories()
    
    def run(self):
        all_transactions = get_all_transactions(MinDate = '1900-01-01')

        for t in all_transactions:
            update_transaction(transaction_id=t['id'], category_id=self.categories.get_category(t['Description']))
