images=(
	"baseimage"
	"inference-server"
	"stream-processing"
	"socketio-server"
	"mqtt-realtime-chart"
)

for image in ${images[@]}; do
	echo -e "\n########## [BUILD] power10-mma-$image ##########\n"
	podman build . -f "Dockerfile.power10-mma-$image" -t "quay.io/mdeloche/power10-mma-$image"
done
