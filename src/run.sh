DIR = `$( dirname "$0"  )`
nohup python3 $DIR/deamon.py > $DIR/main.log & echo $! > $DIR/pid.txt