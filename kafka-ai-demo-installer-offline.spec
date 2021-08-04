%undefine _disable_source_fetch
Name: kafka-ai-demo-installer-offline
Version: 0.0.1
Release: 0
License: Apache-2.0
Summary: Installer for the Kafka AI Demo
Url: https://github.com/ThePrez/Kafka-DayTrader-AI-example

BuildRequires: kafka-ai-demo-installer
Requires: kafka-ai-demo-installer

Source0: install-offline.sh

%description
Offline installation for the Kafka AI Demo at
https://github.com/ThePrez/Kafka-DayTrader-AI-example
Script will download, build, and install all necessary components,
including OpenLiberty, Zookeeper, Kafka, Camel, and DayTrader. It will
also create a database schema, database tables, a user profile, and
service definitions for Service Commander.

%prep

%build
mkdir -p %{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo/

%install
INSTALLDIR=%{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo/ /QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/install.sh 
rm -fr %{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo/jmeter-websocket-master 
rm -fr %{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo/dt7_build
rm -fr %{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo/*.tgz
rm -fr %{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo/*.zip

%files
%defattr(-, qsys, *none)
%exclude /QOpenSys/QIBM/UserData/Kafka-AI-Demo/wlp/usr/servers/dt7server/server.xml
/QOpenSys/QIBM/UserData/Kafka-AI-Demo/
%config(noreplace) /QOpenSys/QIBM/UserData/Kafka-AI-Demo/wlp/usr/servers/dt7server/server.xml


%changelog
* Wed Aug 18 2021 Jesse Gorzinski <jgorzins@us.ibm.com> - 0.0.1
- initial RPM release
