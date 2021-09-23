import requests
import datetime
import config

# Берем инфу из файла настроек
conf = config.Config('config.cfg')
# Берем из конфига кол-во дней для диапазона выдачи с и по
days = conf['days']
# Вывод дат в нужном диапазоне в неделю 
fulltime = datetime.datetime.now()
currdate = datetime.datetime.today()
todate = (datetime.datetime.today()).strftime("%d.%m.%Y")
fromdate = (currdate - datetime.timedelta(days=int(days))).strftime("%d.%m.%Y")


def check_new_messages():
    url = 'https://lk.mrsksevzap.ru/Ajax/Interruptions?region=&district=&settlement=&isSettlement=true&manualSettlement=&street=&isManualStreet=true&manualStreet=&house=&page=1&fieldName=OutageDate&orderDirection=1'
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
    r = requests.get(url, headers=headers, params = params)
    a = r.json()

    for item in a['items']:
        result = ( item['Description'] + ' отключение по адресу ' + item['Address'] + ' c ' + item['From'] + ' по ' + item['To'] + ' ' + item['Condition'])
        print(result)


def check_domoticz_message():
    d_url = 'https://' + conf['domoticz_server'] + ':' + conf['domoticz_port']
    d_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Charset' : 'UTF-8'
    }
    d_params = {
        'rid' : conf['domoticz_idx']
    }
    d_check = requests.get(d_url, headers=d_headers, params=d_params)
    print(d_check)

def update_domoticz_message(text):
    d_url = 'https://' + conf['domoticz_server'] + ':' + conf['domoticz_port'] + 'json.htm?type=command&param=udevice&'
    d_params = {
        'type' : 'command',
        'param': 'udevice',
        'idx': conf['idx'],
        'nvalue': '0',
        'svalue': '0',
        'value' : text
    }
    d_update = requests.post(d_url,params=d_params)

if check_new_messages() == 0:
    print('Нет новых событий')
else:
    if check_domoticz_message() != result:
        update_domoticz_message(result)
    else:
        print('Нечего обновлять')







