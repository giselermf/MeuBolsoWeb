from flask import Flask
from flask_cors import CORS
from server.dto.data_server import get_categories, save_category, delete_category
from flask import request

app = Flask(__name__)
CORS(app)

@app.route('/categories/', methods=['POST'])
def categories():
    if request.method == 'POST':
        return app.make_response(
            save_category(request.form['id'], request.form['category'], request.form['description']))
  #  elif request.method == 'GET':
  #      return app.make_response((get_categories(None), 200))

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
    return app.make_response(delete_category(id))

@app.route('/categories/', methods=['GET'])
def categories_with_filter():
    print('categories_with_filter')
    sort_params = request.args.get('sort').split('|')
    sort = sort_params[0]
    sort_order = sort_params[1]
    filter = request.args.get('filter')
    return app.make_response((get_categories(sort, sort_order, filter), 200))