from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import requests
import os

class Suggest(MethodView):
    def get(self):
        return render_template('suggest.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        #inserts the value of ShopName,Recommendation,Reviews into the database with kind name 'dessert'
        result=model.insert(request.form['ShopName'], request.form['Recommendation'], request.form['Reviews'])
        if result==False:
        	reply="Data is not inserted, please try again"
        	#if insertion fails it renders the same page with error message
        	return render_template('suggest.html',reply=reply)
        else:
        	return render_template('index.html')
        
        
        				
    
    	
    	
    
    	
    	
    	
    	
