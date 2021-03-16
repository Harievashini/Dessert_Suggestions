from flask import redirect, request, url_for, render_template
from flask.views import MethodView
#returns front page
class Index(MethodView):
    def get(self):
          return render_template('index.html')
