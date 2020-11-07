import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


print('品牌：全品牌、得意、柔情、春風、舒潔、五月花')
tissueBrand = input('請輸入品牌：')


driver = webdriver.Chrome('/Users/kayzhang/Downloads/python_sql_class/chromedriver')
driver.get('https://www.ey.gov.tw/Page/304401ED1702010C')

# Create blank list and put crawling information in blank list.
# Period - for storing selector's options temporarily
# row_list - for storing crawling data temporarily
period = []
row_list = []

# Select the options in period from 106/1 to 109/9 (Year/Month).
# And crawl the information from the searched list.
for i in range(106, 110):
    select_category = Select(driver.find_element_by_name('ctl00$ctl09$ddlCategory'))
    select_category.select_by_visible_text(u'衛生紙')

    time.sleep(0.1)

    for j in range(1, 13):
        for op in select_periodStart.options:
            period.append(op.text.strip())
        if str(i) + '年' + str(j) + '月' in period:
            select_periodStart = Select(driver.find_element_by_name('ctl00$ctl09$ddlPeriodStart'))
            select_periodStart.select_by_visible_text(u''+ str(i) + '年' + str(j) + '月')

            time.sleep(0.1)

            select_periodEnd = Select(driver.find_element_by_name('ctl00$ctl09$ddlPeriodEnd'))
            select_periodEnd.select_by_visible_text(u''+ str(i) + '年' + str(j) + '月')

            time.sleep(0.1)

            search_btn = driver.find_element_by_css_selector('.top_bar2')
            search_btn.click()

            time.sleep(1)

            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            elements = soup.select('#tblInfo tr')[2:]

            for element in elements:
                try:
                    year = i
                    month = j
                    product_name = element.find(headers='ProductName').select('a')[0].text.strip()
                    price_min = element.find(headers='period MinVal').text.strip()
                    price_max = element.find(headers='period MaxVal').text.strip()
                    data = {}
                    data['year'] = year
                    data['month'] = month
                    data['product_name'] = product_name
                    data['price_min'] = price_min
                    data['price_max'] = price_max
                    row_list.append(data)
                except IndexError:
                    pass

        else:
            pass
        
        period.clear()

driver.quit()


# Organize data from row_list.  Group product prices by brand name.
# There are 7 kinds of products in row_list.  Use 'count' to ensure the data inside the loop of 7.
product_time = []
product_price = []
count = 1

for i in range(len(row_list)):
    if count % 7 == 1:
        product_time.append(str(row_list[i]['year']) + '/' + str(row_list[i]['month']))
    if row_list[i]['price_min'] == '-' and row_list[i]['price_max'] == '-':
        row_list[i]['price_min'] = row_list[i - 7]['price_min']
        row_list[i]['price_max'] = row_list[i - 7]['price_max']
    price = [(int(row_list[i]['price_min']) + int(row_list[i]['price_max'])) / 2]
    if i // 7 < 1:
        product_price.append(price)
        count += 1
    else:
        product_price[i % 7].extend(price)
        count += 1


# We use only 5 kinds of prodcut in this project.
# Count average price for these products.
products_avgPrice = []
for i in range(len(product_price[0])):
    avgPrice = (product_price[0][i] + product_price[1][i] + product_price[2][i] + product_price[3][i] + product_price[6][i]) / 5
    products_avgPrice.append(avgPrice)


# Rename the request and pick up the data needed.
if tissueBrand == '得意':
    tissueBrand = '得意抽取式衛生紙'
    product_price = product_price[0]
elif tissueBrand == '柔情':
    tissueBrand = '柔情抽取式衛生紙'
    product_price = product_price[1]
elif tissueBrand == '春風':
    tissueBrand = '春風平版衛生紙'
    product_price = product_price[2]
elif tissueBrand == '舒潔':
    tissueBrand = '舒潔平版衛生紙'
    product_price = product_price[3]
elif tissueBrand == '五月花':
    tissueBrand = '五月花盒裝面紙'
    product_price = product_price[6]
else:
    pass


# Read csv file downloaded from Google Trend.
searchEngine = []

searchEngine = pd.read_csv('/Users/kayzhang/Downloads/multiTimeline.csv')
searchEngine = searchEngine.loc['2017-01':, :]
searchEngine = searchEngine.reset_index()['類別：所有類別']
searchEngine = searchEngine.tolist()

for i in range(len(searchEngine)):
    searchEngine[i] = int(searchEngine[i])


# Set Traditional Chinese font for displaying on the line chart.
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False


# Draw a line chart for all brands or one brand.
# X-axis - the time from 2017 to 2020.
# Y-axis - product price on left y-axis(ax1) and counts from Google search on right y-axis(ax2).
if tissueBrand == '全品牌':
    fig, ax1 = plt.subplots(figsize=(14,6))
    plt.title('2017至2020年衛生紙' + tissueBrand + '價格與搜尋次數折線圖')
    plt.xlabel('年份/月份')
    plt.xticks(range(len(product_time)), product_time, rotation=45)
    ax2 = ax1.twinx()

    ax1.set_ylabel('衛生紙價格', color='black')
    l1, = ax1.plot(range(len(product_price[0])), product_price[0], color='tab:orange', alpha=0.4)
    l2, = ax1.plot(range(len(product_price[1])), product_price[1], color='tab:green', alpha=0.4)
    l3, = ax1.plot(range(len(product_price[2])), product_price[2], color='tab:red', alpha=0.4)
    l4, = ax1.plot(range(len(product_price[3])), product_price[3], color='tab:purple', alpha=0.4)
    l5, = ax1.plot(range(len(product_price[6])), product_price[6], color='tab:blue', alpha=0.4)
    l6, = ax1.plot(range(len(products_avgPrice)), products_avgPrice, color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2.set_ylabel('搜尋熱度', color='tab:gray')
    ax2.plot(range(len(searchEngine)), searchEngine, color='tab:gray')
    ax2.tick_params(axis='y', labelcolor='tab:gray')

    plt.legend(handles=[l1, l2, l3, l4, l5, l6],
               labels=['得意抽取式衛生紙', '柔情抽取式衛生紙', '春風平版衛生紙', '舒潔平版衛生紙', '五月花盒裝面紙', '全品牌平均價格'],
               loc='best')

    fig.tight_layout()
    ax1.grid(ls='--')
    plt.show()
else:
    fig, ax1 = plt.subplots(figsize=(14,6))
    plt.title('2017至2020年' + tissueBrand + '價格與搜尋次數折線圖')
    plt.xlabel('年份/月份')
    plt.xticks(range(len(product_time)), product_time, rotation=45)
    ax2 = ax1.twinx()

    ax1.set_ylabel('衛生紙價格', color='black')
    l0, = ax1.plot(range(len(product_price)), product_price, color='black', alpha=0.75)
    l1, = ax1.plot(range(len(products_avgPrice)), products_avgPrice, color='tab:orange', alpha=0.4, ls='--')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2.set_ylabel('搜尋熱度', color='tab:blue')
    ax2.plot(range(len(searchEngine)), searchEngine, color='tab:blue', alpha=0.75)
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.legend(handles=[l0, l1], labels=[tissueBrand, '全品牌平均價格'], loc='best')

    fig.tight_layout()
    ax1.grid(ls='--')
    plt.show()