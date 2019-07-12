import requests
from selenium import webdriver


def get_entity_list(organization):
    response = requests.post('https://fedresurs.ru/backend/companies/search', json={
        "entitySearchFilter": {
            "regionNumber": None,
            "onlyActive": False,
            "startRowIndex": 0,
            "pageSize": 1000000,
            "code": organization['code'],
            "name": organization['name'],
            "legalCase": None
        }
    })
    return response.json()


def get_messages_id(guid):
    response = requests.post("https://fedresurs.ru/backend/companies/publications", json={
        "guid": guid,
        "pageSize": 1000000,
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


def main():
    print("Введите название или идентификатор организации организации:")
    organization = dict.fromkeys(['code', 'name'])
    entered = input()
    if entered.replace(' ', '').isdigit():
        organization.update({'code': entered.replace(' ', '')})
    else:
        organization.update({'name': entered})

    entity_list = get_entity_list(organization)
    if len(entity_list['pageData']) > 0:
        driver = webdriver.Chrome('driver/chromedriver')
        for entity in entity_list['pageData']:
            messages = get_messages_id(entity['guid'])
            for message in messages:
                url = "https://bankrot.fedresurs.ru/MessageWindow.aspx?ID=" + message['guid']
                print(message['guid'])
                print(driver.get(url))

    else:
        print("No such organizations")
        exit(1)


if __name__ == '__main__':
    main()
