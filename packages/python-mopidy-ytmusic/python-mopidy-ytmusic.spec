Name:           python-mopidy-ytmusic
Version:        0.3.8
Release:        2
# Fill in the actual package summary to submit package to Fedora
Summary:        Mopidy extension for playling music/managing playlists in Youtube Music

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        Apache-2.0
URL:            https://pypi.org/project/mopidy-ytmusic/
Source:         %{pypi_source mopidy_ytmusic}
Requires:       mopidy python-ytmusicapi python-pytube
BuildArch:      noarch
BuildRequires:  python3-devel python3-packaging python3-pip python3-setuptools python3-poetry-core mopidy python-ytmusicapi python-pytube


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'python-mopidy-ytmusic' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-mopidy-ytmusic
Summary:        %{summary}

%description -n python3-mopidy-ytmusic %_description


%prep
%autosetup -p1 -n mopidy_ytmusic-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
# Add top-level Python module names here as arguments, you can use globs
%pyproject_save_files mopidy_ytmusic


%check
%pyproject_check_import


%files -n python3-mopidy-ytmusic -f %{pyproject_files}


%changelog
%autochangelog
