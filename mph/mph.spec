Name: mph
Version: 0.1.6
Release: 1%{?dist}
License: MPL-2.0
Summary: a cli tool for using emacs in daemon mode

URL: https://github.com/jfhbrook/public/tree/main/mph
Source0: %{name}-%{version}.tar.gz
BuildArch: x86_64

BuildRequires: rust-packaging >= 21 emacs
Requires: emacs

%description


%prep
%autosetup


%build
tar -xzf %{SOURCE0}
# NOTE: This pulls dependencies at runtime, which is Bad Form - but the
# realistic alternative is packaging this with cargo and rust2rpm
cargo build --release


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 target/release/mph %{buildroot}%{_bindir}


%check


%files
%{_bindir}/mph


%changelog
* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.6-1
- RPM spec is for an x86_64 package (josh.holbrook@gmail.com)

* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.5-1
- Fix for COPR build
* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.4-1
- new package built with tito

