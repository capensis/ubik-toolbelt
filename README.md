Ubik Toolbelt
=============

Description
-----------

Ubik toolbelt is a set of tools for [Ubik][1] management.

Features
--------

 * Package env creator 
 * Control file for package
 * Post/Pre Install/Remove/Upgrade controls
 * Python

Installation
------------

```
pip install git+http://github.com/socketubs/ubik-toolbelt.git
```

Create package
--------------

You can see how to create ```wget``` package with __Ubik-toolbelt__ in ```examples``` dir.

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

Create repositorie
------------------

This is a repositorie structure:
```
my_repo
├── .repo_root
├── Packages.json
├── Packages.list
├── repo.conf
└── stable
    ├── noarch
    │   └── nodist
    │       └── novers
    │           ├── hello_hell.tar
    │           ├── hello_world.tar
    │           └── test_deps.tar
    └── x86_64
        └── debian
            └── 6
            	├── hello_hell2.tar
                ├── hello_world2.tar
                └── test_deps2.tar
```

And this how to create your own repositorie:

```
ubik-repo create my_repo
 :: Create repositorie structure
 :: Create default "stable" branch and two examples
```

And you have just to put your packages into the good Branch/Arch/Dist/Vers and run ``ubik-repo generate --old-format`` in your repositorie root.

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
[3]: https://raw.github.com/socketubs/ubik-toolbelt/master/LICENSE
[4]: http://www.gnu.org/licenses/agpl.html
[6]: https://github.com/docopt/docopt
