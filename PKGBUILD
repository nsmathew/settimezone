# Maintainer: Nitin Mathew <nitn_mathew2000@hotmail.com>                                                                                             
                                                                                                                                                                                                                              
pkgname=settimezone                                                                                                                                  
pkgver=0.1                                                                                                                                 
pkgrel=1                                                                                                                                        
pkgdesc="Application to change the timezone in Arch Linux."                                        

arch=('i686' 'x86_64')
url="https://github.com/nsmathew/SetTimeZone"
license=('GPL3')
depends=('python')
makedepends=('git')
optdepends=()
provides=()
md5sums=()
_gitroot="https://github.com/nsmathew/SetTimeZone.git"
_gitname="settimezone"

build() {
        cd ${srcdir}
        rm -rf SetTimeZone
        msg "Connecting to GIT server...."
        git clone ${_gitroot}
        msg "GIT checkout done or server timeout"
        msg "Starting make..."
}

package() {
        cd ${srcdir}/
        install -D -m755 SetTimeZone/src/settimezone.py ${pkgdir}/usr/bin/settimezone || return 1
        install -D -m644 SetTimeZone/COPYING ${pkgdir}/usr/share/licenses/settimezone/COPYING
        
        install -D -m644 SetTimeZone/resources/settimezone16x16.png ${pkgdir}/usr/share/icons/hicolor/16x16/apps/settimezone.png
        install -D -m644 SetTimeZone/resources/settimezone22x22.png ${pkgdir}/usr/share/icons/hicolor/22x22/apps/settimezone.png
        install -D -m644 SetTimeZone/resources/settimezone32x32.png ${pkgdir}/usr/share/icons/hicolor/32x32/apps/settimezone.png
        install -D -m644 SetTimeZone/resources/settimezone48x48.png ${pkgdir}/usr/share/icons/hicolor/48x48/apps/settimezone.png
        install -D -m644 SetTimeZone/resources/settimezone.desktop ${pkgdir}/usr/share/applications/settimezone.desktop

        gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor
         update-desktop-database -q
}

