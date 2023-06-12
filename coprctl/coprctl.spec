Name: coprctl
Version: 0.1.2
Release: 1%{?dist}
License: MIT
Summary: infrastructure-as-code for COPR

URL: https://github.com/jfhbrook/public/tree/main/coprctl
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: coreutils
Requires: copr-cli yq

%description
infrastructure-as-code for COPR, using copr-cli and yq


%prep
%autosetup


%build
tar -xzf %{SOURCE0}


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 bin/coprctl %{buildroot}%{_bindir}


%check


%files
%{_bindir}/coprctl


%changelog
* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.2-1
- new package built with tito

* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.1-1
- First version of coprctl (josh.holbrook@gmail.com)
