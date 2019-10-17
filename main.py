# import requests

# payload = {'GO': 'status.htm',
# 'pws': 'a67cd125043a369b9ab9ce0d0ae79158',
# 'usr': 'admin',
# 'ui_pws': 'password'}
# url = 'http://192.168.1.1/login.cgi'
# response = requests.post(url, data=payload)
# 
# print(response.text)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tabulate import tabulate
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

try:
    browser.get('http://192.168.1.1')
    time.sleep(5)
    browser.switch_to.frame(1) # Find the search box

    # Password
    password_input = browser.find_element_by_name('ui_pws')
    password_input.send_keys('INTRODUCIR AQUI LA CONTRASEÑA DEL ROUTER')
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Configuración Avanzada
    browser.switch_to.default_content()
    browser.switch_to.frame(0)
    browser.find_element_by_id('hmenu-advconfig').click()
    time.sleep(5)

    # Pestaña NAT/PAT
    browser.switch_to.default_content()
    browser.switch_to.frame(1)
    browser.find_element_by_id('home-dashboard').find_element_by_tag_name( 'ul').find_elements_by_tag_name('li')[1].click()
    time.sleep(5)

    # Tabla NAT

    tabla_nat = browser.find_element_by_id('rules').find_element_by_tag_name('tbody')
    # print(tabla_nat.get_attribute('innerHTML'))

    # Listado de Reglas NAT
    reglas_nat = tabla_nat.find_elements_by_class_name('otherheader')[1:]
    filas = []
    cabeceras = ['Servicio', 'Estado','Puerto (interno)','Puerto (externo)','Protocolo']
    for tr in reglas_nat:
        # print(tr.get_attribute('innerHTML'))
        columnas = tr.find_elements_by_tag_name('td')
        if("internet-avail" in columnas[0].get_attribute('innerHTML')):
            estado = "OK"
        else:
            estado = "KO"
        filas.append([columnas[1].text,estado,columnas[2].text,columnas[3].text,columnas[4].text])

    print(tabulate(filas, headers=cabeceras, tablefmt='orgtbl'))

    browser.quit()
    
except Exception as exception:
    print("[Error]: "+str(exception))
    browser.quit()
