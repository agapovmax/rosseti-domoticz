# rosseti-domoticz

Simple script for checking site for new events from https://lk.mrsksevzap.ru/PowerInterruptions/AllInterruptions and add them
to Domoticz text dummy sensor. You can use it for your own ideas.
For example - notify with telegram\sms about new event (please use DzVents\Blockly\Lua or Python for it)

Простенький скрипт для проверки новых событий о плановых работах МРСК (Россети) https://lk.mrsksevzap.ru/PowerInterruptions/AllInterruptions и создание текстового датчика в Domoticz. Можно использовать в различных сценариях
Например для уведомления о новом событии по телеграм или смс (необходимо использовать DzVents\Blockly\Lua или Python в Domoticz)

# rosseti-newmessage-bot

Скрипт для автоматического создания сообщения на портале светлая-страна.рф. Для запуска в консольном (headless) режиме требуется настройка (https://blog.testproject.io/2018/02/20/chrome-headless-selenium-python-linux-servers/), webdriver для Google Chrome (https://chromedriver.chromium.org/downloads), а также  заполнить переменные в config.cfg

# Installation

git clone https://github.com/agapovmax/rosseti-domoticz.git

pip3 install -U .requirements.txt

cd rosseti-domoticz

Create config.cfg and change your settings 

nano config.cfg

domoticz_server: 'localhost'  # domoticz server IP\name 

domoticz_port: '505'          # domoticz server port

username: 'ivan'              # domoticz username for auth

password: 'pechkin'           # domoticz username password

domoticz_data_idx: '115'      # id new text sensor

domoticz_power_idx: '39'      # id sensor for checking power

ss_username: 'ivan@mail.ru'   # creds for светлаястрана.рф

ss_password: 'pechkin666'

ss_fulladdress: 'Россия, Республика Коми, посёлок Задорожный, Кировская улица, 22 ' # Full addres for светлаястрана.рф new message requirements

region: 'Карелия'             # region for searching new events

fulladdress: 'Новая Вилга'    # Address for searching new events

days: '7'                     # time range for searching new events

timer_delay: '1200'           # sleep for checking power returns

# Running
python3 ./rosseti-domoticz.py

All data logging to .rosseti-domoticz.txt

# Running rosseti-newmessage-bot
python3 ./rosseti-newmessage-bot.py

# Result 
![](https://1.bp.blogspot.com/-wVNwpqdPUpA/YU4acQzfoMI/AAAAAAAAeHE/JRJMhEPxHHQWQuFY6phPueqARx-tEaoXACLcBGAsYHQ/w640-h106/rosseti-dummy.JPG)

# Read more 
https://magapov.blogspot.com/2021/09/rosseti-domoticz-pro.html
