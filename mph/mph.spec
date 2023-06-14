Name: mph
Version: 0.1.3
Release: 1%{?dist}
License: MPL-2.0
Summary: a cli tool for using emacs in daemon mode

URL: https://github.com/jfhbrook/public/tree/main/mph
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: rust-packaging >= 21 emacs
Requires: emacs

%description


%prep
%autosetup


%build
tar -xzf %{SOURCE0}
cargo build --release
install -p -m 755 target/release/mph %{buildroot}%{_bindir}


%install
mkdir -p %{buildroot}%{_bindir}


%check


%files
%{_bindir}/mph


%changelog
