import requests

def get_entity_list(organization):
    response = requests.post('https://fedresurs.ru/backend/companies/search', json={
	"entitySearchFilter": {
		"regionNumber": None,
		"onlyActive": False,
		"startRowIndex": 0,
		"pageSize": 10000,
		"code":organization['code'],
		"name": organization['name'],
		"legalCase": None
	}
})
    return response.json()

def main():
    print("Введите название или идентификатор организации организации:")
    organization = dict.fromkeys(['code','name'])
    entered = input()
    if entered.isdigit():
        organization.update({'code' : entered})
    else:
        organization.update({'name' : entered})
    print(organization)

    print(get_entity_list(organization))

if __name__ == '__main__':
    main()