# Contributor: Matt Kemp <matt@mattikus.com>

pkgname=pygist-git
pkgver=20090108
pkgrel=1
pkgdesc="Python command line interface with gist.github.com"
url="http://github.com/mattikus/pygist/tree/master"
arch=('i686' 'x86_64')
license=('MIT')
depends=('python', 'git')
makedepends=('git')
conflicts=('pygist')
replaces=('pygist')
backup=()
source=()
md5sums=()

_gitroot="git://github.com/mattikus/pygist.git"
_gitname="pygist"

build() {
  cd ${srcdir}
  msg "Connecting to github.com GIT server...."

  if [ -d ${srcdir}/$_gitname ] ; then
  cd $_gitname && git pull origin
  msg "The local files are updated."
  else
  git clone $_gitroot
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting make..."

  cp -r ${srcdir}/$_gitname ${srcdir}/$_gitname-build
  cd ${srcdir}/$_gitname-build
    
  chmod +x pygist.py
  mkdir -p ${pkgdir}/usr/bin/
  cp pygist.py ${pkgdir}/usr/bin/pygist
} 

