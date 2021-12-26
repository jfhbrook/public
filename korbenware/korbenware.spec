Name: korbenware
Version: 0.2.0
Release: 0%{?dist}
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


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbbg %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbbright %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbdesktop %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kblock %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbmenu %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbnotify %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbopen %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbprev %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0}/bin/kbscreenshot %{buildroot}%{_bindir}


%check


%files
%{_bindir}/kbbg
%{_bindir}/kbbright
%{_bindir}/kbdesktop
%{_bindir}/kblock
%{_bindir}/kbmenu
%{_bindir}/kbnotify
%{_bindir}/kbopen
%{_bindir}/kbprev
${_bindir}/kbscreenshot


%changelog

