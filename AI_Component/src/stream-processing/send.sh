while [ 1 ]; do 
	rand=$(tr -dc 1-9 < /dev/urandom | head -c3).$(tr -dc 1-9 < /dev/urandom | head -c2)
	faust -A streaming_app send daytrader "{\"row\": {\"price\": $rand, \"content\": \"test\"}}" > /dev/null &
	echo "$rand"
	sleep 0.3
done
