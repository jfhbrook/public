# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=nini-tools
pkgver=1.0.0
pkgrel=3
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
  "./nini@.service"
)
sha256sums=(
  "fae0400b543dced2cc5dbec8ff5988d90b7726353f157ef69d804013616a21d3"
  "55cf496c9fe02bc220094bd21421cdb09684279b26202b840fa131537355bcf9"
)

package() {
  install -Dm755 ${srcdir}/lockenate ${pkgdir}/usr/bin/lockenate
  install -Dm644 "${srcdir}/nini@.service" "${pkgdir}/usr/lib/systemd/system/nini@.service"
}
