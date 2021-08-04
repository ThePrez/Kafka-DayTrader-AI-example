#!/QOpenSys/pkgs/bin/bash
PATH=/QOpenSys/pkgs/bin:$PATH
export PATH
export WLP_SKIP_UMASK=true
cd $(dirname $0)
SRCDIR="$(pwd)"
INSTALLDIR=/QOpenSys/QIBM/UserData/Kafka-AI-Demo
INSTALLSCHEMA="OCPDT"
LIBERTY_SERVER="dt7server"

set -e
echo "==============================================="
echo " Installing to schema $INSTALLSCHEMA..."
echo "==============================================="

echo "==============================================="
echo " Installing Service Commander files..."
echo "==============================================="
# install sc files for this project
mkdir -p $HOME/.sc/services
cp $SRCDIR/Kafka-DayTrader-AI-example/sc/*.y*ml $HOME/.sc/services
find $HOME/.sc/services -name \*.yaml -print -exec sed -i "s|/home/OCPDT/|$INSTALLDIR/|gi" {} \;


echo "==============================================="
echo " Starting Daytrader aplication..."
echo "==============================================="
sc start daytrader

echo "==============================================="
echo " Setting up DayTrader database..."
echo "==============================================="
sleep 12
[ -e /qsys.lib/$INSTALLSCHEMA.lib ] || system "RUNSQL SQL('create schema $INSTALLSCHEMA') COMMIT(*NONE)"
curl http://localhost:10200/daytrader/config?action=buildDB
curl http://localhost:10200/daytrader/config?action=buildDBTables

echo "==============================================="
echo " Stopping Daytrader aplication..."
echo "==============================================="
sc stop daytrader

echo "==============================================="
echo " Creating DTAQ+trigger in $INSTALLSCHEMA..."
echo "==============================================="
[ -e /qsys.lib/$INSTALLSCHEMA.lib/AI.DTAQ ] || system "CRTDTAQ DTAQ($INSTALLSCHEMA/AI) MAXLEN(64512)" || true
sed -i "s|OCPDT|$INSTALLSCHEMA|gi" Kafka-DayTrader-AI-example/trigger/create_trigger.sql
system "RUNSQLSTM SRCSTMF('$SRCDIR/Kafka-DayTrader-AI-example/trigger/create_trigger.sql')"

echo ''
echo 'DONE!!' 
echo '   Demo has been installed to:'
echo "      Schema '$INSTALLSCHEMA'"
echo "      Directory '$INSTALLDIR'"
echo ""
echo '   To start the demo, run:'
echo '      /QOpenSys/pkgs/bin/sc start group:aikafka'
echo '   To stop the demo, run:'
echo '      /QOpenSys/pkgs/bin/sc stop group:aikafka'
echo '   To stress test with Apache JMeter:'
echo "      $INSTALLDIR/jmeter/bin/jmeter -n -t $INSTALLDIR/daytrader7.jmx -JHOST=127.0.0.1 -JPORT=10200 -JTHREADS=10 -JDURATION=120 -l jmeter_log.txt"
echo ''
