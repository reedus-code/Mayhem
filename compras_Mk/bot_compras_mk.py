from requests_html import HTMLSession #, AsyncHTMLSession
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By

# Ingresar item_url MemoryKings
url = 'https://www.memorykings.pe/producto/354762/geforce-rtx-5090-32gb-512-bit-gigabyte-windforce'


def consulta_stock (html_url):

    session = HTMLSession()
    while True:
        request_html = session.get(html_url)
        #print(r.content) #Contenido HTML
        found = request_html.html.find('#bt-agregar-carrito')
        name_item = request_html.html.find(".body-text strong", first=True).text
        stock_item = request_html.html.xpath("//div[@class='body-text' and text()='Stock: ']//strong/text()")
        print(f'Modelo: {name_item}\nStock: {stock_item[0]}')
        #print(found) #Tipo lista
        if len(found) > 0 and int(stock_item[0]) != 0:
            print('\nHay stock!!!') #Correcto: mandar SMS|Correo (requiere API)
            break
        else:
            print('Sigue sin haber stock :')
        sleep(30)
    return


def waiting_response (driver,content, by = 'id'):
    html_block = None
    if by == 'id':
        while not html_block:
            html_block = driver.find_element(By.ID, content)
            sleep(2)
    elif by == 'xpath':
        while not html_block:
            html_block = driver.find_element(By.XPATH, content)
            sleep(2)
    return html_block


def alert_box (driver, times = False):
    while True:
        try:
            driver.switch_to.alert.accept()
            if times:
                sleep(1)
                driver.switch_to.alert.accept()
            break
        except NoAlertPresentException:
            pass
    return


def web_surfing (url_web):
    chrome_driver_path = '/usr/bin/chromedriver'
    service = webdriver.ChromeService(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url_web)
    
    waiting_response(driver, 'bt-agregar-carrito').click()
    alert_box(driver)
  
    link = waiting_response(driver,"//a[@class='primary-button' and text()='Ver Carrito']", 'xpath').get_attribute('href')
    driver.get(link)

    waiting_response(driver,"//a[@class='primary-button proceder-pedido' and text()='Proceder con la Compra']", 'xpath').click()
    alert_box(driver, True)

    # Ingresar datos (cuidado que esta en texto plano!)
    waiting_response(driver, 'email_login').send_keys('email_prueba@mail.com')
    driver.find_element(By.ID, 'password_login').send_keys('Bazinga')
    driver.find_element(By.ID, 'bt-login').click()
    #... Seguir llenenando datos
    return


def main ():
    consulta_stock(url)
    web_surfing(url)


if __name__ == '__main__':
    main()