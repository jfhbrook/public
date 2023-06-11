Name: yq
Version: 4.34.1
Release: 1%{?dist}
License: MIT
Summary: a portable command-line YAML, JSON, XML, CSV, TOML and properties processor

URL: https://github.com/mikefarah/yq/releases/download/v${version}/
Source0: %{name}_linux_amd64.tar.gz
BuildArch: x86_64

%description
yq is a portable command-line YAML, JSON, XML, CSV, TOML and properties processor


%prep
%autosetup


%build
tar -xzf %{SOURCE0}


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 bin/yq_linux_amd64 %{buildroot}${_bindir}/yq
mkdir -p %{_mandir}/man1/
cp yq.1 %{_mandir}/man1/

%check


%files
%{_bindir}/yq
%{_mandir}/man1/yq.1
