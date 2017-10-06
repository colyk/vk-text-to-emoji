import requests
from bs4 import BeautifulSoup
import json


def get_html(URL):
    response = requests.get(URL)
    return response.text


def get_date(html):
    dic = {}
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all('table',class_='smile_table')
    # tab1 = tables[0]
    for j in tables:
        # print(j)
        for i in j.find_all('tr')[1:]:
            try:
                smile_code = i.find('td', class_ = 'smile_code').text.strip()
            except:
                continue
            description = i.find('td', class_ = 'description').text.strip()
            if description == '':
            	continue
            dic[smile_code] = description.lower()
    print(len(dic))
    with open("json_out.txt", "w", encoding='utf-8') as file:
        json.dump(dic, file, indent=2, ensure_ascii =False, sort_keys=True)





def main():
    URL = 'http://www.kody-smajlov-vkontakte.ru/'
    html = get_html(URL)
    get_date(html)

if __name__ == '__main__':
    main()
