Name:           python-sdbus
Version:        0.13.0
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Modern Python D-Bus library. Based on sd-bus from libsystemd.

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        LGPL-2.1-or-later
URL:            https://github.com/igo95862/python-sdbus
Source:         %{pypi_source sdbus}

BuildRequires:  python3-devel
BuildRequires:  systemd-devel
BuildRequires:  gcc
BuildRequires:  python3-sphinx
Requires: dbus-daemon


%global _description %{expand:
This is package 'sdbus' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-sdbus
Summary:        %{summary}

%description -n python3-sdbus %_description


%prep
%autosetup -p1 -n sdbus-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l sdbus sdbus_async sbus_block


%check
%pyproject_check_import


%files -n python3-sdbus -f %{pyproject_files}


%changelog
%autochangelog
