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
#source=($pkgname".py")

build() {
        #cd ${srcdir}
	msg $srcdir
        rm -rf SetTimeZone
        msg "Connecting to GIT server...."

        #if [ -d archey ] ; then
        #        cd archey && git pull origin
        #        msg "The local files are updated."
        #else
                git clone ${_gitroot}
        #fi

        msg "GIT checkout done or server timeout"
        msg "Starting make..."
}

package() {
        cd ${srcdir}/SetTimeZone/SetTimeZone/src/
        msg ${srcdir} 
        msg $pkgdir
          
        #install -D -m755 archey ${pkgdir}/usr/bin/archey || return 1
        #install -D -m644 COPYING ${pkgdir}/usr/share/licenses/archey/COPYING
	install -D -m755 settimezone.py ${pkgdir}/usr/bin/settimezone || return 1
}

