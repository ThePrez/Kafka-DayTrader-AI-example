# Kafka-based AI example using DayTrader

For more information on this project, see complementary article at `<<INSERT LINK HERE>>`

# Components of this demo project

The installation of this demo project installs all of the following on IBM i:
- [DayTrader](https://github.com/jdmcclur/sample.daytrader7), a sample application that simulates a stock exchange
- [Apache JMeter](https://jmeter.apache.org/), which can be used to stress-test the application by executing a large amount of stock trades
- [Websocket extensions](https://github.com/kawasima/jmeter-websocket/) for JMeter, needed for use with DayTrader
- [OpenLiberty](http://openliberty.io), a server runtime (used to run DayTrader)
- [Service Commander](https://theprez.github.io/ServiceCommander-IBMi/#service-commander-for-ibm-i), a utility to help manage which jobs are running
- [Apache Kafka](https://kafka.apache.org), message-oriented middleware that delivers a distributed streaming platform
- [Apache Zookeeper](https://zookeeper.apache.org/), a service for powering distributed applications (used by Kafka)
- [Apache Camel](https://camel.apache.org), an integration library (used for integrating Db2 transactions with Kafka)

This project also requires an IBM i user profile and schema to be created of the same name, which the installation script will create. These are used by the DayTrader application. 


# IBM i component Installation

- Installation requires that you have the `yum` ecosystem installed (see [http://ibm.biz/ibmi-rpms](http://ibm.biz/ibmi-rpms))
- You should run any documented commands in an SSH terminal session

## Standard install (with Internet access)

First, install the `kafka-ai-demo-installer` RPM, which will ensure that any requisites are installed (Service Commander will need to be installed separately, as shown below)

```
yum install https://github.com/ThePrez/Kafka-DayTrader-AI-example/releases/download/v0.0.2/kafka-ai-demo-installer-0.0.2-0.ibmi7.2.ppc64.rpm
```

That RPM will place the installer script at `/QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/install.sh`

There are several items you can customize about your installation through the use of the following environment variables:
- `INSTALLDIR`: The installation directory (default: `/QOpenSys/OCPDT_demo`)
- `INSTALLSCHEMA`: The schema to create for use by DayTrader. A user profile of the same name will be created. **DO NOT USE a name for which an existing user profile exists!!** (default: `OCPDT`)

For example, to install to `/QOpenSys/ocp2`, use schema `OCP2`, and create user profile `OCP2`, run the following command:
`INSTALLDIR=/QOpenSys/ocp2 INSTALLSCHEMA=OCP2 /QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/install.sh`

When the install completes, it should provide you with output similar to the following, providing instructions on how to start/stop the demo and run Apache JMeter for stress testing :
```
DONE!!
   Demo has been installed to:
      Schema 'OCP2'
      Directory '/QOpenSys/ocp2'

   To start the demo, sign in as JGORZINS and run:
      /QOpenSys/pkgs/bin/sc start group:aikafka
   To stop the demo, sign in as JGORZINS and run:
      /QOpenSys/pkgs/bin/sc stop group:aikafka
   To stress test with Apache JMeter:
      /QOpenSys/ocp2/jmeter/bin/jmeter -n -t /QOpenSys/ocp2/daytrader7.jmx -JHOST=127.0.0.1 -JPORT=10200 -JTHREADS=10 -JDURATION=120 -l jmeter_log.txt
```



## Offline install (without Internet access) -- WARNING: untested and unlikely to work!

First, download the following files and upload them to a directory on IBM i:
- https://github.com/ThePrez/Kafka-DayTrader-AI-example/releases/download/v0.0.1/kafka-ai-demo-installer-offline-0.0.2-0.ibmi7.2.ppc64.rpm

Then, `cd` to the directory where you have placed these RPMs and run the following commands to install them (you may need to also install other requisite RPMs):
```
yum install ./sc-0.4.1-0.ibmi7.2.ppc64.rpm
yum install ./kafka-ai-demo-installer-offline-0.0.1-0.ibmi7.2.ppc64.rpm
```

These RPMs will place the offline installer script at `/QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/install-offline.sh`

There are several items you can customize about your installation through the use of the following environment variables:
- `INSTALLDIR`: The installation directory
- `INSTALLSCHEMA`: The schema to create for use by DayTrader
- `INSTALLUSER`: The user profile to create for use by DayTrader

For example, to install to `/QOpenSys/ocp2`, use schema `OCP2`, and create user profile `JESSE`, run the following command:
`INSTALLDIR=/QOpenSys/ocp2 INSTALLSCHEMA=OCP2 INSTALLUSER=JESSE /QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/install-offline.sh`

When the install completes, it should provide you with output similar to the following, providing instructions on how to start/stop the demo and run Apache JMeter for stress testing :
```
DONE!!
   Demo has been installed to:
      Schema 'OCP2'
      Directory '/QOpenSys/ocp2'

   To start the demo, sign in as JGORZINS and run:
      /QOpenSys/pkgs/bin/sc start group:aikafka
   To stop the demo, sign in as JGORZINS and run:
      /QOpenSys/pkgs/bin/sc stop group:aikafka
   To stress test with Apache JMeter:
      /QOpenSys/ocp2/jmeter/bin/jmeter -n -t /QOpenSys/ocp2/daytrader7.jmx -JHOST=127.0.0.1 -JPORT=10200 -JTHREADS=10 -JDURATION=120 -l jmeter_log.txt
```

# AI Component installation
See [the README for the AI component](AI_Component/README.md)
