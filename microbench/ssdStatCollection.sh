# This script collects SSD statistics. We collect three primary statistics:

# SMART Counter 246 - Number of Writes made by Host (Total_Host_Sector_Write) = Host_Program_Page_Count * 16
# SMART Counter 247 - NAND Program Operations Initiated by Host (Host_Program_Page_Count)
# SMART Counter 248 - NAND Program Operations Initiated by FTL Layer (Bckgnd_Program_Page_Cnt)

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
device=${3:-'/dev/sdd'}

if [[ "$startstop" = "start" ]]; then
	echo "start collection script"
	if pidof -x "diskStat.sh" >/dev/null; then
		echo "Process already running"
		exit
	else
		sudo ./diskStat.sh $timeInterval $device
	fi
	
elif [[ "$startstop" = "stop" ]]; then
	echo "stop collection script"
	sudo kill -9 pidof -x "diskStat.sh"
else
	echo "unknown command"
fi
