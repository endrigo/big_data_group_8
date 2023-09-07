import psycopg2
from pymongo import MongoClient
import pymongo
import urllib.parse
import json

# Configuración de la conexión a MongoDB
username = urllib.parse.quote_plus('mongoadmin')
password = urllib.parse.quote_plus('bdung')

mongo_client = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
mongo_db=mongo_client.db #database name
mongo_collection = mongo_db.ofac #collection

# Configuración de la conexión a PostgreSQL
pg_connection_params = {
    'dbname': 'conta',
    'user': 'postgres',
    'password': '321',
    'host': 'localhost',
    'port':'5435'
}

# Conexión a PostgreSQL
pg_connection = psycopg2.connect(**pg_connection_params)
pg_cursor = pg_connection.cursor()

# Recuperar datos de MongoDB
mongo_data = mongo_collection.find()

print("Total a imprimir:")
print(mongo_collection.count_documents({}))
count = 0

# # Iterar a través de los datos y guardar en PostgreSQL
for document in mongo_data:

    # print(f'> {document}\n')

# {'_id': ObjectId('64f9f72cbac715496c2d467b'), 
#  'uid': '44910', 
#  'lastName': 'CHERNOV', 
#  'sdnType': 'Individual', 
#  'programs': [{'program': 'CYBER2'}], 
#  'akas': [{'uid': '69452', 'type': 'a.k.a.', 'category': 'weak', 'lastName': 'BULLET'}], 
#  'address': [{'uid': '66831', 'address1': '', 'city': '', 'postalCode': '', 'country': 'Russia'}],
#  'ids': [{'uid': '165190', 'idType': 'Gender', 'idNumber': 'Male', 'idCountry': ''}, {'uid': '165273', 'idType': 'Secondary sanctions risk:', 'idNumber': 'Ukraine-/Russia-Related Sanctions Regulations, 31 CFR 589.201', 'idCountry': ''}], 
#  'nationalities': [{'uid': '65191', 'country': 'Russia', 'mainEntry': 'true'}], 
#  'datesOfBirth': [{'uid': '65189', 'dateOfBirth': '26 Jan 1986', 'mainEntry': 'true'}], 'placesOfBirth': []
#  }

    count += 1
    print(f'> {count}')

    uid = document.get('uid')
    lastName = document.get('lastName')
    sdnType = document.get('sdnType')
    programs = json.dumps(document.get('programs'))
    akas = json.dumps(document.get('akas'))
    address = json.dumps(document.get('address'))
    ids = json.dumps(document.get('ids'))
    nationalities = json.dumps(document.get('nationalities'))
    datesOfBirth = json.dumps(document.get('datesOfBirth'))
    placesOfBirth = json.dumps(document.get('placesOfBirth'))

    #Insertar en PostgreSQL
    insert_query = "INSERT INTO mongo_db (uid,lastName,sdnType,programs,akas,address,ids,nationalities,datesOfBirth,placesOfBirth) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    pg_cursor.execute(insert_query, (uid,lastName,sdnType,programs,akas,address,ids,nationalities,datesOfBirth,placesOfBirth))
    pg_connection.commit()

# Cerrar las conexiones
pg_cursor.close()
pg_connection.close()
mongo_client.close()
