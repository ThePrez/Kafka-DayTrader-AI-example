#!/QOpenSys/pkgs/bin/bash
PATH=/QOpenSys/pkgs/bin:/QOpenSys/usr/bin:$PATH
export PATH
export WLP_SKIP_UMASK=true
cd $(dirname $0)
echo "Using source directory $SRCDIR"
export JAVA_HOME="/QOpenSys/QIBM/ProdData/JavaVM/jdk80/64bit"
: ${INSTALLDIR="/QOpenSys/OCPDT_demo/"}
: ${INSTALLSCHEMA="OCPDT"}
INSTALLSCHEMA=$(echo $INSTALLSCHEMA | tr -cd '[:alnum:]' | tr '[:lower:]' '[:upper:]'| head -c 10)
LIBERTY_SERVER="dt7server"
USRPRF_PW=$(cat /dev/urandom | tr -cd '[A-Z0-9]' | head -c 10)
: ${INSTALLUSER="$INSTALLSCHEMA"}
#INSTALLUSER=$(echo $INSTALLUSER | tr -cd '[:alnum:]' | tr '[:lower:]' '[:upper:]')
INSTALLUSER=$INSTALLSCHEMA

set -e
echo "==============================================="
echo " Installing to directory $INSTALLDIR..."
echo " Installing to schema $INSTALLSCHEMA..."
echo " Creating user profile $INSTALLUSER...   "
echo "==============================================="
sleep 4
mkdir -p $INSTALLDIR
cd $INSTALLDIR

echo "==============================================="
echo " Installing requisite open source packages..."
echo "==============================================="
#OFFLINE_COPY_HERE
yum install ca-certificates-mozilla
yum install wget unzip gzip git tar-gnu openjdk-11 maven coreutils-gnu sed-gnu grep-gnu https://github.com/ThePrez/ServiceCommander-IBMi/releases/download/v0.3.4/sc-0.4.1-0.ibmi7.2.ppc64.rpm
hash -r 

echo "==============================================="
echo " Fetching AI Sample Code..."
echo "==============================================="
rm -rf Kafka-DayTrader-AI-example* example.zip
curl -L https://github.com/ThePrez/Kafka-DayTrader-AI-example/archive/refs/heads/main.zip -o example.zip
unzip example.zip
mv Kafka-DayTrader-AI-example-main Kafka-DayTrader-AI-example

echo "==============================================="
echo " Creating $INSTALLUSER user..."
echo "==============================================="
[ -e /qsys.lib/$INSTALLUSER.usrprf ] || system -i "crtusrprf USRPRF($INSTALLUSER) PASSWORD($USRPRF_PW)"
system -i "chgusrprf USRPRF($INSTALLUSER) PASSWORD($USRPRF_PW)"

echo "==============================================="
echo " Downloading Apache JMeter..."
echo "==============================================="
wget -c https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-3.0.tgz -O jmeter.tgz

echo "==============================================="
echo " Installing Apache JMeter..."
echo "==============================================="
[ -e jmeter ] || mkdir jmeter
tar xzf jmeter.tgz --strip-components 1 -C jmeter 
sed -i "s|-server||g" jmeter/bin/jmeter
cp Kafka-DayTrader-AI-example/jmeter/jmeter.properties jmeter/bin

echo "==============================================="
echo " Downloading Apache JMeter extensions..."
echo "==============================================="
wget -c https://github.com/kawasima/jmeter-websocket/archive/refs/heads/master.zip -O jmeter-websocket.zip

echo "==============================================="
echo " Building+installing Apache JMeter extensions..."
echo "==============================================="
wget -c https://github.com/kawasima/jmeter-websocket/archive/refs/heads/master.zip -O jmeter-websocket.zip
unzip -uoq jmeter-websocket.zip
pushd jmeter-websocket-master
mvn validate compile package 
popd
cp jmeter-websocket-master/target/ApacheJmeter_websocket-dist-0.1.0-SNAPSHOT.jar jmeter/lib/ext

echo "==============================================="
echo " Downloading Liberty..."
echo "==============================================="
wget -c https://public.dhe.ibm.com/ibmdl/export/pub/software/openliberty/runtime/release/2021-07-27_1323/openliberty-javaee8-21.0.0.8.zip -O openliberty.zip

echo "==============================================="
echo " Installing Liberty..."
echo "==============================================="
rm -fr wlp
unzip -uoq openliberty.zip

