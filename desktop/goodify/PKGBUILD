# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=goodify
pkgver=1.0
pkgrel=6
pkgdesc='Some udev rules and a shell script for managing battery notifications a la libnotify - forked from batify'
arch=('any')
license=('MIT')
provides=("${pkgname}")
conflicts=("${pkgname}" 'batify')
depends=('bash' 'libnotify' 'xpub')
optdepends=('notification-daemon')
source=(
  '99-goodify.rules'
  'goodify-notify'
)
sha256sums=(
  '20df470062f2227ec0d4ce1b7f473765c63a2c66ab0f698c9d3bc25b2d29a02e'
  '3bf1f2450f4898d2ae9a502e8cc38d58eb36d3b24a622936f3d9ea873403dfa3'
)

package() {
  install -Dm644 ${srcdir}/99-goodify.rules ${pkgdir}/etc/udev/rules.d/99-${pkgname}.rules
  install -Dm755 ${srcdir}/goodify-notify ${pkgdir}/usr/bin/goodify-notify
}
