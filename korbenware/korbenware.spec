Name: korbenware
Version: 0.2.0
Release: 0%{?dist}
License: MPL-2.0
Summary: linux/unix desktop cli software

URL: https://github.com/jfhbrook/public/tree/main/korbenware
Source: %{name}-%{version}.tar.gz
BuildArch: noarch

%description


%prep


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -p pm 755 %{SOURCE0}/bin/* %{buildroot}%{_bindir}


%check


%files
%{_bindir}/kbbg
%{_bindir}/kbbright
%{_bindir}/kbdesktop
%{_bindir}/kblock
%{_bindir}/kbmenu
%{_bindir}/kbnotify
%{_bindir}/kbopen
%{_bindir}/kbprev
${_bindir}/kbscreenshot


%changelog

