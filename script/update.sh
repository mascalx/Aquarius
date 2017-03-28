#!/bin/bash

cd /home/pi
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/script/acquario.py

cd /var/www
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/index.php
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/data.php
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/update.php
wget https://raw.githubusercontent.com/mascalx/Aquarius/master/web/style.css

sudo reboot
