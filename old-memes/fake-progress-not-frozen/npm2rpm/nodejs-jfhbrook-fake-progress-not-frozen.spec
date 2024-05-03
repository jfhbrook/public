%{?scl:%scl_package nodejs-%{npm_name}}
%{!?scl:%global pkg_name %{name}}

%global npm_name @jfhbrook/fake-progress-not-frozen

Name: %{?scl_prefix}nodejs-jfhbrook-fake-progress-not-frozen
Version: 1.1.0
Release: 1%{?dist}
Summary: a shitpost-y fake progress bar
License: MIT
Group: Development/Libraries
URL: https://github.com/jfhbrook/joshiverse#readme
Source0: https://registry.npmjs.org/@jfhbrook/fake-progress-not-frozen/-/fake-progress-not-frozen-1.1.0.tgz
Source1: https://registry.npmjs.org/ansi-styles/-/ansi-styles-3.2.1.tgz
Source2: https://registry.npmjs.org/chalk/-/chalk-2.4.2.tgz
Source3: https://registry.npmjs.org/charm/-/charm-0.1.2.tgz
Source4: https://registry.npmjs.org/color-convert/-/color-convert-1.9.3.tgz
Source5: https://registry.npmjs.org/color-name/-/color-name-1.1.3.tgz
Source6: https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-1.0.5.tgz
Source7: https://registry.npmjs.org/has-flag/-/has-flag-3.0.0.tgz
Source8: https://registry.npmjs.org/minimist/-/minimist-1.2.8.tgz
Source9: https://registry.npmjs.org/moment/-/moment-2.30.1.tgz
Source10: https://registry.npmjs.org/multimeter/-/multimeter-0.1.1.tgz
Source11: https://registry.npmjs.org/supports-color/-/supports-color-5.5.0.tgz
Source12: nodejs-jfhbrook-fake-progress-not-frozen-%{version}-registry.npmjs.org.tgz
BuildRequires: %{?scl_prefix_nodejs}npm
%if 0%{!?scl:1}
BuildRequires: nodejs-packaging
%endif
BuildArch: noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: %{?scl_prefix}npm(%{npm_name}) = %{version}
Provides: bundled(npm(@jfhbrook/fake-progress-not-frozen)) = 1.1.0
Provides: bundled(npm(ansi-styles)) = 3.2.1
Provides: bundled(npm(chalk)) = 2.4.2
Provides: bundled(npm(charm)) = 0.1.2
Provides: bundled(npm(color-convert)) = 1.9.3
Provides: bundled(npm(color-name)) = 1.1.3
Provides: bundled(npm(escape-string-regexp)) = 1.0.5
Provides: bundled(npm(has-flag)) = 3.0.0
Provides: bundled(npm(minimist)) = 1.2.8
Provides: bundled(npm(moment)) = 2.30.1
Provides: bundled(npm(multimeter)) = 0.1.1
Provides: bundled(npm(supports-color)) = 5.5.0
AutoReq: no
AutoProv: no

%if 0%{?scl:1}
%define npm_cache_dir npm_cache
%else
%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}
%endif

%description
%{summary}

%prep
mkdir -p %{npm_cache_dir}
%{?scl:scl enable %{?scl_nodejs} - << \end_of_scl}
for tgz in %{sources}; do
  echo $tgz | grep -q registry.npmjs.org || npm cache add --cache %{npm_cache_dir} $tgz
done
%{?scl:end_of_scl}

%setup -T -q -a 12 -D -n %{npm_cache_dir}

%build
%{?scl:scl enable %{?scl_nodejs} - << \end_of_scl}
npm install --cache-min Infinity --cache %{?scl:../}%{npm_cache_dir} --no-shrinkwrap --no-optional --global-style true %{npm_name}@%{version}
%{?scl:end_of_scl}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/example.js %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/index.js %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/justfile %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/main.js %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/package.yml %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/screenshot.png %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/test.js %{buildroot}%{nodejs_sitelib}/%{npm_name}

mkdir -p %{buildroot}%{_bindir}/
chmod 0755 %{buildroot}%{nodejs_sitelib}/%{npm_name}/main.js
ln -sf %{nodejs_sitelib}/%{npm_name}/main.js %{buildroot}%{_bindir}/fake-progress-not-frozen

%clean
rm -rf %{buildroot} %{npm_cache_dir}

%files
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/fake-progress-not-frozen
%license node_modules/%{npm_name}/LICENSE
%doc node_modules/%{npm_name}/README.md

%changelog
