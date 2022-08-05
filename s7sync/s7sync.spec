Name: s7sync
Version: 0.1.0
Release: 1%{?dist}
License: MPL-2.0
Summary: sie7e labs filesync professional edition

URL: https://github.com/jfhbrook/public/tree/main/s7sync
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: coreutils
Requires: bash coreutils

%description


%prep
%autosetup


%build
tar -xzf %{SOURCE0}


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 bin/s7sync %{buildroot}%{_bindir}


%check


%files
%{_bindir}/s7sync


%changelog
