# rosseti-domoticz

Simple script for checking site for new events from https://lk.mrsksevzap.ru/PowerInterruptions/AllInterruptions and add them /
to Domoticz text dummy sensor. You can use it for your own ideas.
For example - notify with telegram\sms about new event (please use DzVents\Blockly\Lua or Python for it)

Простенький скрипт для проверки новых событий о плановых работах МРСК (Россети) https://lk.mrsksevzap.ru/PowerInterruptions/AllInterruptions и создание /
текстового датчика в Domoticz. Можно использовать в различных сценариях
Например для уведомления о новом событии по телеграм или смс (необходимо использовать DzVents\Blockly\Lua или Python в Domoticz)

# Installation

git clone <%repasitoryname%>
pip3 install -U .requirements.txt
cd rosseti-domoticz.py

Create conf.cfg and change your settings 

nano conf.cfg
domoticz_server: 'localhost'  # domoticz server IP\name 
domoticz_port: '505'          # domoticz server port
username: 'ivan'              # domoticz username for auth
password: 'pechkin'           # domoticz username password
domoticz_idx: '115'           # id new text sensor
region: 'Карелия'             # region for searching new events
days: '7'                     # time range for searching new events

Run
python3 ./rosseti-domoticz.py

ll data logging to .rosseti-domoticz.txt

# Please read more 
https://magapov.blogspot.com/2021/09/rosseti-domoticz-pro.html
