Name:		nagios-plugins-eudat-b2stage
Version:	0.5
Release:	1%{?dist}
Summary:	Nagios probe for B2STAGE
License:	GPLv3+
Packager:	Themis Zamani <themiszamani@gmail.com>

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}
AutoReqProv: no

%description
Nagios probe to check functionality of B2STAGE service

%prep
%setup -q

%define _unpackaged_files_terminate_build 0 

%install

install -d %{buildroot}/%{_libexecdir}/argo-monitoring/probes/eudat-b2stage
install -d %{buildroot}/%{_sysconfdir}/nagios/plugins/eudat-b2stage
install -m 755 check_b2stage_http-api.py %{buildroot}/%{_libexecdir}/argo-monitoring/probes/eudat-b2stage/check_b2stage_http-api.py

%files
%dir /%{_libexecdir}/argo-monitoring
%dir /%{_libexecdir}/argo-monitoring/probes/
%dir /%{_libexecdir}/argo-monitoring/probes/eudat-b2stage

%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes//eudat-b2stage/check_b2stage_http-api.py

%changelog
* Fri Oct 19 2018 Themis Zamani  <themiszamani@gmail.com> - 0.1-1
- Initial version of the package. 
* Thu Oct 18 2018 Mattia D'Antonio  <m.dantonio@cineca.it> - 0.1-1
- Initial version of the package. 
