Name: dbus-iface-markdown
Version: 1.0.0
Release: 1%{?dist}
License: MIT
Summary: Generate markdown documentation from a live Dbus interface

URL: https://github.com/jfhbrook/public/tree/main/dbus-iface-markdown
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Requires: perl
Requires: dbus-tools

%description
Generate markdown documentation from a live Dbus interface


%prep
%autosetup


%build
tar -xzf %{SOURCE0}


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 bin/dbus-iface-markdown %{buildroot}%{_bindir}


%check


%files
%{_bindir}/dbus-iface-markdown


%changelog
