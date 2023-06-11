Name: fortune-jfhbrook
Version: 0.0.3
Release: 1%{?dist}
License: UNLICENSED
Summary: Josh Holbrook's collection of fortunes for fortune-mod

URL: https://github.com/jfhbrook/public/tree/main/fortune-mod
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: coreutils fortune-mod
Requires: fortune-mod

%description
Josh Holbrook's collection of fortunes for fortune-mod

%prep
%autosetup

# see: https://src.fedoraproject.org/rpms/fortune-mod/blob/rawhide/f/fortune-mod.spec
%global CookieDir %{_datadir}/games/fortune


%build
ls ./fortunes/ | xargs -I '$file' strfile './fortunes/$path'

%install
mkdir -p %{buildroot}%{CookieDir}
cp -r ./fortunes/* %{buildroot}%{CookieDir}

%check


%files
%{CookieDir}/clock-app
%{CookieDir}/clock-app.dat
%{CookieDir}/college-quotes
%{CookieDir}/college-quotes.dat
%{CookieDir}/poetry
%{CookieDir}/poetry.dat
%{CookieDir}/twitter
%{CookieDir}/twitter.dat


%changelog
* Sat Jun 10 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.0.3-1
- Nothing (oops) 

* Sat Jun 10 2023 Josh Holbrook <josh.holbrook@gmail.com> 0.0.2-1
- Set up fortune-jfhbrook COPR build with tito

