Name: yq
Version: 4.34.1
Release: 1%{?dist}
License: MIT
Summary: a portable command-line YAML, JSON, XML, CSV, TOML and properties processor

URL: https://github.com/mikefarah/yq
Source0: %{name}-%{version}.tar.gz
BuildArch: x86_64

BuildRequires: curl

%description
yq is a portable command-line YAML, JSON, XML, CSV, TOML and properties processor


%prep
%autosetup


%build
curl -L https://github.com/mikefarah/yq/releases/download/v%{version}/yq_linux_amd64.tar.gz -o release.tar.gz
tar -xzf release.tar.gz


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 yq_linux_amd64 %{buildroot}%{_bindir}/yq

%check


%files
%{_bindir}/yq

%changelog
* Sat Jun 10 2023 Josh Holbrook <josh.holbrook@gmail.com> 4.34.3-1
- Add %changelog section to yq spec (josh.holbrook@gmail.com)
