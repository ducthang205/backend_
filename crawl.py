# importing necessary packages

from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

engine = create_engine("sqlite:///./sql_app.db")


def send_mail():
    print("send mail")


def real_time():
    while 1 == 1:
        get_data()
        sleep(120)


def get_data():
    last = []
    _engine = create_engine("sqlite:///./sql_app.db")
    _conn = _engine.connect()
    rs = _conn.execute('SELECT * FROM records ORDER BY id DESC LIMIT 1')
    for row in rs:
        last.append(row)
    # print(last[0])
    list = []
    rs = _conn.execute('SELECT * FROM condition ORDER BY id DESC LIMIT 1')

    for row in rs:
        list.append(row)

    # print(list[0])
    price_check = int(list[0][2].replace(",", ""))
    vol_check = int(list[0][3].replace(",", ""))
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver.minimize_window()
    user = "supergalaxy205@gmail.com"
    _pass = "123456"
    url = "https://finance.vietstock.vn/CTI/thong-ke-giao-dich.htm"
    driver.get(url)
    button = driver.find_element(By.XPATH, "/html/body/div[2]/div[6]/div/div[2]/div[2]/a[3]")
    driver.execute_script("arguments[0].click();", button)
    username = driver.find_element(By.XPATH, "//*[@id=\"txtEmailLogin\"]")
    username.clear()
    username.send_keys(user)
    password = driver.find_element(By.XPATH, "//*[@id=\"txtPassword\"]")
    password.clear()
    password.send_keys(_pass)
    button = driver.find_element(By.XPATH, "//*[@id=\"btnLoginAccount\"]")
    driver.execute_script("arguments[0].click();", button)
    # button = driver.find_element(By.XPATH, "//*[@id=\"view-tab\"]/li[2]/a")
    # driver.execute_script("arguments[0].click();", button)
    sleep(8)
    data = []
    for a in range(1):

        j = 0

        check = 0
        while 1 == 1:
            if check == 1:
                break
            for i in range(15):
                # try:
                id = i + j * 15

                time = driver.find_element(By.XPATH,
                                           "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                               i + 1) + "]/td[1]")

                price = driver.find_element(By.XPATH,
                                            "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                i + 1) + "]/td[2]/span/span[1]")

                change = driver.find_element(By.XPATH,
                                             "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                 i + 1) + "]/td[2]/span/span[2]")

                per = driver.find_element(By.XPATH,
                                          "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                              i + 1) + "]/td[2]/span/span[4]")

                vol = driver.find_element(By.XPATH,
                                          "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                              i + 1) + "]/td[3]")

                totalVol = driver.find_element(By.XPATH,
                                               "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                   i + 1) + "]/td[3]")

                density = driver.find_element(By.XPATH,
                                              "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                  i + 1) + "]/td[4]")
                if int(price.text.replace(",", "")) > price_check and int(vol.text.replace(",", "")) > vol_check:
                    send_mail()
                value = {"id": 0, "time": time.text, "price": price.text, "change": change.text, "per": per.text,
                         "vol": vol.text,
                         "totalVol": totalVol.text, "density": density.text}
                if value == last:
                    check = 1
                    break
                _engine = create_engine("sqlite:///./sql_app.db")
                _conn = _engine.connect()
                _conn.execute("INSERT INTO records (time, price,change,per, vol, totalVol, density) "
                              "VALUES (:time, :price,:change,:per, :vol, :totalVol, :density)", time=time.text,
                              price=price.text, change=change.text, per=per.text, vol=vol.text, totalVol=totalVol.text,
                              density=density.text)

                data.append(value)
                print(value)
                i = i + 1
            # except:
            #
            #     break
            j = j + 1
            button = driver.find_element(By.XPATH, "//*[@id=\"btn-page-next\"]")
            driver.execute_script("arguments[0].click();", button)

    return data



