Name: yq
Version: 4.34.1
Release: 1%{?dist}
License: MIT
Summary: a portable command-line YAML, JSON, XML, CSV, TOML and properties processor

URL: https://github.com/mikefarah/yq
Source0: ./yq_linux_amd64.tar.gz
BuildArch: x86_64

%description
yq is a portable command-line YAML, JSON, XML, CSV, TOML and properties processor

%global debug_package %{nil}

%prep
%autosetup


%build
tar -xzf %{source0}


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 yq_linux_amd64 %{buildroot}%{_bindir}/yq
# mkdir -p %{buildroot}%{_mandir}/man1/
# install -p -m 644 yq.1 %{buildroot}%{_mandir}/man1/yq.1

%check


%files
%{_bindir}/yq
# %{_mandir}/man1/yq.1

%changelog
* Sat Jun 10 2023 Josh Holbrook <josh.holbrook@gmail.com> 4.34.1-1
- new package built with tito

