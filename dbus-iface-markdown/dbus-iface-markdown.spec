Name: dbus-iface-markdown
Version: 1.0.2
Release: 1
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
* Mon Sep 15 2025 Josh Holbrook <josh.holbrook@gmail.com> 1.0.2-1
- Slightly more robust error handling (josh.holbrook@gmail.com)

* Mon Sep 15 2025 Josh Holbrook <josh.holbrook@gmail.com>
- Slightly more robust error handling (josh.holbrook@gmail.com)

* Wed Feb 19 2025 Josh Holbrook <josh.holbrook@gmail.com> 1.0.1-1
- More idiomatic perl
* Wed Feb 19 2025 Josh Holbrook <josh.holbrook@gmail.com> 1.0.0-1
- new package built with tito

