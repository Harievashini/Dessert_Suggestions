from .model_datastore import model

appmodel = model()
#To get the backend database
def get_model():
    return appmodel
