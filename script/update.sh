#!/bin/bash

cd /home/pi
curl https://raw.githubusercontent.com/mascalx/Aquarius/master/script/acquario.py -o acquario.py

cd /var/www
curl https://raw.githubusercontent.com/mascalx/Aquarius/master/web/index.php -o index.php
curl https://raw.githubusercontent.com/mascalx/Aquarius/master/web/update.php -o update.php
curl https://raw.githubusercontent.com/mascalx/Aquarius/master/web/style.css -o style.css
curl https://raw.githubusercontent.com/mascalx/Aquarius/master/web/upgrade.php -o upgrade.php

sudo reboot
