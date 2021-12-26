%global forgeurl https://github.com/jfhbrook/public
%global commit a7368bdfc415e737c79dd4a855700a356da1423f

%forgemeta

Name: korbenware
Version: 
Release: 1%{?dist}
Summary: linux/unix desktop cli software

License: MPL-2.0
URL: %{forgeurl}
Source: %{forgesource}

BuildRequires:
Requires:

%description


%prep
%forgesetup


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

