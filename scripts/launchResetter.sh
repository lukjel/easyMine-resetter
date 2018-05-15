 #!/bin/bash

c=`ps aux | grep -i main.py | grep -v grep | wc -l`
s=`dirname ${0}`

if [ ${c} -eq 0 ]
then
  cd ${s}/..
  git pull
  echo 'Init!' > /var/log/resetter.log
  python3 main.py > /var/log/resetter.log
fi
