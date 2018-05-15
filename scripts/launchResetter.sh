 #!/bin/bash

c=`ps aux | grep -i main.py | grep -v grep | wc -l`
s=`dirname ${0}`

if [ ${c} -eq 0 ]
then
  cd ${s}/..
  git pull
  python3 main.py 2>&1 > /var/logs/resetter.log
fi
