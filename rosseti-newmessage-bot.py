from json import encoder
from typing import Text
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
from requests.auth import HTTPBasicAuth
import datetime
import time
import pickle
import config

# Берем настройки из файла конфигурации
conf = config.Config('config.cfg')

# Задержка перед выполнением скрипта \
# Необходима для уверенности, что это не оперативное переключение
time.sleep(int(conf['timer_delay']))

# Получаем текущее время отключения электричества и день 
today = (datetime.datetime.today()).strftime("%d.%m.%Y")
off_time = (datetime.datetime.today()).strftime("%H:%M")

# Проверяем статус датчика наличия электричества
d_url = 'http://' + conf['domoticz_server'] + ':' + conf['domoticz_port'] + '/json.htm?'
d_headers = {
    'User-Agent' : 'curl/7.61.0',
    'Charset' : 'UTF-8'
}
d_params = {
    'type' : 'devices',
    'rid' : conf['domoticz_power_idx']
}
d_check = requests.get(d_url, headers=d_headers, params=d_params, auth=HTTPBasicAuth(conf['domoticz_username'], conf['domoticz_password'])).json()
for item in d_check['result']:
    d_result = item['Status']
    print('Текущий статус электричества: ' + d_result)


def new_message(url, text):
    # Готовим Chrome к режиму headless
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options,
      service_args=['--log-path=rosseti-newmessage.log'])

    #Запускаем хром и входим в личный кабинет
    #driver = webdriver.Chrome()
    driver.get('https://xn--80aaafp0bqweeid1o.xn--p1ai/platform/portal/cons_main')
    time.sleep(1)
    username = driver.find_element_by_xpath('//*[starts-with(@id, "workplaceTopForm:j_idt")]')
    username.click()
    username = driver.find_element_by_id("workplaceTopForm:j_username")
    username.click()
    username.send_keys(conf['ss_username'])
    time.sleep(1)
    username = driver.find_element_by_id("workplaceTopForm:j_password")
    username.click()
    username.send_keys(conf['ss_password'])
    time.sleep(1)
    username = driver.find_element_by_id("workplaceTopForm:loginBtn")
    username.click()
    time.sleep(1)

    # Получаем куки 
    pickle.dump(driver.get_cookies(), open('cookie_rosseti', 'wb'))
    driver.get(url=url)
    time.sleep(2)
    for cookie in pickle.load(open(f"cookie_rosseti", 'rb')):
        driver.add_cookie(cookie)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(1)
    msg_type = driver.find_element_by_id("workplaceForm:cons_messages_wp:dataObjectControllerInstance_sections:sMw_widgetTimeline:dataObjectControllerInstanceFields__classifierProblem__Value:ac")
    msg_type.click()

    # Выбираем тему сообщения из выпадающего списка
    msg_type_choose = Select(driver.find_element_by_id("workplaceForm:cons_messages_wp:dataObjectControllerInstance_sections:sMw_widgetTimeline:dataObjectControllerInstanceFields__classifierProblem__Value:ac_input"))
    msg_type_choose.select_by_visible_text('Систематические отключения электроэнергии')
    ##### Остальные варианты
    #msg_type_choose.select_by_visible_text('Колебания напряжения / Низкое напряжение')
    time.sleep(1)

    # Вводим полный адрес
    msg_address = driver.find_element_by_id("suggest")
    msg_address.send_keys(conf['ss_fulladdress'])
    time.sleep(1)
    # Выбираем из выпадающего списка который появляется после ввода полного адреса кнопкой ВНИЗ и ВВОД
    action = ActionChains(driver)
    action.send_keys(Keys.ARROW_DOWN)
    time.sleep(3)
    action.send_keys(Keys.RETURN).perform()
    time.sleep(3)

    # Заполняем текст обращения
    msg_text = driver.find_element_by_id("workplaceForm:cons_messages_wp:dataObjectControllerInstance_sections:sMw_widgetTimeline:dataObjectControllerInstanceFields__aText__Value")
    msg_text.click()
    msg_text.send_keys(text)
    time.sleep(3)

    # Жмем кнопку "Отправить сообщение"
    time.sleep(3)
    msg_send = driver.find_element_by_id("workplaceForm:cons_messages_wp:dataObjectControllerInstance_sections:sMw_widgetTimeline:pMw_btnBack:dataObjectControllerInstanceFields__btnSend__Value")
    msg_send.click()
    # Добавляем задержку для обработки формы и отправки её на сервер
    time.sleep(10)
    driver.close()
    driver.quit()
    
def main():
    if d_result == 'On':
        new_message(url='https://xn--80aaafp0bqweeid1o.xn--p1ai/platform/portal/cons_createMsg',text='Сегодня ' + today + ' в ' + off_time + ' отключили электричество. Плановых работ сегодня нет')
    else:
        print("Электричество восстановлено")

if __name__ == "__main__":
    main()