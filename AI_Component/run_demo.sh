if [ -z "$KAFKA_BROKER" ]; then
	echo -e  "Variable 'KAFKA_BROKER' needs to be set to the URL\n of the Kafka broker providing DayTrader data:\n kafka://ip-address:port"
	exit 1
fi

run_app () {
	app_name="$1"
	if [ "$app_name" == "rabbitmq" ]; then
		image_name="rabbitmq:3-management"
	else
		image_name="power10-mma-$app_name"
	fi
	shift
	
	echo -e "\n##### power10-mma-$app_name #####\n"
	podman run --network host -d --name "power10-mma-$app_name" $@ "quay.io/mdeloche/$image_name"
}

run_app "rabbitmq"
run_app "inference-server"
run_app "stream-processing"	-e KAFKA_BROKER="$KAFKA_BROKER"
run_app "socketio-server"
run_app "mqtt-realtime-chart"
