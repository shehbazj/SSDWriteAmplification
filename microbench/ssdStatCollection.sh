# This script collects SSD statistics. We collect three primary statistics:

# SMART Counter 247 - NAND Program Operations Initiated by Host
# SMART Counter 248 - NAND Program Operations Initiated by FTL Layer
# we collect periodic statistics (per second).
# at the end we also map cumulative statistics. 

usage()
{
	echo "./ssdStatCollection.sh <start|stop> [time-interval] [device]"
	echo ""
	echo "start - start data collection"
	echo "stop - end data collection"
	echo "time-interval integer seconds - time between each SMART collection (default 5 seconds)"
	echo "device - host device - default /dev/sdc"
}

if [ "$#" -lt 1 ]; then
	usage
	exit
fi

startstop=$1
timeInterval=${2:-5}
device=${3:-'/dev/sdb'}

if [[ "$startstop" = "start" ]]; then
	echo "start collection script"
	if pidof -x "diskStat.sh" >/dev/null; then
		echo "Process already running"
		exit
	else
		./diskStat.sh $timeInterval $device
	fi
	
elif [[ "$startstop" = "stop" ]]; then
	echo "stop collection script"
	sudo kill -9 pidof -x "diskStat.sh"
else
	echo "unknown command"
fi
