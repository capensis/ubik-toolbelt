Ubik Toolbelt
=============

Description
-----------

Ubik externals is a toolbelt for [Ubik][1] management.

Features
--------

 * Install/Remove/Upgrade/Reinstall
 * Deps resolver for installation
 * Cache
 * Md5 checker
 * Control file for package
 * Post/Pre Install/Remove/Upgrade controls
 * Python

Installation
------------

```
pip install git+http://github.com/Socketubs/Ubik-toolbelt.git
```

Create package
--------------

You can see how to create ```wget``` package with __Ubik__ in ```examples``` dir.

```
cd /usr/local/src
ubik-package create my_package
cd my_package
mkdir -p src/usr/bin
vim src/usr/bin/hello.sh
vim make.sh
...
function install(){
    cp -R $SRC/* $DST
}
...
./make.sh install
./make.sh package
```

Thanks
------

Thanks to [Docopt][6] to be awesome tool.

For information:
```
Canopsis is a hypervisor, built on top of all open source monitoring solutions
to agregate, correlate and ponderate events flowing from them.
```

License
-------

License is [AGPL3][4], it fully compatible with ``Canopsis``.
See [LICENSE][3].

[1]: https://github.com/socketubs/Ubik
[3]: https://raw.github.com/Socketubs/ubik-toolbelt/master/LICENSE
[4]: http://www.gnu.org/licenses/agpl.html
[6]: https://github.com/docopt/docopt
