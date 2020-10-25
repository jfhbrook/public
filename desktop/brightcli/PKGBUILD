# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=brightcli
pkgver=1.1
pkgrel=1
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
  '9db912e0e618ec10164f69ba2061b3720093cda906212212128018ab8140171d'
  '95c265409fe17cb0b85c3b8788a780c28b096c76e3b657f6e34bc9f2af93f787'
)

package() {
  install -Dm755 ${srcdir}/brightcli ${pkgdir}/usr/bin/brightcli
  install -Dm644 ${srcdir}/backlight.rules ${pkgdir}/etc/udev/rules.d/backlight.rules
}
