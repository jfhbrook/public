Name: coprctl
Version: 1.0.0
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
* Wed Jun 04 2025 Josh Holbrook <josh.holbrook@gmail.com> 1.0.0-1
- Split COPR tools out of coprctl and into copr-tools (josh.holbrook@gmail.com)

- Mount entire homedir (josh.holbrook@gmail.com)
- tito-docker script (josh.holbrook@gmail.com)
- Build coprctl on fedora 41 (josh.holbrook@gmail.com)
- Publish coprctl to homebrew tap (josh.holbrook@gmail.com)

* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.2.2-1
- Forgot to pull packagename for pypi COPR builds (josh.holbrook@gmail.com)

* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.2.1-1
- logging improvements (josh.holbrook@gmail.com)

* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.2.0-1
- Bugfixes for `coprctl get package-pypi` (josh.holbrook@gmail.com
- Logs now print to stderr (josh.holbrook@gmail.com)

* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.6-1
- 

* Tue Jun 13 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.5-1
- coprctl now supports projects (josh.holbrook@gmail.com)

* Mon Jun 12 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.4-1
- Add package-custom support to coprctl (josh.holbrook@gmail.com)

* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.3-1
- Busted config

* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.2-1
- new package built with tito

* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.1.1-1
- First version of coprctl (josh.holbrook@gmail.com)
