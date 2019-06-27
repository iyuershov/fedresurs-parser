import  urllib.request
# from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def main():
    print(get_html('https://fedresurs.ru'))

if __name__ == '__main__':
    main()