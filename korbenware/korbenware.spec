Name: korbenware
Version: 1.0.2
Release: 1%{?dist}
License: MPL-2.0
Summary: linux/unix desktop cli software

URL: https://github.com/jfhbrook/public/tree/main/korbenware
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: coreutils
Requires: bash coreutils fzf python3 python3-pyxdg sway viu

%description


%prep
%autosetup


%build
tar -xzf %{SOURCE0}


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 bin/kbbg %{buildroot}%{_bindir}
install -p -m 755 bin/kbconfig %{buildroot}%{_bindir}
install -p -m 755 bin/kbmenu %{buildroot}%{_bindir}
install -p -m 755 bin/kbopen %{buildroot}%{_bindir}
install -p -m 755 bin/kbprev %{buildroot}%{_bindir}


%check


%files
%{_bindir}/kbconfig
%{_bindir}/kbbg
%{_bindir}/kbmenu
%{_bindir}/kbopen
%{_bindir}/kbprev


%changelog
* Sun Mar 23 2025 Josh Holbrook <josh.holbrook@gmail.com> 1.0.2-1
- Released wrong branch in 1.0.1
* Sun Mar 23 2025 Josh Holbrook <josh.holbrook@gmail.com> 1.0.1-1
- Overhauled korbenware publish flow
- README updates
- kbopen has more robust handling of command construction
- shellcheck passes on kbopen
* Sat May 04 2024 Josh Holbrook <josh.holbrook@gmail.com> 1.0.0-1
- kbbg, kbmenu and kbopen support MacOS (josh.holbrook@gmail.com)
- kbconfig has extended options to support MacOS (josh.holbrook@gmail.com)
- Release automatically posted to GitHub (josh.holbrook@gmail.com)
- Homebrew package updated automatically (josh.holbrook@gmail.com)
- Homebrew package includes dependencies (josh.holbrook@gmail.com)
- kbconfig formatted with black (josh.holbrook@gmail.com)
* Fri May 03 2024 Josh Holbrook <josh.holbrook@gmail.com> 0.7.1-1
- kbconfig get handles missing section (josh.holbrook@gmail.com)

* Fri May 03 2024 Josh Holbrook <josh.holbrook@gmail.com> 0.7.0-1
- Updated kbconfig defaults
- Addition of kbconfig init (josh.holbrook@gmail.com)
- kbbg reads background paths from kbconfig (josh.holbrook@gmail.com)
- kbmenu reads python_path from kbconfig (josh.holbrook@gmail.com)
- fzf preview in kbmenu and kbprev better handles spaces in filenames
  (josh.holbrook@gmail.com)
- logging slightly quieter (josh.holbrook@gmail.com)

* Fri May 03 2024 Josh Holbrook <josh.holbrook@gmail.com> 0.6.2-1
- Remove bins from files in korbenware spec (josh.holbrook@gmail.com)

* Fri May 03 2024 Josh Holbrook <josh.holbrook@gmail.com> 0.6.1-1
- korbenware requires viu (josh.holbrook@gmail.com)
- Remove scripts not needed by Fedora Sway Spin (josh.holbrook@gmail.com)

* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.5.1-1
- new package built with tito

* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com>
- new package built with tito

* Sun Jun 11 2023 Josh Holbrook <josh.holbrook@gmail.com>
- new package built with tito

* Sat Jun 10 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.5.0-1
- add semantic ui color properties in kblock (initial support)
  (josh.holbrook@gmail.com)

* Fri Jun 09 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.4.3-1
- just publish task (josh.holbrook@gmail.com)

* Fri Jun 09 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.4.2-1
- That version was wrong! (josh.holbrook@gmail.com)

* Fri Jun 09 2023 Josh Holbrook <josh.holbrook@gmail.com>
- Bump korbenware version to v0.4.0 (josh.holbrook@gmail.com)

* Fri Jun 09 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.3.2-1
- Repo no longer has submodules

* Fri Jun 09 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.3.1-1
- Use INI config file for kblock (josh.holbrook@gmail.com)
- Fix errant characters in kbmenu logging (josh.holbrook@gmail.com)

* Tue Dec 28 2021 Josh Holbrook <josh.holbrook@gmail.com> 0.3.0-1
- Remove kbbright (use brightnessctl) (josh.holbrook@gmail.com)
- Fix DOA bugs in kbnotify and kbscreenshot (josh.holbrook@gmail.com)
* Sun Dec 26 2021 Josh Holbrook <josh.holbrook@gmail.com> 0.2.0-1
- Build korbenware package using tito

* Sun Dec 26 2021 Josh Holbrook <josh.holbrook@gmail.com>
- new package built with tito


