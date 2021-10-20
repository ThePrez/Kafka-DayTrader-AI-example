# AI-Usecases

## Environment setup

* install conda

```
wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-ppc64le.sh
sh Anaconda3-2021.05-Linux-ppc64le.sh # accept license and leave default values
source ~/.bashrc
```

* clone that Git repository (requires a token from your IBM Github account

```
git clone https://github.ibm.com/P10-IBMi-AI-Proof-Point/AI-Usecases/
cd AI-Usecases/
```

* restore "opence" conda environment

```
conda env create -f opence-conda-env.yml
conda activate opence
```

[BACKUP] With ausgsa channel:

```
conda create -n opence python=3.8
conda install flask numpy pandas scipy scikit-learn statsmodels kombu eventlet nodejs
pip install pytorch_forecasting faust python-socketio==4.0.0 python-engineio==3.2.0
```

## How To

1. Launch RabbitMQ (`docker login docker.io` might be required)

```
podman run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

2. Download trained model checkpoint 
from ["IBM i P10 AI Proof Point" Box folder](https://ibm.ent.box.com/folder/141751006062)
and place the `n-beats.ckpt` file in the `src/inference-server/` folder

3. Run inference server

```
# inference_server.py requires training/utils.py, add it to PYTHONPATH
export PYTHONPATH=/root/AI-Usecases/src/training:
cd src/inference-server/ && python3 inference_server.py
```

4. Run streaming service (update the `KAFKA_BROKER` variable to point to the URL and port of Kafka)

```
cd src/stream-processing/
KAFKA_BROKER="kafka://10.20.30.40:9092" python3 streaming_app.py worker -l info
```

5. Run SocketIO server

```
cd src/visualization/ && python3 ./socketio-server/server.py
```

6. Run Vue web server

```
git clone https://github.com/MaximeDeloche/mqtt-realtime-chart-client && cd mqtt-realtime-chart-client/
npm install && npm start
```

Note: the visualization range can be changed manually in the `visualization/mqtt-realtime-chart-client/src/components/Home.vue` file (`min` and `max` values lines 77 and 78). 

6. Connect to `http://server-ip:9080`

Note: you might need to:

* disable SELinux: `sudo setenforce 0`
* open ports 9080 (web server) and 9081 (websocket connection): `firewall-cmd --add-port=9080/tcp` and `firewall-cmd --add-port=9081/tcp`

7. Launch JMeter. Connect to the IBMi system and run:

```
/QOpenSys/ocp5/jmeter/bin/jmeter -n -t /QOpenSys/ocp5/daytrader7.jmx -JHOST=127.0.0.1 -JPORT=10200 -JTHREADS=10 -JDURATION=120 -l jmeter_log.txt
```

## Sources

* [Nick Jokic - Real-time visualization of high-frequency streams](https://itnext.io/javascript-real-time-visualization-of-high-frequency-streams-d6533c774794#ad5d)
