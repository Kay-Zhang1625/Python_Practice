import lxml.html
import re
import requests
import pymysql
import time

from lxml import etree


# 此定義使用 pymysql 套件將資料傳入 MySQL，請先在 MySQL 裡建立好資料庫 "tami"
def writeIntoDatabase(data):
    # 建立資料庫連線
    conn = pymysql.connect(host='localhost',
                            user='root',
                            password='test',
                            port=3306,                       
                            db='tami',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with conn.cursor() as cursor:
            # 於資料庫中新建表 "tamoRowData"
            sql_createTb =  """
                            CREATE TABLE tamiRowData(
                                公司名稱 varchar(60), 公司電話 varchar(50), 公司傳真 varchar(50), 公司地址 varchar(80),
                                工廠電話 varchar(50), 工廠傳真 varchar(50), 工廠地址 varchar(80), 公司網址 varchar(100),
                                資本額 varchar(30), 電子郵件 varchar(100), 員工人數 varchar(10), 主要產品 varchar(800)
                            );
                            """
            cursor.execute(sql_createTb)
            
            # 將資料打包傳入資料庫中
            sql_insertData = """
                            INSERT INTO tamiRowData (公司名稱, 公司電話, 公司傳真, 公司地址, 工廠電話, 工廠傳真, 工廠地址, 公司網址,
                                資本額, 電子郵件, 員工人數, 主要產品) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
            dataNumber = 0
            for keyOne, valueOne in data.items():
                for keyTwo, valueTwo in valueOne.items():
                    for keyThree, valueThree in valueTwo.items():
                        dataNumber += 1
            val = [list(range(12)) for _ in range(dataNumber)]
            count = 0
            for keyOne, valueOne in data.items():
                for keyTwo, valueTwo in valueOne.items():
                    for keyThree, valueThree in valueTwo.items():
                        val[count].clear()
                        for value in valueThree:
                            val[count].append(value)
                        val[count] = list(val[count])
                        count += 1
            cursor.executemany(sql_insertData, val)
            conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    t1 = time.time()
    print('------ Start ------')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    
    linkList = {}
    categoryOneLinkList = []  # 產品分類URL列表
    categoryOneNameList = []
    
    for i in range(1, 5):
        res = requests.get(
            "http://www.tami.org.tw/category/product-new1.php?on=" + str(i), headers=headers)
        content = res.content.decode()
        originHTML = etree.HTML(content)  # 原始HTML文件

        categoryOneA = originHTML.xpath("//a[@class='product-link']")  # 產品分類
        for index in range(len(categoryOneA)):
            categoryOneLink = categoryOneA[index].get("href")
            categoryOneLink = "http://www.tami.org.tw/category/" + categoryOneLink
            categoryOneLinkList.append(categoryOneLink)
            categoryOneName = re.findall(r"\s.+", categoryOneA[index].text.strip())[0].split()
            categoryOneNameList.append(categoryOneName)
            linkList[categoryOneName[0]] = {}

        try:
            categoryOneB = originHTML.xpath("//a[@class='product-link2']")  # 產品分類
            for index in range(len(categoryOneB)):
                categoryOneLink = categoryOneB[index].get("href")
                categoryOneLink = "http://www.tami.org.tw/category/" + categoryOneLink
                categoryOneLinkList.append(categoryOneLink)
                categoryOneName = re.findall(r"\s.+", categoryOneB[index].text.strip())[0].split()
                categoryOneNameList.append(categoryOneName)
                linkList[categoryOneName[0]] = {}
        except:
            pass


    time.sleep(2)
    # print(linkList)

    print('------ 正在爬取第二層資料 ------')

    # 產品分類第二層
    for indexOne in range(len(categoryOneLinkList)):
        resTwo = requests.get(categoryOneLinkList[indexOne], headers=headers)
        contentTwo = resTwo.content.decode()
        originHTMLTwo = etree.HTML(contentTwo)  # 原始HTML文件
        categoryTwo = originHTMLTwo.xpath("//a[@class='product-link']")  # 產品分類
    
        categoryTwoLinkList = []  # 產品分類URL列表
        categoryTwoNameList = []
        for indexTwo in range(len(categoryTwo)):
            categoryTwoLink = categoryTwo[indexTwo].get("href")
            categoryTwoLink = "http://www.tami.org.tw/category/" + categoryTwoLink
            categoryTwoLinkList.append(categoryTwoLink)
            categoryTwoName = re.findall(r"\s.+", categoryTwo[indexTwo].text)[0].split()
            categoryTwoNameList.append(categoryTwoName)
            linkList[categoryOneNameList[indexOne][0]][categoryTwoName[0]] = {}

        time.sleep(2)

        for indexTwo in range(len(categoryTwoLinkList)):
            resThree = requests.get(categoryTwoLinkList[indexTwo], headers=headers)
            contentThree = resThree.content.decode()
            originHTMLThree = etree.HTML(contentThree)  # 原始HTML文件
            companysNameXpath = originHTMLThree.xpath("//a[@class='company-word3']")  # 產品分類

            companysNameLinkList = []  # 產品分類URL列表
            companysNameList = []
            for indexThree in range(len(companysNameXpath)):
                companysNameLink = companysNameXpath[indexThree].get("onclick")
                companysNameLinkpart = re.findall(r"\w?\d+", companysNameLink)[0]
                companysNameLink = "http://www.tami.org.tw/category/contact_2.php?ms=" + companysNameLinkpart + "&on=1"
                companysNameLinkList.append(companysNameLink)
                companysName = companysNameXpath[indexThree].text.split()
                companysNameList.append(companysName)

                resFour = requests.get(companysNameLink, headers=headers)
                originHTMLFour = etree.HTML(resFour.text)  # 原始HTML文件
                try:
                    companyName = originHTMLFour.xpath("//span[contains(@class, 'company-top')]/text()")[0].split()
                    companyPhone = originHTMLFour.xpath("//tr[2]//td[contains(@class, 'list_td')][2]/text()")[0].split()
                    companyFax = originHTMLFour.xpath("//tr[2]//td[contains(@class, 'list_td')][4]/text()")[0].split()
                    companyAddress = originHTMLFour.xpath("//tr[3]//td[contains(@class, 'list_td')][2]/text()")[0].split()
                    factoryPhone = originHTMLFour.xpath("//tr[4]//td[contains(@class, 'list_td')][2]/text()")[0].split()
                    factoryFax = originHTMLFour.xpath("//tr[4]//td[contains(@class, 'list_td')][4]//font/text()")[0].split()
                    factoryAddress = originHTMLFour.xpath("//tr[5]//td[contains(@class, 'list_td')][2]/text()")[0].split()
                    website = originHTMLFour.xpath("//tr[6]//td[contains(@class, 'list_td')][2]//a/@href")[0].split()
                    capital = originHTMLFour.xpath("//tr[6]//td[contains(@class, 'list_td')][4]/text()")[0].split()
                    email = originHTMLFour.xpath("//tr[7]//td[contains(@class, 'list_td')][2]//a/text()")[0].split()
                    employeeNumber = originHTMLFour.xpath("//tr[7]//td[contains(@class, 'list_td')][4]/text()")[0].split()
                    products = originHTMLFour.xpath("//tr[8]//td[contains(@class, 'list_td')][2]/text()")[0].split()
                    linkList[categoryOneNameList[indexOne][0]][categoryTwoNameList[indexTwo][0]][companysName[0]] = \
                        [companyName[0], companyPhone[0], companyFax[0], companyAddress[0], factoryPhone[0], factoryFax[0], factoryAddress[0], website[0], capital[0], email[0], employeeNumber[0], products[0]]
                except:
                    pass

    print('------ 資料爬取完畢 ------')
    print('------ 資料正在匯入 MySQL ------')
    writeIntoDatabase(linkList)
    print('------ End ------')
    t2 = time.time()
    print('總共耗時' + str(round(t2-t1), 2) + '秒')