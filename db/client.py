from pymongo import MongoClient

# se conecta a localhost de froma automatica sino hay que escribir dnde esta en remoto
db_client = MongoClient()
#se conecta y se cconecta a la coleccion de FitLife
db = db_client.FitLife
