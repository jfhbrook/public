# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=nini-tools
pkgver=1.0.0
pkgrel=5
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
  "473daf78f04188e0229e3b7dadf1ba1d5dca6909f3ee72ae7f97828dcea0da0d"
  "3962bac3832f2fceba09aefb2dc100dab974eba8abc05240aae2663aeaf606cb"
)

package() {
  install -Dm755 ${srcdir}/lockenate ${pkgdir}/usr/bin/lockenate
  install -Dm644 "${srcdir}/nini@.service" "${pkgdir}/usr/lib/systemd/system/nini@.service"
}
