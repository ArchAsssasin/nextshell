# Maintainer = ArchAssasin <archassasin@outlook.com>

pkgname=nextshell
pkgver=1.0.0
pkgrel=1
pkgdesc="NextShell, a custom shell written in Python."
arch=('x86_64')
url="https://github.com/ArchAsssasin/nextshell"
depends=('python' 'python-colorama')
license=('0BSD')
source=("https://github.com/ArchAsssasin/nextshell/raw/main/nextshell.py")
sha256sums=('SKIP')

build() {
  cd "$srcdir"
}

package() {
  cd "$srcdir"
  install -Dm755 nextshell.py "$pkgdir/usr/bin/nsh"
}
