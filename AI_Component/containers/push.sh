images=(
	"baseimage"
	"inference-server"
	"stream-processing"
	"socketio-server"
	"mqtt-realtime-chart"
)

for image in ${images[@]}; do
	echo -e "\n########## [PUSH] power10-mma-$image ##########\n"
	podman push "quay.io/mdeloche/power10-mma-$image"
done
