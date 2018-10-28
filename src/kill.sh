DIR="$( cd "$( dirname "$0"  )" && pwd  )"
kill -9 `cat $DIR/pid.txt`
pkill -9 chrome