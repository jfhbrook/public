Name: korbenware
Version: 0.2.0
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
%{_bindir}/kbbg
%{_bindir}/kbdesktop
%{_bindir}/kblock
%{_bindir}/kbmenu
%{_bindir}/kbnotify
%{_bindir}/kbopen
%{_bindir}/kbprev
%{_bindir}/kbscreenshot


%changelog
* Sun Dec 26 2021 Josh Holbrook <josh.holbrook@gmail.com> 0.2.0-1
- Build korbenware package using tito

* Sun Dec 26 2021 Josh Holbrook <josh.holbrook@gmail.com>
- new package built with tito


