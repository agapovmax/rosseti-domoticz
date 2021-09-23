import requests
import datetime
import config
from requests.auth import HTTPBasicAuth

# Берем инфу из файла настроек
conf = config.Config('config.cfg')
# Берем из конфига кол-во дней для диапазона выдачи с и по
days = conf['days']
# Вывод дат в нужном диапазоне в неделю 
fulltime = datetime.datetime.now()
currdate = datetime.datetime.today()
todate = (datetime.datetime.today()).strftime("%d.%m.%Y")
fromdate = (currdate - datetime.timedelta(days=int(days))).strftime("%d.%m.%Y")

# Проверяем новые события на МРСК с настройками из conf.cfg
url = 'https://lk.mrsksevzap.ru/Ajax/Interruptions?region=&district=&settlement=&manualSettlement=&street=&isManualStreet=true&manualStreet=&house=&page=1&fieldName=OutageDate&orderDirection=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
params = {
    'fullAddress': conf['fulladdress'] + ', ' + conf['street'] + ', ' + conf['house'],
    'region':  conf['region'],
    'isSettlement': 'true',
    'from': fromdate,
    'to': todate,
    }

r = requests.get(url, headers=headers, params = params).json()

# Проверяем, есть ли работы
count = r.get('TotalCount')
if count == 0:
    result = 'С ' + fromdate + ' по ' + todate + ' нет плановых работ'
else:
    for item in r['items']:
        result = ( item['Description'] + ' отключение по адресу ' + item['Address'] + ' c ' + item['From'] + ' по ' + item['To'] + ' ' + item['Condition'])
        print('Есть запись: ')
        print(result)

# Проверяем текущее значение idx в domoticz
d_url = 'http://' + conf['domoticz_server'] + ':' + conf['domoticz_port'] + '/json.htm?'
d_headers = {
    'User-Agent' : 'curl/7.61.0',
    'Charset' : 'UTF-8'
}
d_params = {
    'type' : 'devices',
    'rid' : conf['domoticz_idx']
}
d_check = requests.get(d_url, headers=d_headers, params=d_params, auth=HTTPBasicAuth(conf['username'], conf['password'])).json()

for item in d_check['result']:
    d_result = item['Data']
    print('Текущая запись в домотикз')
    print(d_result)

# Обновляем idx в domoticz
du_params = {
    'type' : 'command',
    'param': 'udevice',
    'idx': conf['domoticz_idx'],
    'nvalue': '0',
    'svalue' : result
    }

if result == 0:
    print('Нет новых событий!')
else:
    print('Запись найдена!')
    if d_result != result:
        print('Обновляем запись...')
        # Пишем в файл данные
        # Открываем лог файл для записи
        f = open('rosseti-domoticz.txt', 'a')
        f.write(str(fulltime) + '; ' + result + '\n')
        f.close()
        s = requests.post(d_url,headers=d_headers,params=du_params, auth=HTTPBasicAuth(conf['username'], conf['password']))
    else:
        print('Нечего обновлять')