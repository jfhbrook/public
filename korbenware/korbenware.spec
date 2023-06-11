Name: korbenware
Version: 0.5.0
Release: 1%{?dist}
License: MPL-2.0
Summary: linux/unix desktop cli software

URL: https://github.com/jfhbrook/public/tree/main/korbenware
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: coreutils
Requires: bash coreutils cowsay fortune-mod fzf libnotify python3 python3-pyxdg sway wl-clipboard

%description


%prep
%autosetup


%build
tar -xzf %{SOURCE0}


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 bin/kbconfig %{buildroot}%{_bindir}
install -p -m 755 bin/kbbg %{buildroot}%{_bindir}
install -p -m 755 bin/kbdesktop %{buildroot}%{_bindir}
install -p -m 755 bin/kblock %{buildroot}%{_bindir}
install -p -m 755 bin/kbmenu %{buildroot}%{_bindir}
install -p -m 755 bin/kbnotify %{buildroot}%{_bindir}
install -p -m 755 bin/kbopen %{buildroot}%{_bindir}
install -p -m 755 bin/kbprev %{buildroot}%{_bindir}
install -p -m 755 bin/kbscreenshot %{buildroot}%{_bindir}


%check


%files
%{_bindir}/kbconfig
%{_bindir}/kbbg
%{_bindir}/kbdesktop
%{_bindir}/kblock
%{_bindir}/kbmenu
%{_bindir}/kbnotify
%{_bindir}/kbopen
%{_bindir}/kbprev
%{_bindir}/kbscreenshot


%changelog
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


