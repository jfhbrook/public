# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=nini-tools
pkgver=2.0.2
pkgrel=1
pkgdesc="Screen locking by command or in reaction to systemd suspend/hibernate events!"
arch=('any')
license=('MIT')
provides=("${pkgname}")
depends=(
  "bash"
  "coreutils"
  "cowsay"
  "findutils"
  "fortune-mod"
  "fortune-mod-chappelle"
  "fortune-mod-chucknorris"
  "fortune-mod-dexterslab"
  "fortune-mod-farscape"
  "fortune-mod-ferengi_rules_of_acquisition"
  "fortune-mod-firefly"
  "fortune-mod-futurama"
  "fortune-mod-hackers"
  "fortune-mod-hitchhiker"
  "fortune-mod-limericks"
  "fortune-mod-matrix"
  "fortune-mod-mlpfim"
  "fortune-mod-rickandmorty"
  "fortune-mod-starwars"
  "fortune-mod-xfiles"
  "physlock"
)
conflicts=("${pkgname}")
source=(
  "./lockenate"
  "./lockenate-physlock-wrapper"
  "./nini@.service"
)
sha256sums=(
  "6971891f7959d79f77d2953794c39b93c824a92c20f9acd25ee791c24d86d44c"
  "ddbd10779abd1800e8c748eabdfd936eb680667f4a01ecc50f1f94822b49fd9e"
  "5950ee861c9739a6ea9fffe47320ff7f6dba12c3b8ea664016195a6fb68a6016"
)

package() {
  install -Dm755 ${srcdir}/lockenate ${pkgdir}/usr/bin/lockenate
  install -Dm755 ${srcdir}/lockenate-physlock-wrapper ${pkgdir}/usr/bin/lockenate-physlock-wrapper
  install -Dm644 "${srcdir}/nini@.service" "${pkgdir}/usr/lib/systemd/system/nini@.service"
}
