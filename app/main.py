from urllib import request, parse
# from bs4 import BeautifulSoup

def get_html(url):
    response = request.urlopen(url)
    return response.read()

def main():
    print("Введите название организации:")
    entity = input()
    query = "https://fedresurs.ru/search/entity?name=" + parse.quote(entity)
    print(get_html(query))

if __name__ == '__main__':
    main()