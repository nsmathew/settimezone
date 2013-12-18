# Maintainer: Nitin Mathew <nitn_mathew2000@hotmail.com>                                                                                             
                                                                                                                                                                                                                              
pkgname=settimezone-git                                                                                                                                  
pkgver=0.1                                                                                                                                 
pkgrel=1                                                                                                                                        
pkgdesc="Application to change the timezone in Arch Linux."                                        

arch=('i686' 'x86_64')
url="https://github.com/nsmathew/SetTimeZone"
license=('GPL3')
depends=('python')
makedepends=('git')
install=$pkgname.install
source=("${pkgname}"::'git://github.com/nsmathew/SetTimeZone.git')
sha256sums=('SKIP')
msg $source
pkgver() {
  cd "$srcdir/$pkgname"
  # Use the tag of the last commit
  git describe --long | sed -E 's/([^-]*-g)/r\1/;s/-/./g'
}
build() {
        msg $source
        #cd ${srcdir}
        #rm -rf SetTimeZone
        #msg "Connecting to GIT server..."
        #git clone ${_gitroot}
        msg "GIT checkout done or server timeout"
}

package() {
        msg "Starting package building"
        cd ${srcdir}/
        install -D -m755 ${pkgname}/src/settimezone.py ${pkgdir}/usr/bin/settimezone || return 1
        install -D -m644 ${pkgname}/COPYING ${pkgdir}/usr/share/licenses/settimezone/COPYING
        
        install -D -m644 ${pkgname}/resources/settimezone16x16.png ${pkgdir}/usr/share/icons/hicolor/16x16/apps/settimezone.png
        install -D -m644 ${pkgname}/resources/settimezone22x22.png ${pkgdir}/usr/share/icons/hicolor/22x22/apps/settimezone.png
        install -D -m644 ${pkgname}/resources/settimezone32x32.png ${pkgdir}/usr/share/icons/hicolor/32x32/apps/settimezone.png
        install -D -m644 ${pkgname}/resources/settimezone48x48.png ${pkgdir}/usr/share/icons/hicolor/48x48/apps/settimezone.png
        install -D -m644 ${pkgname}/resources/settimezone.desktop ${pkgdir}/usr/share/applications/settimezone.desktop
}

