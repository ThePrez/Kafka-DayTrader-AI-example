images=(
	"baseimage"
	"inference-server"
	"stream-processing"
)

for image in ${images[@]}; do
	echo -e "\n########## power10-mma-$image ##########\n"
	podman build . -f "Dockerfile.power10-mma-$image" -t "power10-mma-$image"
done
