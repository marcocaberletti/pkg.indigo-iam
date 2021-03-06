%define name            iam-login-service
%define warversion      0.6.0
%define base_version    0.6.0
%define base_release    1

%define user            iam

%define jdk_version     1.8.0
%define mvn_version     3.3.0

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name:		%{name}
Version:	%{base_version}
Release:	%{release_version}%{?dist}
Summary:	INDIGO Identity and Access Management Service.

Group:		Applications/Web
License:	apache2
URL:		https://github.com/indigo-dc/iam

BuildArch: noarch
BuildRequires: java-%{jdk_version}-openjdk-devel
BuildRequires: maven >= %{mvn_version}

Requires:	java-%{jdk_version}-openjdk

%description
The INDIGO IAM (Identity and Access Management service) provides 
user identity and policy information to services so that consistent 
authorization decisions can be enforced across distributed services.

%prep

%build
sudo cp -r $HOME/sources/%{name} /
sudo chown -R $(id -un):$(id -un) /%{name}
cd /%{name}
mvn -U clean package

%install
cd ${RPM_BUILD_ROOT}
mkdir -p var/lib/indigo/%{name}
mkdir -p usr/lib/systemd/system
mkdir -p etc/sysconfig
cp /%{name}/%{name}/target/%{name}.war var/lib/indigo/%{name}
cp /%{name}/rpm/SOURCES/%{name}.service usr/lib/systemd/system
cp /%{name}/rpm/SOURCES/%{name} etc/sysconfig

%clean

%pre

%post
/usr/bin/id -u %{user} > /dev/null 2>&1
if [ $? -eq 1 ]; then
  useradd --comment "INDIGO IAM" --system --user-group --home-dir /var/lib/indigo/%{name} --no-create-home --shell /sbin/nologin %{user}
fi
chown -R %{user}:%{user} /var/lib/indigo/%{name}
systemctl daemon-reload

%preun
systemctl stop %{name}

%postun
systemctl daemon-reload

%files
%config(noreplace) /etc/sysconfig/iam-login-service
%dir /var/lib/indigo
%dir /var/lib/indigo/%{name}
/var/lib/indigo/%{name}/%{name}.war
/usr/lib/systemd/system/%{name}.service

%changelog
* Thu Apr 27 2017 Marco Caberletti <marco.caberletti@cnaf.infn.it> 0.6.0
- Initial IAM Login Service for Indigo 2.
