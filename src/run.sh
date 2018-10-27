DIR = `$( dirname "$0"  )`
echo `executable directory: $DIR`
nohup python3 $DIR/deamon.py > $DIR/main.log & echo $! > $DIR/pid.txt