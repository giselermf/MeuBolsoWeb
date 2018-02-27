from server.dto.category_management import get_all_categories
from server.dto.transaction_management import get_all_transactions, update_transaction
import re

class Categories(object): 
    def __init__(self):
        categories = {}
        try: 
            all_categories = get_all_categories()
            for e in all_categories:
                category = " ".join(str(e['category'] + "#" + e['subcategory'] + "#" + e['type'] ).split())  # remove extra spaces between words
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
    
    def get_category(self, description, category=None):
        key = category if category != "" and category != "Other" and category is not None else description
        key = " ".join(key.split()).lower() # remove extra spaces between words
        value = [self.categories_regex[k] for k in self.categories_regex if re.search(" ".join(k.split()).lower(), key.lower())]
        category_and_subcategory_and_type = value[0] if len(value) > 0 and str(value[0]) != 'nan' else "Others#Others#Others"
        return category_and_subcategory_and_type.split("#")

class Categorization(object):

    def __init__(self):
        self.categories = Categories()
    
    def run(self):
        for t in get_all_transactions():
            t['Category'], t['SubCategory'], t['Type'] = self.categories.get_category(t['Description'] )
            update_transaction(id=t['id'], category=t['Category'], sub_category=t['SubCategory'], type=t['Type'])

