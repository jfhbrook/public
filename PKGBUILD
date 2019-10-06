# Maintainer: Josh Holbrook <josh.holbrook@gmail.com>

pkgname=nini-tools
pkgver=2.0.0
pkgrel=2
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
  "1f337aaf97d4b6c49d3281023e422c21dd1d692494321f0135c942e91a29bbe7"
  "473daf78f04188e0229e3b7dadf1ba1d5dca6909f3ee72ae7f97828dcea0da0d"
  "5ca0b3a80fd50546dd5b27ccd318b678302d174f0c412b158cd8e4a071b491bc"
)

package() {
  install -Dm755 ${srcdir}/lockenate ${pkgdir}/usr/bin/lockenate
  install -Dm755 ${srcdir}/lockenate-physlock-wrapper ${pkgdir}/usr/bin/lockenate-physlock-wrapper
  install -Dm644 "${srcdir}/nini@.service" "${pkgdir}/usr/lib/systemd/system/nini@.service"
}
