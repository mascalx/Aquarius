#!/bin/bash

cd /home/pi
curl https://raw.githubusercontent.com/mascalx/Aquarius/master/script/acquario.py -o acquario.py

cd /var/www
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/index.php -o index.php
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/data.php -o data.php
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/update.php -o update.php
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/style.css -o style.css

sudo reboot
