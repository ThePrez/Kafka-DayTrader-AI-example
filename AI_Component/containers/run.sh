run_app () {
	app_name="$1"
	if [ "$app_name" == "rabbitmq" ]; then
		image_name="rabbitmq:3-management"
	else
		image_name="power10-mma-$app_name"
	fi
	shift
	
	echo -e "\n##### power10-mma-$app_name #####\n"
	podman run --network power10-mma-network -d --name "power10-mma-$app_name" $@ "$image_name"
}

run_app "rabbitmq"				-p "5672:5672"
run_app "inference-server"		-p "5000:5000"
run_app "stream-processing"		-e KAFKA_BROKER="kafka://9.40.204.181:9092"
run_app "socketio-server"		-p "9081:9081"
# run_app "mqtt-realtime-chart"	"TODO"