echo "==============================================="
echo " Building DayTrader..."
echo "==============================================="
[ -d dt7_build ] || mkdir -p dt7_build 
wget -c https://github.com/jdmcclur/sample.daytrader7/archive/refs/heads/stock-dataset.zip -O sample.daytrader7.zip
pushd dt7_build
[ -d sample.daytrader7 ] || unzip -uoq ../sample.daytrader7.zip
[ -d sample.daytrader7 ] || mv sample.daytrader7-stock-dataset sample.daytrader7
pushd sample.daytrader7
mvn package
cp daytrader-ee7/target/daytrader-ee7.ear $INSTALLDIR
cp jmeter_files/*.jmx $INSTALLDIR
popd
popd
cp Kafka-DayTrader-AI-example/jmeter/*.jmx .

echo "==============================================="
echo " Creating DayTrader Server..."
echo "==============================================="
rm -fr $INSTALLDIR/wlp/usr/servers/$LIBERTY_SERVER
wlp/bin/server create $LIBERTY_SERVER

echo "==============================================="
echo " Installing DayTrader application..."
echo "==============================================="
mkdir -p $INSTALLDIR/wlp/usr/shared/apps/
mv daytrader-ee7.ear $INSTALLDIR/wlp/usr/shared/apps/

echo "==============================================="
echo " Configuring DayTrader application..."
echo "==============================================="
cp Kafka-DayTrader-AI-example/daytrader/server.xml $INSTALLDIR/wlp/usr/servers/$LIBERTY_SERVER
sed -i "s|/home/OCPDT/|$INSTALLDIR/|gi" $INSTALLDIR/wlp/usr/servers/$LIBERTY_SERVER/server.xml
sed -i -E "s|libraries=\"[^\"]+\"|libraries=\"$INSTALLSCHEMA\"|gi" $INSTALLDIR/wlp/usr/servers/$LIBERTY_SERVER/server.xml
sed -i -E "s|user=\"[^\"]+\"|user=\"$INSTALLUSER\"|gi" $INSTALLDIR/wlp/usr/servers/$LIBERTY_SERVER/server.xml
sed -i -E "s|password=\"[^\"]+\"|password=\"$USRPRF_PW\"|gi" $INSTALLDIR/wlp/usr/servers/$LIBERTY_SERVER/server.xml
$INSTALLDIR/wlp/bin/featureUtility installServerFeatures $LIBERTY_SERVER

echo "==============================================="
echo " Installing Service Commander files..."
echo "==============================================="
mkdir -p $HOME/.sc/services
cp Kafka-DayTrader-AI-example/sc/*.y*ml $HOME/.sc/services
find $HOME/.sc/services -name \*.yaml -print -exec sed -i "s|/home/OCPDT/|$INSTALLDIR/|gi" {} \;

echo "==============================================="
echo " Initializing Daytrader database..."
echo "==============================================="
[ -e /qsys.lib/$INSTALLSCHEMA.lib ] || system "RUNSQL SQL('create schema $INSTALLSCHEMA') COMMIT(*NONE)"
system -i "CHGOWN OBJ('/qsys.lib/$INSTALLSCHEMA.lib') NEWOWN($INSTALLUSER) RVKOLDAUT(*NO) SUBTREE(*ALL)" || true

echo "==============================================="
echo " Starting Daytrader application..."
echo "==============================================="
sc restart daytrader

echo "==============================================="
echo " Setting up DayTrader database..."
echo "==============================================="
sleep 12
curl http://localhost:10200/daytrader/config?action=buildDBTables
curl http://localhost:10200/daytrader/config?action=buildDB

echo "==============================================="
echo " Stopping Daytrader aplication..."
echo "==============================================="
sc stop daytrader

echo "==============================================="
echo " Downloading Kafka and Zookeeper..."
echo "==============================================="
wget -c https://apache.osuosl.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz -O kafka.tgz

echo "==============================================="
echo " Installing Kafka and Zookeeper..."
echo "==============================================="
[ -e kafka ] || mkdir kafka
tar xzf kafka.tgz --strip-components 1 -C kafka

echo "==============================================="
echo " Creating DTAQ+trigger in $INSTALLSCHEMA..."
echo "==============================================="
[ -e /qsys.lib/$INSTALLSCHEMA.lib/AI.DTAQ ] || system "CRTDTAQ DTAQ($INSTALLSCHEMA/AI) MAXLEN(64512) SIZE(*MAX2GB)" || true
sed -i "s|OCPDT|$INSTALLSCHEMA|gi" Kafka-DayTrader-AI-example/trigger/create_trigger.sql
system "RUNSQLSTM SRCSTMF('Kafka-DayTrader-AI-example/trigger/create_trigger.sql')"


echo "==============================================="
echo " Building Camel application..."
echo "==============================================="
pushd Kafka-DayTrader-AI-example/camel
sed -i "s|OCPDT|$INSTALLSCHEMA|gi" src/main/resources/config.properties
mvn compile
popd

echo ''
echo 'DONE!!' 
echo '   Demo has been installed to:'
echo "      Schema '$INSTALLSCHEMA'"
echo "      Directory '$INSTALLDIR'"
echo ""
echo "   To start the demo, sign in as $(id -un) and run:"
echo '      /QOpenSys/pkgs/bin/sc start group:aikafka'
echo "   To stop the demo, sign in as $(id -un) and run:"
echo '      /QOpenSys/pkgs/bin/sc stop group:aikafka'
echo '   To stress test with Apache JMeter:'
echo "      $INSTALLDIR/jmeter/bin/jmeter -n -t $INSTALLDIR/daytrader7.jmx -JHOST=127.0.0.1 -JPORT=10200 -JTHREADS=10 -JDURATION=120 -l jmeter_log.txt"
echo ''
