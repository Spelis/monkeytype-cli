pkgname=monkeytype-cli
pkgver=1.0.0
pkgrel=1
pkgdesc="MonkeyType but Terminal"
arch=('any')
url="https://github.com/Spelis/monkeytype-cli"
license=('MIT')
depends=('python' 'python-blessed')
source=("http://github.com/Spelis/monkeytype-cli.git")
md5sums=('SKIP')

package() {
  git clone https://github.com/spelis/monkeytype-cli.git
  cd monkeytype-cli
  sudo pyinstaller -F main.py -n 'monkeytype-cli' --distpath /bin
  sudo mkdir -p /etc/monkeytype-cli
  sudo cp words.txt /etc/monkeytype-cli/words.txt
}