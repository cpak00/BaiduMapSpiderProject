DIR="$( cd "$( dirname "$0"  )" && pwd  )"
echo $DIR
nohup python3 $DIR/deamon.py > $DIR/main.log & echo $! > $DIR/pid.txt