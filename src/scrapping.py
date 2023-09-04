# https://medium.com/swlh/web-scraping-with-python-using-beautifulsoup-and-mongodb-6f15f6b04d68
import requests
from bs4 import BeautifulSoup
import pymongo
import urllib.parse


def scrape_quotes():
    quotes = []

    url_xml = "https://www.treasury.gov/ofac/downloads/sdn.xml"

    respuesta = requests.get(url_xml)
    contenido_xml = respuesta.text

    soup = BeautifulSoup(contenido_xml, "xml")
    sdnEntrys = soup.find_all('sdnEntry')

    for name in sdnEntrys:
        
        quote = {}
        quote['uid'] = getValue(name.uid)
        quote['lastName'] = getValue(name.lastName)
        quote['sdnType'] = getValue(name.sdnType)

        quotes.append(quote)
        continue

        programList = name.find_all('programList')
        if programList is None :
            continue
        else:
            for program in programList: #.stripped_strings):
                program = getValue(program)
                print(f'>> {program}')

        akaList = name.find_all('akaList')
        if akaList is None :
            continue
        else:
            for aka in akaList:

                akaUid = getValue(aka.uid)
                akaType = getValue(aka.type)
                akaCategory = getValue(aka.category)
                akaLastName = getValue(aka.lastName)
                print(f'>>> {akaUid}')
                print(f'>>> {akaType}')
                print(f'>>> {akaCategory}')
                print(f'>>> {akaLastName}')

        addressList = name.find_all('addressList')
        if addressList is None :
            continue
        else:
            for address in addressList:
                addressUid = getValue(address.uid)
                addressCity = getValue(address.city)
                addressCountry = getValue(address.country)
                print(f'>>>> {addressUid}')
                print(f'>>>> {addressCity}')
                print(f'>>>> {addressCountry}')

        idsList = name.find_all('idList')
        if idsList is None :
            continue
        else:
            for ids in idsList:
                idListUid = getValue(ids.uid)
                idListType = getValue(ids.idType)
                idListNumber = getValue(ids.idNumber)
                idListCountry = getValue(ids.idCountry)
                print(f'>>>>> {idListUid}')
                print(f'>>>>> {idListType}')
                print(f'>>>>> {idListNumber}')
                print(f'>>>>> {idListCountry}')

        nationalityList = name.find_all('nationalityList')
        if nationalityList is None :
            continue
        else:
            for nationality in nationalityList:
                nationalityUid = getValue(nationality.uid)
                nationalityCountry = getValue(nationality.country)
                nationalityMainEntry = getValue(nationality.mainEntry)
                print(f'>>>>>> {nationalityUid}')
                print(f'>>>>>> {nationalityCountry}')
                print(f'>>>>>> {nationalityMainEntry}')
  
        dateOfBirthList = name.find_all('dateOfBirthList')
        if dateOfBirthList is None :
            continue
        else:
            for dateOfBirth in dateOfBirthList:
                dateOfBirthUid = getValue(dateOfBirth.uid)
                dateOfBirthDate = getValue(dateOfBirth.country)
                dateOfBirthMainEntry = getValue(dateOfBirth.mainEntry)
                print(f'>>>>>>> {dateOfBirthUid}')
                print(f'>>>>>>> {dateOfBirthDate}')
                print(f'>>>>>>> {dateOfBirthMainEntry}')

        placeOfBirthList = name.find_all('dateOfBirthList')
        if placeOfBirthList is None :
            continue
        else:
            for placeOfBirth in placeOfBirthList:
                placeOfBirthUid = getValue(placeOfBirth.uid)
                placeOfBirthPlace = getValue(placeOfBirth.country)
                placeOfBirthMainEntry = getValue(placeOfBirth.mainEntry)
                print(f'>>>>>>>> {placeOfBirthUid}')
                print(f'>>>>>>>> {placeOfBirthPlace}')
                print(f'>>>>>>>> {placeOfBirthMainEntry}')


        print("-----------")

    return quotes


def getValue(val):

    # print(f'VAL {val}')

    # if val == "-1":
    #     return ''
    
    # if val == '':
    #     return ''
    
    if val is None:
        return ''
    
    return val.text.strip()

quotes = scrape_quotes()

#print(f'> {quotes}')

username = urllib.parse.quote_plus('mongoadmin')
password = urllib.parse.quote_plus('bdung')

client = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
db = client.db.debts
try:
    db.insert_many(quotes)
    print(f'inserted {len(quotes)} articles')
except:
    print('an error occurred quotes were not stored to db')