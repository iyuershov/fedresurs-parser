import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_entity_list(organization):
    response = requests.post('https://fedresurs.ru/backend/companies/search', json={
        "entitySearchFilter": {
            "regionNumber": None,
            "onlyActive": False,
            "startRowIndex": 0,
            "pageSize": 2,
            "code": organization['code'],
            "name": organization['name'],
            "legalCase": None
        }
    })
    return response.json()


def get_messages_info(guid):
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


def build_options():
    options = Options()
    options.headless = True
    return options


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
        driver = webdriver.Firefox(options=build_options(), executable_path="driver/geckodriver")
        result = []
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
                result.append({entity['guid']: message_list})
            else:
                result.append({entity['guid']: "No bankrupt-themed messages."})

        print(result)

    else:
        print("No such organizations")
        exit(1)


if __name__ == '__main__':
    main()
