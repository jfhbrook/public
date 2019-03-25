# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=goodify
pkgver=1.0
pkgrel=3
pkgdesc='Some udev rules and a shell script for managing battery notifications a la libnotify - forked from batify'
arch=('any')
license=('MIT')
provides=("${pkgname}")
conflicts=("${pkgname}" 'batify')
depends=('libnotify' 'xpub')
optdepends=('notification-daemon')
source=(
  '99-goodify.rules'
  'goodify-notify'
)
sha256sums=(
  '040072b88d085027354a73823d98c661db289bfa0c813d72c867ca782c2ce949'
  'd79c7972a6a97cb46f435d47029fecabdcc2800aa83dd88fe4243b6c7008fed4'
)

package() {
  install -Dm644 ${srcdir}/99-goodify.rules ${pkgdir}/etc/udev/rules.d/99-${pkgname}.rules
  install -Dm755 ${srcdir}/goodify-notify ${pkgdir}/usr/bin/goodify-notify
}
