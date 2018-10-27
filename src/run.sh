cd `$( dirname "$0"  )`
nohup python3 deamon.py > main.log & echo $! > pid.txt