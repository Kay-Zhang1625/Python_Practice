import csv
import requests
from bs4 import BeautifulSoup


def getData(link):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    resp = requests.post(link, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    items = soup.select('.zg-item-immersion')
    return items


def saveData(items):
    row_list = []
    for item in items:
        rank = item.select('.zg-badge-text')[0].text
        item_name = item.select('div.p13n-sc-truncate-desktop-type2')[0].text.strip()
        item_link = 'https://www.amazon.com/' + item.find('a', href=True).get('href')
        img_src = item.find('img')['src']
    
        data = {}
        data['rank'] = rank
        data['item_name'] = item_name
        data['item_link'] = item_link
        data['img_src'] = img_src

        row_list.append(data)

    return row_list


def writeCSVfile(row_list):
    with open('/Users/kayzhang/Github/Public/Python_Practice/brushes.csv', 'w') as f:
        headers = ['rank', 'item_name', 'item_link', 'img_src']
        dict_writer = csv.DictWriter(f, headers)
        dict_writer.writeheader()
        dict_writer.writerows(row_list)


if __name__ == "__main__":
    page1 = 'https://www.amazon.com/Best-Sellers-Beauty-Makeup-Brush-Sets-Kits/zgbs/beauty/11059451/ref=zg_bs_pg_2?_encoding=UTF8&pg=1'
    page1_data = saveData(getData(page1))
    page2 = 'https://www.amazon.com/Best-Sellers-Beauty-Makeup-Brush-Sets-Kits/zgbs/beauty/11059451/ref=zg_bs_pg_2?_encoding=UTF8&pg=2'
    page2_data = saveData(getData(page2))
    
    page1_data.extend(page2_data)

    writeCSVfile(page1_data)
