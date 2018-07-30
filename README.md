##Cron configuration

In file `/etc/crontab` add line:
`* * * * * root /home/pi/easyMine-resetter/scripts/launchResetter.sh`

Instalacja modułów:

GPIO
apt-get install python-rpi.gpio python3-rpi.gpio


apt-get install python3-pip
pip3 install RPi.GPIO
