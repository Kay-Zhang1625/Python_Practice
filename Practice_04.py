import csv
import requests
from bs4 import BeautifulSoup


def top100Page(link):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    resp = requests.post(link, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    items = soup.select('.zg-item-immersion')
    return items


def top100(items):
    row_list = []
    for item in items:
        rank = item.select('.zg-badge-text')[0].text
        item_name = item.select('div.p13n-sc-truncate-desktop-type2')[0].text.strip()
        item_link = 'https://www.amazon.com' + item.find('a', href=True).get('href')
        img_src = item.find('img')['src']
    
        data = {}
        data['rank'] = rank
        data['item_name'] = item_name
        data['item_link'] = item_link
        data['img_src'] = img_src

        row_list.append(data)

    return row_list


def productDetail(link):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    resp = requests.post(link, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # store = soup.select_one('a#bylineInfo').text
    # store_link = 'https://www.amazon.com' + soup.find('a', id='bylineInfo', href=True).get('href')
    # price = soup.select_one('span#priceblock_saleprice').text
    star = soup.select_one('span.a-size-medium.a-color-base').text
    reviews_mentioned_s = soup.find(id='reviewsMedley').find(class_='a-fixed-left-grid-col a-col-right').find(class_='cr-lazy-widget cr-summarization-lighthut')
    # reviews_mentioned = []
    # for i in reviews_mentioned_s:
    #     reviews = i.select('span a')
    #     reviews_mentioned.append(reviews)

    # data = {}
    # data['store'] = store
    # data['store_link'] = store_link
    # data['price'] = price
    # data['star'] = star
    # data['reviews_mentioned'] = reviews_mentioned[0]

    return star, reviews_mentioned_s


# def getDetailInfo():



def writeCSVfile(row_list):
    with open('/Users/kayzhang/Github/Public/Python_Practice/brushes.csv', 'w') as f:
        headers = ['rank', 'item_name', 'item_link', 'img_src']
        dict_writer = csv.DictWriter(f, headers)
        dict_writer.writeheader()
        dict_writer.writerows(row_list)


if __name__ == "__main__":
    # page1 = 'https://www.amazon.com/Best-Sellers-Beauty-Makeup-Brush-Sets-Kits/zgbs/beauty/11059451/ref=zg_bs_pg_2?_encoding=UTF8&pg=1'
    # page1_data = top100(top100Page(page1))
    # page2 = 'https://www.amazon.com/Best-Sellers-Beauty-Makeup-Brush-Sets-Kits/zgbs/beauty/11059451/ref=zg_bs_pg_2?_encoding=UTF8&pg=2'
    # page2_data = top100(top100Page(page2))
    
    # page1_data.extend(page2_data)

    # writeCSVfile(page1_data)
    url = 'https://www.amazon.com/BS-MALL-Brushes-Synthetic-Foundation-Concealers/dp/B01LZ3RLPC/ref=zg_bs_11059451_1?_encoding=UTF8&psc=1&refRID=JSS5HDZRQG2QGN8DYZ2E'
    print(productDetail(url))
