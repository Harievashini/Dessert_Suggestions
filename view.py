from flask import render_template
from flask.views import MethodView
import gbmodel
import requests
import os

class View(MethodView):
    def get(self):
        #Retrieve the backend database
        model = gbmodel.get_model()
        entries=[]
        #To retrieve all the values from the database 
        for row in model.select():
            #To get the nutrition content of the recommended food
            nutrition=self.getnutrition(row[1])
            #To get the place details
            details = self.findstore(row[0]) 
            if details !=[]:
                for i in details:
                    #To obtain the address information
                    if 'vicinity' in i.keys():
                        address=i['vicinity']
                    else:
                        address='unknown'
                    #To obtain the rating information
                    if 'rating' in i.keys():
                        rating=i['rating']
                    else:
                        rating='unknown'
                    #To obtain the place id
                    if 'place_id' in i.keys():
                        placeid=i['place_id']
                    else:
                        place_id='unknown'
                    #Using the placeid get further details on the given food shop
                    details1=self.getdetails(placeid)
                    if details1 !=[]:
                        #To obtain the website information
                        if 'website' in details1.keys():
                            website=details1['website']
                        else:
                            website='unknown'
                        #To obtain the phonenumber information
                        if 'international_phone_number' in details1.keys():
                            phonenumber=details1['international_phone_number']
                        else:
                            phonenumber='unknown'
                        #Display all the details on view.html
                        entries.append(dict(ShopName=row[0], Address=address, Recommendation=row[1], Nutrition=nutrition, Reviews=row[2], Rating=rating, Website=website, Phonenumber=phonenumber))
                    #Displaying only one address of the shop
                    break
        return render_template('view.html',entries=entries)
    #Uses nutritionix api to get information on the recommended food
    def getnutrition(self,food):
        #API ID
        api_id = os.environ.get('NUTRITIONIX_API_ID')
        #API KEY
        api_key = os.environ.get('NUTRITIONIX_API_KEY')
        #Response from the API in json format
        response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', headers = {"Content-Type":"application/json","x-app-id":api_id,"x-app-key":api_key}, json = {"query":food,"timezone":"US/Western"})
        res=response.json()
        #Getting calories, fats, carbohydrates, protein information from API and appending it inside nutrition dictionary
        if "foods" in res.keys():
            if "nf_calories" in res["foods"][0].keys():
                calories=res["foods"][0]["nf_calories"]
            else:
                calories=None
            if "nf_total_fat" in res["foods"][0].keys():
                fats=res["foods"][0]["nf_total_fat"]
            else:
                fats=None
            if "nf_total_carbohydrate" in res["foods"][0].keys():
                carbohydrates=res["foods"][0]["nf_total_carbohydrate"]
            else:
                carbohydrates=None
            if "nf_protein" in res["foods"][0].keys():
                proteins=res["foods"][0]["nf_protein"]
            else:
                proteins=None
            nutrition=dict(Calories=calories, Fats=fats, Carbohydrates=carbohydrates, Proteins=proteins)
        #If no details present it unknown
        else:
            nutrition={"unknown"}
        return nutrition
    #Uses places api to get information on the given shop
    def findstore(self,shop):
        #API KEY
        api_key = os.environ.get('PLACES_API_KEY')
        #Response from the API in json format
        response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=45.523064,-122.676483&radius=30000&type=restaurant&keyword='+shop+'&key='+api_key)
        res=response.json()
        #Returning the details dict
        details = res['results']
        return details 
    #Using the other places api and shop's placeid obtain further details	
    def getdetails(self,placeid):
        #API KEY
        api_key = os.environ.get('PLACES_API_KEY')
        #Response from the API in json format
        response = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id='+placeid+'&key='+api_key)
        res=response.json()
        #Returning the detail dict
        details=res['result']
        return details
    	
