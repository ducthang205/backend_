# importing necessary packages
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import smtplib

engine = create_engine("sqlite:///./sql_app.db")


def send_mail(value):
    print("send mail")
    sender_email = "ducthang.nguyen205@gmail.com"
    rec_email = "supergalaxy205@gmail.com"
    password = "thangytbg"
    message = "Mã chứng khoán của bạn đã yêu cầu. Thông tin là thời gian: " + value["time"] + " giá: " + value["price"]
    mes = message.encode("utf-8")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender_email, password)
        print("Login success")
        server.sendmail(sender_email, rec_email, mes)
        print("Email has been sent to ", rec_email)
    except:
        print("Message wasn't sent to ", rec_email)


def real_time():
    while 1 == 1:
        get_data()
        print("Stop 2m ....")
        sleep(120)


def find_last_time():
    last = []
    _engine = create_engine("sqlite:///./sql_app.db")
    _conn = _engine.connect()
    rs = _conn.execute('SELECT time FROM records')
    for row in rs:
        last.append(row)
    last_time = datetime.strptime("9:0:0", '%H:%M:%S')
    for l in last:
        if datetime.strptime(str(l[0]), '%H:%M:%S') > last_time:
            last_time = datetime.strptime(str(l[0]), '%H:%M:%S')
    print(last_time)
    return last_time


def get_data():
    last = find_last_time()
    _engine = create_engine("sqlite:///./sql_app.db")
    _conn = _engine.connect()

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

                    value = {"id": 0, "time": time.text, "price": price.text, "change": change.text, "per": per.text,
                             "vol": vol.text,
                             "totalVol": totalVol.text, "density": density.text}
                    print(last)
                    print(datetime.strptime(time.text, '%H:%M:%S'))
                    if datetime.strptime(time.text, '%H:%M:%S') <= last:

                        check = 1
                        break
                    if int(price.text.replace(",", "")) > price_check and int(vol.text.replace(",", "")) > vol_check:
                        print(price.text.replace(",", ""), price_check, vol.text.replace(",", ""), vol_check)
                        send_mail(value)

                    _engine = create_engine("sqlite:///./sql_app.db")
                    _conn = _engine.connect()
                    _conn.execute("INSERT INTO records (time, price,change,per, vol, totalVol, density) "
                                  "VALUES (:time, :price,:change,:per, :vol, :totalVol, :density)", time=time.text,
                                  price=price.text, change=change.text, per=per.text, vol=vol.text,
                                  totalVol=totalVol.text,
                                  density=density.text)

                    data.append(value)

                    i = i + 1
                # except:
                #
                #     break
            if check == 1:

                break
            j = j + 1
            button = driver.find_element(By.XPATH, "//*[@id=\"btn-page-next\"]")
            driver.execute_script("arguments[0].click();", button)

    return data
