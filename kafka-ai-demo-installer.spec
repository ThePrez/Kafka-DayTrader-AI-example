%undefine _disable_source_fetch
Name: kafka-ai-demo-installer
Version: 0.0.2
Release: 0
License: Apache-2.0
Summary: Installer for the Kafka AI Demo
Url: https://github.com/ThePrez/Kafka-DayTrader-AI-example


Requires: ca-certificates-mozilla
Requires: wget unzip gzip service-commander tar-gnu openjdk-11 maven coreutils-gnu sed-gnu grep-gnu

Source0: install.sh

%description
Installer for the Kafka AI Demo at https://github.com/ThePrez/Kafka-DayTrader-AI-example
Script will download, build, and install all necessary components,
including OpenLiberty, Zookeeper, Kafka, Camel, and DayTrader. It will
also create a database schema, database tables, a user profile, and
service definitions for Service Commander.

%prep

%build
mkdir -p %{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/


%install
cp %{SOURCE0} %{buildroot}/QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/

%files
%defattr(-, qsys, *none)
/QOpenSys/QIBM/UserData/Kafka-AI-Demo-installer/install.sh


%changelog
* Fri Oct 29 2021 Jesse Gorzinski <jgorzins@us.ibm.com> - 0.0.2
- Add dependency on 'service-commander'
- remove dependency on git
* Wed Aug 18 2021 Jesse Gorzinski <jgorzins@us.ibm.com> - 0.0.1
- initial RPM release
