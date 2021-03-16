from flask import redirect, request, url_for, render_template,flash
from flask.views import MethodView
import gbmodel
import requests
import os
import json

class Recipe(MethodView):
    def get(self):
        return render_template('recipe.html')
        
    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        #Obtain the dessert name from recipe.html
        food=request.form['Dessert']
        #To grab the recipe details of the given dessert
        foodname = self.findrecipe(food)
        #render recipe details in recipe.html
        return render_template('recipe.html',foodname=foodname)
        
    #Uses spoonacular's recipe api to list the recipe details of the requested dessert.  
    def findrecipe(self,food):
    	#API KEY
        api_key = os.environ.get('RECIPE_API_KEY')
        #List to hold all recipe details
        foodname=[]
	#Response is returned in text format 
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
        querystring = {"query":food}
        headers = {'x-rapidapi-key': api_key,'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"}

        response = requests.request("GET", url, headers=headers, params=querystring)
        r=response.text
        #Converting the text format to json format
        d = json.loads(r)
        food_ids=[] #To store recipe id
	#Obtaining the ids of all the recipes
        for i in d['results']:
            food_ids.append(i['id'])
	#Using the ids, each recipe details are retrieved
        for i in food_ids:
            url1 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+str(i)+"/information"
            headers1 ={'x-rapidapi-key': api_key,'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"}
	    #Response in text format
            response1 = requests.request("GET", url1, headers=headers1)
            r1=response1.text
            #Converting the text format to json format
            d1 = json.loads(r1)
	    # To merge title,ingredients,method of all the recipes for a given dessert
            foodname.append(d1['title'])
            ingre=""
            for i in d1['extendedIngredients']:
                ingre+=i['originalString']
                ingre+=','
            foodname.append(ingre[:-1])
            foodname.append(d1['instructions'])
        return(foodname)
