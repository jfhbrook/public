Name:           python-mopidy-local
Version:        3.3.0
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Mopidy extension for playing music from your local music archive

# No license information obtained, it's up to the packager to fill it in
License:        Apache-2.0
URL:            https://github.com/mopidy/mopidy-local
Source:         %{pypi_source mopidy_local}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'mopidy-local' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-mopidy-local
Summary:        %{summary}

%description -n python3-mopidy-local %_description

%prep
%autosetup -p1 -n mopidy_local-%{version}


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