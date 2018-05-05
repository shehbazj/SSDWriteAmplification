# Collect SMART Values 247 and 248

usage()
{
	echo "./diskStat.sh <time_interval> <device>"	
	echo "Output: Number of Host Writes(Only), Number of FTL Writes(Only)"
}

if [ "$#" -lt 2 ]; then
	usage
	exit
fi

time=$1
dev=$2

prev247=0
prev248=0

while true;
do
	smart247=`sudo smartctl -a $dev | grep "Host_Program_Page_Count" | rev | cut -d" " -f1 | rev`
	smart248=`sudo smartctl -a $dev | grep "Bckgnd_Program_Page_Cnt" | rev | cut -d" " -f1 | rev`
	delta247=$(($smart247 - $prev247))
	delta248=$(($smart248 - $prev248))
	if [ "$delta247" = "$smart247" ]; then
		echo "0 0"
	else
		echo "$delta247 $delta248"
	fi
	prev247=$smart247
	prev248=$smart248
sleep $time
done
