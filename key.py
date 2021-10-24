import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_list_key():
    list_key = []
    urls = []
    for i in range(159):
        urls.append('https://finance.vietstock.vn/doanh-nghiep-a-z?page='+str(i+1))
    data = []
    for page in urls:
        page_url = page
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.minimize_window()
        driver.get(page_url)

        # name = "/html/body/div[1]/div[12]/div/div/div[1]/div/div/div[2]/div/div/div[3]/div[1]/div"
        # a = driver.find_elements_by_xpath(name)
        # print(a)
        # list = [agency.text for agency in a]
        # count = int(str(list[0]).replace("Tổng số ", "").replace((" bản ghi", "")))
        for i in range(20):
            a = driver.find_element(By.XPATH, "//*[@id=\"az-container\"]/div[2]/table/tbody/tr["+str(i+1)+"]/td[2]/a")
            print(a.text)
            data.append(a.text)
        print(data)


# get_list_key()
