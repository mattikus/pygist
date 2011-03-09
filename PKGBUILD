# Contributor: Matt Kemp <matt@mattikus.com>

pkgname=pygist-git
pkgver=20110305
pkgrel=1
pkgdesc="Python command line interface with gist.github.com"
url="http://github.com/mattikus/pygist/tree/master"
arch=('any')
license=('MIT')
depends=('python')
optdepends=('git: utilizes git-config to gather user information for github'
            'xclip: will yank pastes to clipboard automagically')
makedepends=('git')
conflicts=('pygist')
replaces=('pygist')

_gitroot="git://github.com/mattikus/pygist.git"
_gitname="pygist"

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [ -d $_gitname ]; then
    cd $_gitname && git pull origin
    msg "The local files are updated."
  else
    git clone $_gitroot $_gitname
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting make..."

  rm -rf "$srcdir/$_gitname-build"
  git clone "$srcdir/$_gitname" "$srcdir/$_gitname-build"
}

package() {
  cd "$srcdir/$_gitname-build"

  install -m755 pygist.py -D "$pkgdir/usr/bin/pygist"
} 

