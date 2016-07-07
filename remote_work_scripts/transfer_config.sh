# Prefix path for the remote machine
REMOTE_BASE=/home/sandc3
#REMOTE_BASE=/tmp/test
IP=$(cat ~/bin/sandc3-u12-ip)

wd=$(pwd)
if [[ "work" != ${wd:$((${#wd} - 4))} ]]; then
    echo "Please move into the work directory first."
    exit 1
fi

if [[ "/" == ${TARGET:$((${#TARGET} - 1))} ]]; then
    TARGET=${TARGET:0:$((${#TARGET} - 1))}
fi
