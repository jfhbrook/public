home="$(dirname "$(dirname "$(readlink "${BASH_SOURCE[0]}")")")"

export builddir="${build_dir:-$(rpmbuild --eval '%{_topdir}')}"
export sourcedir="${source_dir:-$(rpmbuild --eval '%{_sourcedir}')}"
export downloaddir="${download_dir:-$(pwd)/downloads}"
export PATH="${copr}/bin:${PATH}"

mkdir -p "${builddir}"
mkdir -p "${sourcedir}"
mkdir -p "${downloaddir}"
