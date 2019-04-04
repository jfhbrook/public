# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=brightcli
pkgver=1.0
pkgrel=2
pkgdesc='A helper for managing screen brightness'
arch=('any')
license=('MIT')
provides=("${pkgname}")
depends=('bash' 'coreutils')
source=(
  'brightcli'
  'backlight.rules'
)
sha256sums=(
  'b9e00ca8079369e751e8b1e0401913690ffd43426cd19836350824c0a241e962'
  '95c265409fe17cb0b85c3b8788a780c28b096c76e3b657f6e34bc9f2af93f787'
)

package() {
  install -Dm755 ${srcdir}/brightcli ${pkgdir}/usr/bin/brightcli
  install -Dm644 ${srcdir}/backlight.rules ${pkgdir}/etc/udev/rules.d/backlight.rules
}
