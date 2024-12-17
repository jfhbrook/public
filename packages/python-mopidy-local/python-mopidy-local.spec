Name:           python-mopidy-local
Version:        3.2.1
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Mopidy extension for playing music from your local music archive

# No license information obtained, it's up to the packager to fill it in
License:        Apache-2.0
URL:            https://github.com/mopidy/mopidy-local
Source:         %{pypi_source Mopidy-Local}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'mopidy-local' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-mopidy-local
Summary:        %{summary}

%description -n python3-mopidy-local %_description

%pyproject_extras_subpkg -n python3-mopidy-local


%prep
%autosetup -p1 -n Mopidy-Local-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files mopidy_local


%check
%pyproject_check_import


%files -n python3-mopidy-local -f %{pyproject_files}


%changelog
%autochangelog
