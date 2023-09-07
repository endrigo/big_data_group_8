# https://medium.com/swlh/web-scraping-with-python-using-beautifulsoup-and-mongodb-6f15f6b04d68
import requests
from bs4 import BeautifulSoup
import pymongo
import urllib.parse


def scrape_registers():

    url_xml = "https://www.treasury.gov/ofac/downloads/sdn.xml"

    respuesta = requests.get(url_xml)
    contenido_xml = respuesta.text

    soup = BeautifulSoup(contenido_xml, "xml")
    sdnEntrys = soup.find_all('sdnEntry')

    registers = []

    for name in sdnEntrys:
        
        register = {}
        register['uid'] = getValue(name.uid)
        register['lastName'] = getValue(name.lastName)
        register['sdnType'] = getValue(name.sdnType)

        programList = name.find_all('programList')
        if programList is None :
            continue
        else:
            programs = []    

            for program in programList: #.stripped_strings):
                # program = getValue(program)
                # print(f'>> {program}')
                programs.append({
                    "program": getValue(program)
                    })
            
            register['programs'] = programs

        akaList = name.find_all('akaList')
        
        if akaList is None :
            continue
        else:


            akas = []

            for akaAux in akaList:
                for aka in akaAux.find_all('aka'):
                    akaUid = getValue(aka.uid)
                    akaType = getValue(aka.type)
                    akaCategory = getValue(aka.category)
                    akaLastName = getValue(aka.lastName)
                    # print(f'>>> {akaUid}')
                    # print(f'>>> {akaType}')
                    # print(f'>>> {akaCategory}')
                    # print(f'>>> {akaLastName}')

                    akas.append({
                        "uid": akaUid,
                        "type":  akaType,
                        "category": akaCategory,
                        "lastName": akaLastName
                        })

        register['akas'] = akas

        ###
        ### addressList
        ###
        addressList = name.find_all('addressList')

        # print(f':> {register["uid"]}')
        # print(f':> {addressList}')

        if addressList is None :
            continue
        else:

            addressArray = []
            # count = 0

            for addressAux in addressList:
                for address in addressAux.find_all('address'):
                    # count += 1
                    # print(f':> {count}_{address}')

                    addressUid = getValue(address.uid)
                    address1 = getValue(address.address1)
                    addressCity = getValue(address.city)
                    postalCode = getValue(address.postalCode)
                    addressCountry = getValue(address.country)
                    # # print(f'>>>> {addressUid}')
                    # # print(f'>>>> {addressCity}')
                    # # print(f'>>>> {addressCountry}')

                    addressArray.append({
                        "uid": addressUid,
                        "address1": address1,
                        "city":  addressCity,
                        "postalCode":  postalCode,
                        "country": addressCountry
                        })

        register['address'] = addressArray


        idsList = name.find_all('idList')
        if idsList is None :
            continue
        else:
            idsArray = []

            for idsAux in idsList:
                for ids in idsAux.find_all('id'):
                    idListUid = getValue(ids.uid)
                    idListType = getValue(ids.idType)
                    idListNumber = getValue(ids.idNumber)
                    idListCountry = getValue(ids.idCountry)
                    # print(f'>>>>> {idListUid}')
                    # print(f'>>>>> {idListType}')
                    # print(f'>>>>> {idListNumber}')
                    # print(f'>>>>> {idListCountry}')

                    idsArray.append({
                        "uid": idListUid,
                        "idType":  idListType,
                        "idNumber": idListNumber,
                        "idCountry": idListCountry
                        })

        register['ids'] = idsArray


        nationalityList = name.find_all('nationalityList')
        if nationalityList is None :
            continue
        else:
            nationalities = []

            for nationalityAux in nationalityList:
                for nationality in nationalityAux.find_all('nationality'):
                    nationalityUid = getValue(nationality.uid)
                    nationalityCountry = getValue(nationality.country)
                    nationalityMainEntry = getValue(nationality.mainEntry)
                    # print(f'>>>>>> {nationalityUid}')
                    # print(f'>>>>>> {nationalityCountry}')
                    # print(f'>>>>>> {nationalityMainEntry}')
    
                    nationalities.append({
                        "uid": nationalityUid,
                        "country":  nationalityCountry,
                        "mainEntry": nationalityMainEntry
                        })

        register['nationalities'] = nationalities


        dateOfBirthList = name.find_all('dateOfBirthList')
        if dateOfBirthList is None :
            continue
        else:
            datesOfBirth = []

            for dateOfBirthAux in dateOfBirthList:
                for dateOfBirth in dateOfBirthAux.find_all('dateOfBirthItem'):
                    dateOfBirthUid = getValue(dateOfBirth.uid)
                    dateOfBirthDate = getValue(dateOfBirth.dateOfBirth)
                    dateOfBirthMainEntry = getValue(dateOfBirth.mainEntry)
                    # print(f'>>>>>>> {dateOfBirthUid}')
                    # print(f'>>>>>>> {dateOfBirthDate}')
                    # print(f'>>>>>>> {dateOfBirthMainEntry}')

                    datesOfBirth.append({
                        "uid": dateOfBirthUid,
                        "dateOfBirth":  dateOfBirthDate,
                        "mainEntry": dateOfBirthMainEntry
                        })

        register['datesOfBirth'] = datesOfBirth


        placeOfBirthList = name.find_all('placeOfBirthList')
        if placeOfBirthList is None :
            continue
        else:

            placesOfBirth = []

            for placeOfBirthAux in placeOfBirthList:
                for placeOfBirth in placeOfBirthAux.find_all('placeOfBirthItem'):
                    placeOfBirthUid = getValue(placeOfBirth.uid)
                    placeOfBirthPlace = getValue(placeOfBirth.placeOfBirth)
                    placeOfBirthMainEntry = getValue(placeOfBirth.mainEntry)
                    # print(f'>>>>>>>> {placeOfBirthUid}')
                    # print(f'>>>>>>>> {placeOfBirthPlace}')
                    # print(f'>>>>>>>> {placeOfBirthMainEntry}')

                    placesOfBirth.append({
                        "uid": placeOfBirthUid,
                        "placeOfBirth":  placeOfBirthPlace,
                        "mainEntry": placeOfBirthMainEntry
                        })

        register['placesOfBirth'] = placesOfBirth

        #Save all into main Array
        registers.append(register)

    return registers


def getValue(val):
    
    if val is None:
        return ''
    
    return val.text.strip()

quotes = scrape_registers()

#print(f'> {quotes}')

username = urllib.parse.quote_plus('mongoadmin')
password = urllib.parse.quote_plus('bdung')

client = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
db = client.db.ofac
try:
    db.insert_many(quotes)
    print(f'inserted {len(quotes)} registers')
# except:
    # print('an error occurred quotes were not stored to db')
except Exception as error:
  print("an error occurred registers were not stored to db:", error)