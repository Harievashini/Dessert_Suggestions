"""
A simple Desserts flask app.
"""
import flask
import os
from flask.views import MethodView
from index import Index
from suggest import Suggest
from view import View
from recipe import Recipe
app = flask.Flask(__name__)       # our Flask app

#index uses GET method
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET'])
#sign uses GET and POST methods
app.add_url_rule('/suggest/',
                 view_func=Suggest.as_view('suggest'),
                 methods=['GET', 'POST'])
#view file uses GET method to fetch and display the list
app.add_url_rule('/view/',
                 view_func=View.as_view('view'),
                 methods=['GET'])
#recipe uses both get and post
app.add_url_rule('/recipe/',
                 view_func=Recipe.as_view('recipe'),
                 methods=['GET', 'POST'])
#Deployed at port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
