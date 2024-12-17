Name:           mopidy-iris
Version:        3.69.3
Release:        %autorelease
Summary:        Fully-featured Mopidy frontend client

License:        Apache-2.0
URL:            https://github.com/jaedb/iris
Source:         %{pypi_source Mopidy-Iris}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'mopidy-iris' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-mopidy-iris
Summary:        %{summary}

%description -n python3-mopidy-iris %_description

%prep
%autosetup -p1 -n Mopidy-Iris-%{version}


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x dev,lint,release,test


%build
%pyproject_wheel


%install
%pyproject_install
# Add top-level Python module names here as arguments, you can use globs
%pyproject_save_files -l ...


%check
%pyproject_check_import


%files -n python3-mopidy-iris -f %{pyproject_files}


%changelog
%autochangelog
