import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from flask import Flask, request, jsonify

app = Flask(__name__)

#Получение списка организаций по ключевой фразе (название, инн или огрн)
def get_entity_list(organization):
    response = requests.post('https://fedresurs.ru/backend/companies/search', json={
        "entitySearchFilter": {
            "regionNumber": None,
            "onlyActive": False,
            "startRowIndex": 0,
            "pageSize": 10000000,
            "code": organization['code'],
            "name": organization['name'],
            "legalCase": None
        }
    })
    return response.json()


#Получение списка сообщений о банкротстве ("searchFirmBankruptMessage": True), относящихся к организации
def get_messages_info(entity_guid):
    response = requests.post("https://fedresurs.ru/backend/companies/publications", json={
        "guid": entity_guid,
        "pageSize": 10000000,
        "startRowIndex": 0,
        "startDate": None,
        "endDate": None,
        "messageNumber": None,
        "bankruptMessageType": None,
        "bankruptMessageTypeGroupId": None,
        "legalCaseId": None,
        "searchAmReport": False,
        "searchFirmBankruptMessage": True,
        "searchFirmBankruptMessageWithoutLegalCase": False,
        "searchSfactsMessage": False,
        "searchSroAmMessage": False,
        "searchTradeOrgMessage": False,
        "sfactMessageType": None,
        "sfactsMessageTypeGroupId": None
    })
    return response.json()['pageData']


#Создание конфига для работы headless-firefox
def build_options():
    options = Options()
    options.headless = True
    return options

@app.route('/create_task', methods=['GET'])
def main():

    #Параметры задаются в адресной строке
    code = request.args.get('code')
    name = request.args.get('name')

    organization = dict(code=code,name=name)

    entity_list = get_entity_list(organization)
    if len(entity_list['pageData']) > 0:
        driver = webdriver.Firefox(options=build_options(), executable_path="driver/geckodriver")
        result = dict()
        for entity in entity_list['pageData']:
            messages = get_messages_info(entity['guid'])
            message_list = []
            for message in messages:
                url = "https://bankrot.fedresurs.ru/MessageWindow.aspx?ID=" + message['guid']
                driver.get(url)
                data = {
                    "guid": message['guid'],
                    "text": driver.find_element_by_class_name("msg").text[7:],
                    "date": message['datePublish'],
                    "url": url
                }
                message_list.append(data)

            if len(message_list) > 0:
                result[entity['guid']] = message_list

        return jsonify(result)

    else:
        return "No such organizations"


if __name__ == '__main__':
    app.run()
