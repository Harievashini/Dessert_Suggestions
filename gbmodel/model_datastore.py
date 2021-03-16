# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Model import Model
from google.cloud import datastore
from datetime import datetime

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ ShopName, Recommendation, Reviews, Date]
    where ShopName, Recommendation, Reviews are Python strings
    and where date is a Python datetime
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['ShopName'],entity['Recommendation'],entity['Reviews'],entity['Date']]

class model(Model):
    def __init__(self):
    	#Project id
        self.client = datastore.Client('cloud-f20-hvashini-dk-hariev2')
    #entity creation and selection
    def select(self):
        query = self.client.query(kind = 'dessert')
        entities = list(map(from_datastore,query.fetch()))
        return entities
    #inserting the input values into the datastore table entities
    def insert(self, ShopName, Recommendation, Reviews):
        key = self.client.key('dessert')
        rev = datastore.Entity(key)
        rev.update( {
            'ShopName':ShopName, 
            'Recommendation':Recommendation,
            'Reviews':Reviews,
            'Date' : datetime.today()
            })
        self.client.put(rev)
        return True
