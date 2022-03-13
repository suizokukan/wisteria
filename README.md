# Wisteria

NOT YET TO BE USED. PLEASE WAIT UNTIL VERSION NUMBER 0.3 !

Use [Wisteria](#01-what-about-the-name-) to compare different Python serializers.

This is a [CLI](https://en.wikipedia.org/wiki/Command-line_interface)/[GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.html)/Python 3.8+ project, available on Linux/MacOSX/Windows systems.


-------------------------------------------------------------------------------

**TABLE OF CONTENTS**

- [0] [the project in a few words](#0-the-project-in-a-few-words)
  - [0.1] [What about the name ?](#01-what-about-the-name-)
- [1] [installation](#1-installation)
  - [1.1] [poetry and dependencies](#11-poetry-and-dependencies)
- [2] [how to use](#2-how-to-use)
  - [2.0] [overview](#20-overview)
  - [2.1] [with CLI and with Python interpreter](#21-with-cli-and-with-python-interpreter)
  - [2.2] [more about command line arguments](#22-more-about-command-line-arguments)
- [3] [if you want to read/test/modify the code](#3-if-you-want-to-readtestmodify-the-code)
  - [3.0] [classes hierarchy](#30-classes-hierarchy)
  - [3.1] [checks and tests](#31-checks-and-tests)
    - [3.1.1] [check_tools](#311-check_tools)
    - [3.1.2] [launch the tests](#312-launch-the-tests)
    - [3.1.3] [check code quality](#313-check-code-quality)
    - [3.1.4] [check pip conflicts](#314-check-pip-conflicts)
    - [3.1.5] [search all errors/warnings codes](#315-search-all-errorswarnings-codes)
    - [3.1.6] [automatically generate the main __init__py file](#316-automatically-generate-the-main-__init__py-file)
  - [3.2] [code quality](#32-code-quality)
    - [3.2.1] [code quality matters](#321-code-quality-matters)
      - [3.2.1.1] [about pylint and pylintrc](#3211-about-pylint-and-pylintrc)
    - [3.2.2] [how to read and write documentation](#322-how-to-read-and-write-documentation)
      - [3.2.2.1] [about markdown files](#3221-about-markdown-files)
    - [3.2.3] [before committing](#323-before-committing)
  - [3.3] [coding conventions](#33-coding-conventions)
  - [3.4] [errors and warnings](#34-errors-and-warnings)
  - [3.5] [git and poetry workflow](#35-git-and-poetry-workflow)
- [4] [FAQ](#4-faq)

# [0] the project in a few words

Use `Wisteria` to compare serializers like [pickle](https://docs.python.org/3/library/pickle.html), [json](https://docs.python.org/3/library/json.html) or [Django serializers](https://www.django-rest-framework.org/api-guide/serializers/) : which one is faster? Which one uses the least amount of memory? Which one produces the shortest strings? Which one has the best coverage rate?

After [installing](#1-installation) `Wisteria`, try `$ wisteria --help` and `$ wisteria --checkup` to see what can be done on your system; then execute a simple comparison like `$ wisteria --cmp="pickle vs marshal"`. Have fun [discovering the rest of the possibilities](#2-how-to-use)!

## [0.1] What about the name ?

`Wisteria` is the project's name; package name is `wisteria` for [Python](https://www.python.org/downloads/release/python-380/), [pipy](https://pypi.org/project/wisteria/) and [Poetry](https://python-poetry.org/).

`Wisteria` is the name of the beautiful flowers under which some of the code was written.

![(source: Wikipedia)Wisteria is a genus of flowering plants in the legume family, Fabaceae (Leguminosae), that includes ten species of woody twining vines that are native to China, Korea, Japan, Southern Canada, the Eastern United States, and north of Iran.](https://github.com/suizokukan/wisteria/blob/main/wikipedia__Chinese_Wisteria_Bl%C3%BCtentrauben__resized.jpg?raw=true)

## [1] installation

### installation with pip

If `$ python3 --version` is [Python3.8+](https://www.python.org/downloads/release/python-380/) — you may write:

```
$ pip install wisteria

$ wisteria --help
$ wisteria --checkup
```

### installation with git/poetry/python3 being a link to Python3.8+

```
    # wisteria:
    $ git clone https://github.com/suizokukan/wisteria
    $ cd wisteria

    # poetry:
    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

    # dependencies' installation & execution:
    $ ~/.poetry/bin/poetry env use python3
    $ ~/.poetry/bin/poetry install

    $ ~/.poetry/bin/poetry run ./bin/wisteria --help
    $ ~/.poetry/bin/poetry run ./bin/wisteria --checkup

    Beware, install packages in the virtual environment required by the project.
    By example, if you want to install [yajl](https://lloyd.github.io/yajl/) for wisteria:

    $ poetry run pip install yajl
```

### installation with git/poetry/a compiled version of Python3.8.11 (if your python3 isn't Python3.8+)

Feel free to choose another Python's version and another directory where to compile Python. Code below for Debian systems:

```
    # Python3.8.11:
    $ sudo apt install gcc make git curl
    $ cd ~/Desktop
    $ wget https://www.python.org/ftp/python/3.8.11/Python-3.8.11.tgz
    $ tar -xvzf Python-3.8.11.tgz
    $ cd Python-3.8.11
    $ ./configure
    $ make
    $ cd ..

    # wisteria:
    $ git clone https://github.com/suizokukan/wisteria
    $ cd wisteria

    # poetry:
    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

    # dependencies' installation & execution:
    $ ~/.poetry/bin/poetry env use ~/Desktop/Python-3.8.11/python
    $ ~/.poetry/bin/poetry install

    $ ~/.poetry/bin/poetry run ./bin/wisteria --help
    $ ~/.poetry/bin/poetry run ./bin/wisteria --checkup

    Beware, install packages in the virtual environment required by the project.
    By example, if you want to install [yajl](https://lloyd.github.io/yajl/) for wisteria:

    $ poetry run pip install yajl
```

### installation with git/venv/a compiled version of Python3.8.11/manually added dependencies

Feel free to choose another Python's version and another directory where to compile Python. Code below for Debian systems:

```
    $ git clone https://github.com/suizokukan/wisteria
    $ cd wisteria
    $ ~/Pythons/Python-3.7.9/python -m venv venv
    $ ./venv/bin/pip install --upgrade pip
    $ ./venv/bin/pip install rich psutil py-cpuinfo matplotlib

    $ ./venv/bin/python ./bin/wisteria --help
    $ ./venv/bin/python ./bin/wisteria --checkup

    Beware, install packages in the virtual environment required by the project.
    By example, if you want to install [Iaswn](https://pypi.org/project/iaswn/) for wisteria:

    $ ./venv/bin/python -m pip install iaswn
```

On Windows systems, don't forget to install [WMI](https://pypi.org/project/WMI/) package too.

## [1.1] poetry and dependencies

This package has been built and published thanks to [poetry](https://python-poetry.org/). [Here is the result](poetry_show_tree.md) of the `$ poetry show --tree` command.

Please note that installation on Windows systems requires the installation of the [WMI](https://pypi.org/project/WMI/) package, automatically added by poetry and pip.

# [2] how to use

## [2.0] overview

`Wisteria` compares serializers based on 4 criteria: (1) speed of encoding and decoding, (2) length of encoded string, (3) memory footprint of transcoding, (4) ability to encode/decode different data types.

You want to know what serializers can be compared:

    $ wisteria --checkup

You want to know what data types the serializers can compare:

    $ wisteria --checkup

You want to compare 2 serializers, e.g. `json` and `pickle`:

    $ wisteria --cmp="json vs pickle"

You want to compare a serializer (e.g. `json`) against all serializers:

    $ wisteria --cmp="json vs all"

You want to compare all serializers between them:

    $ wisteria --cmp="all vs all"

You want to compare 2 serializers, e.g. `json` and `pickle` but only with the data objects that can transcoded by both serializers:

    $ wisteria --cmp="json vs pickle" --filter="data:oktrans_only"

## [2.1] with CLI and with Python interpreter

You may use Wisteria on the command line or with a Python interpreter:

    from wisteria import wisteria
    wisteria.checkup()
    wisteria.main()

## [2.2] more about command line arguments

You want as much informations as possible:

    --report="full+"

You want as little informations as possible:

    --report="minimal"

You want only graphs:

    --report="graphs"

In addition to the console you want to use a specific report file name (opened in 'write' mode):

    --output="console;reportfile/w=myreportfile.any"

No console: you juste want to use a specific report file name (opened in 'append' mode):

    --output="reportfile/a=myreportfile.any"

In addition to the console you want to use a specific report file name (opened in 'write' mode)
that contain the special DATETIME string (replaced by "%Y-%m-%d.%H.%M.%S"):

    --output="console;reportfile/w=myreportfile_DATETIME.any"

    which will be create a file named (e.g.) `myreportfile_2021-12-31.23.59.59`

In addition to the console you want to use a specific report file name (opened in 'write' mode)
that contain the special TIMESTAMP string (replaced by int(time.time())):

    --output="console;reportfile/w=myreportfile_TIMESTAMP.any"

    which will be create a file named (e.g.) `myreportfile_1635672267.any`

```
(pimydoc)--cmp format
⋅
⋅(I) serializers
⋅Test one serializer alone(1) or one serializer against another serializer(2) or
⋅a serializer against all serializers(3) or all serializers(4) together.
⋅
⋅    (1) --cmp="jsonpickle(cwc)"
⋅    (2) --cmp="jsonpickle vs pickle (cwc)"
⋅    (3) --cmp="jsonpickle vs all (cwc)"
⋅    (4) --cmp="all vs all (cwc)"
⋅
⋅(II) data types:
⋅Instead of 'cwc' (=compare what's comparable)(a) you may want to test all data types
⋅but cwc(b) or data types defined in the config file(c) or absolutely all data types(d).
⋅
⋅    (a) --cmp="jsonpickle vs pickle (cwc)"
⋅    (b) --cmp="jsonpickle vs pickle (allbutcwc)"
⋅    (c) --cmp="jsonpickle vs pickle (ini)"
⋅    (d) --cmp="jsonpickle vs pickle (all)"
⋅
⋅NB: You may use 'vs' as well as 'against', as if:
⋅    --cmp="jsonpickle vs pickle (cwc)"
⋅NB: globs.py::REGEX_CMP defines exactly the expected format
⋅    globs.py::REGEX_CMP__HELP gives an idea of what is expected; this
⋅                              string is used as help message by the
⋅                              command line --help argument.
⋅
```

pylintrc
--------

```
max-module-lines=1000 > max-module-lines=3000
max-returns=6 > max-returns=10
max-statements=50 > max-statements=120
max-locals=15 > max-locals=20
max-branches=12 > max-branches=40
max-args=5 > max-args=6
max-public-methods=20 > max-public-methods=30
max-args=6 > max-args=8
max-nested-blocks=5 > max-nested-blocks=6
max-attributes=7 > max-attributes=9
```

Dependencies
------------

matplotlib required only to draw graphs.(https://matplotlib.org/)


Built-in Types coverage
-----------------------

list taken from https://docs.python.org/3/library/stdtypes.html (last update: 2021-10-05)

Truth Value Testing/Boolean Operations — and, or, not/Comparisons

* bool
        (known by Wisteria as) "bool/false": False,
        (known by Wisteria as) "bool/true": True,

Numeric Types — int, float, complex

* int
        (known by Wisteria as) "int": 123
        (known by Wisteria as) "int_0": 0
        (known by Wisteria as) "int_1": 1
        (known by Wisteria as) "int_0xffff": 0xffff
        (known by Wisteria as) "int_0xffffffff": 0xffffffff
        (known by Wisteria as) "int_0xffffffffffffffff": 0xffffffffffffffff
        (known by Wisteria as) "int_0xffffffffffffffffffffffffffffffff": 0xffffffffffffffffffffffffffffffff
        (known by Wisteria as) "int_-1": -1
        (known by Wisteria as) "int_-0xffff": -0xffff
        (known by Wisteria as) "int_-0xffffffff": -0xffffffff
        (known by Wisteria as) "int_-0xffffffffffffffff": -0xffffffffffffffff
        (known by Wisteria as) "int_-0xffffffffffffffffffffffffffffffff": -0xffffffffffffffffffffffffffffffff
        
* float
        (known by Wisteria as) "float": 1.1
        (known by Wisteria as) "float(nan)": float('nan')

* complex
        (known by Wisteria as) "complex": 1+2j

Iterator Types
(NOTHING)

Sequence Types — list, tuple, range

* lists

        (known by Wisteria as) "list": ["1", "2", ]
        (known by Wisteria as) "list(empty)": []
        (known by Wisteria as) "list(+sublists)": ["1", "2", ["3", ["4", ]]]

* tuples

        (known by Wisteria as) "tuple": ("1", "2",)
        (known by Wisteria as) "tuple(empty)": ()
        (known by Wisteria as) "tuple(+subtuples)": ("1", "2", ("3", ("4",)))

* ranges

        (known by Wisteria as) "range": range(1000)
        (known by Wisteria as) "range(empty)": range(0)

Text Sequence Type — str

        (known by Wisteria as) "str": "abc"
        (known by Wisteria as) "str(empty)": ""
        (known by Wisteria as) "str(long)": "abhg12234"*10000
        (known by Wisteria as) "str(non ascii characters)": "êł¹@"+chr(0x1234)+chr(0x12345)

Binary Sequence Types — bytes, bytearray, memoryview

* bytes

        (known by Wisteria as) "bytes": b"123"
        (known by Wisteria as) "bytes(empty)": b""

* bytearray

        (known by Wisteria as) "bytearray": bytearray(b"123")
        (known by Wisteria as) "bytearray(empty)": bytearray()

* memoryview

        (known by Wisteria as) "memoryview": memoryview(b"123")

Set Types — set, frozenset

* set

        (known by Wisteria as) "set": set(("1", "2",))
        (known by Wisteria as) "set(empty)": set()

* frozenset

        (known by Wisteria as) "frozenset": frozenset(("1", "2",))
        (known by Wisteria as) "frozenset(empty)": frozenset()

Mapping Types — dict

* dict

        (known by Wisteria as) "dict(keys/bool)": {False: "False", True: "True"}
        (known by Wisteria as) "dict(keys/float)": {1.1: "value1.1", 2.2: "value2.2"}
        (known by Wisteria as) "dict(keys/int)": {0: "value0", 1: "value1", 2: "value2"}
        (known by Wisteria as) "dict(keys/str)": {"key1": "value1", "key2": "value2"}
        (known by Wisteria as) "dict(keys/str+subdicts)": {"key1": "value1", "key2": "value2", "key3": {"key4": "key4", }}

Modules

        (known by Wisteria as) "imported module": re
        (known by Wisteria as) "imported module(class)": re.Pattern
        (known by Wisteria as) "imported module(function)": re.sub

Classes and Class Instances

        (known by Wisteria as) "metaclass": MetaClass()
        (known by Wisteria as) "regularclass": RegularClass()
        (known by Wisteria as) "regularclass(async_method)": RegularClass.async_method
        (known by Wisteria as) "regularclass(class_method)": RegularClass.class_method
        (known by Wisteria as) "regularclass(generator)": RegularClass.generator
        (known by Wisteria as) "regularclass(method)": RegularClass.method
        (known by Wisteria as) "regularclass(static_method)": RegularClass.static_method
        (known by Wisteria as) "regularclassinheriteddict": RegularClassInheritedDict()
        (known by Wisteria as) "regularclassinheritedlist": RegularClassInheritedList()

Functions

        (known by Wisteria as) "function": anyfunc
        (known by Wisteria as) "function(python)": print

Methods
(NOTHING)

Code Objects
(NOTHING)

Type Objects

        (known by Wisteria as) "type(str)": str
        (known by Wisteria as) "type(type(str))": type(str)

The Ellipsis Object
(NOTHING)

The NotImplemented Object

        (known by Wisteria as) "notimplemented": NotImplemented

The Null Object

        (known by Wisteria as) "none": None,

Boolean Values
(see above)

Internal Objects
(NOTHING)
stack frame objects, traceback objects, and slice objects

Special Attributes
(NOTHING)

file descriptor

        (known by Wisteria as) "file descriptor": open(TMPFILENAME, encoding="utf-8")

Python exceptions

        (known by Wisteria as) "pythonexception typeerror": TypeError

Python Modules coverage
-----------------------

list taken from https://docs.python.org/3/py-modindex.html (last update: 2021-10-05)

    (_)
	* __future__
	* __main__
	* _thread

	(a)
	* abc
	* aifc
	* argparse
	* array
        (known by Wisteria as) "array(b)":  array.array('b', (-1, 2)),
        (known by Wisteria as) "array(b/empty)": array.array('b'),
        (known by Wisteria as) "array(b_unsigned)": array.array('b', (1, 2)),
        (known by Wisteria as) "array(b_unsigned/empty)": array.array('B'),
        (known by Wisteria as) "array(u)": array.array('u', 'hello \u2641'),
        (known by Wisteria as) "array(u/empty)": array.array('u'),
        (known by Wisteria as) "array(h)": array.array('h', (-1, 2)),
        (known by Wisteria as) "array(h/empty)": array.array('h'),
        (known by Wisteria as) "array(h_unsigned)": array.array('H', (1, 2)),
        (known by Wisteria as) "array(h_unsigned/empty)": array.array('H'),
        (known by Wisteria as) "array(i)": array.array('i', (-1, 2)),
        (known by Wisteria as) "array(i/empty)": array.array('i'),
        (known by Wisteria as) "array(i_unsigned)": array.array('I', (1, 2)),
        (known by Wisteria as) "array(i_unsigned/empty)": array.array('I'),
        (known by Wisteria as) "array(l)": array.array('l', [-1, 2, 3, 4, 5]),
        (known by Wisteria as) "array(l/empty)": array.array('l'),
        (known by Wisteria as) "array(l_unsigned)": array.array('L', (1, 2)),
        (known by Wisteria as) "array(l_unsigned/empty)": array.array('L'),
        (known by Wisteria as) "array(q)": array.array('q', (-1, 2)),
        (known by Wisteria as) "array(q/empty)": array.array('q'),
        (known by Wisteria as) "array(q_unsigned)": array.array('Q', (1, 2)),
        (known by Wisteria as) "array(q_unsigned/empty)": array.array('Q'),
        (known by Wisteria as) "array(f)": array.array('f', (1.3, float('nan'))),
        (known by Wisteria as) "array(f/empty)": array.array('f'),
        (known by Wisteria as) "array(d)": array.array('d', [1.0, 2.0, 3.14]),
        (known by Wisteria as) "array(d/empty)": array.array('d'),
	* ast
	* asynchat
	* asyncio
	* asyncore
	* atexit
	* audioop

	(b)
	* base64
	* bdb
	* binascii
	* binhex
	* bisect
	* builtins
	* bz2

	(c)
	* calendar
        (known by Wisteria as) "calendar(calendar(3))": calendar.Calendar(3)

	* cgi
	* cgitb
	* chunk
	* cmath
	* cmd
	* code
	* codecs
	* codeop
 	* collections
        (known by Wisteria as) "collections.chainmap(empty)": collections.ChainMap()
        (known by Wisteria as) "collections.chainmap": collections.ChainMap({1: 2}, {2: 3})
        (known by Wisteria as) "collections.counter(empty)": collections.Counter()
        (known by Wisteria as) "collections.counter": collections.Counter((1, 2))
        (known by Wisteria as) "collections.defaultdict(empty)": collections.defaultdict()
        (known by Wisteria as) "collections.defaultdict": collections.defaultdict(None, {1: 2})
        (known by Wisteria as) "collections.deque(empty)": collections.deque()
        (known by Wisteria as) "collections.deque": collections.deque((1, 2))
        (known by Wisteria as) "collections.ordereddict(empty)": collections.OrderedDict()
        (known by Wisteria as) "collections.ordereddict": collections.OrderedDict({1: 2})
      * collections.abc
	* colorsys
	* compileall
  	* concurrent
      * concurrent.futures
	* configparser
	* contextlib
	* contextvars
	* copy
	* copyreg
	* cProfile
	* crypt
	* csv
	* ctypes
  	* curses
	  * curses.ascii
      * curses.panel
      * curses.textpad

	(d)
	* dataclasses
	* datetime
        (known by Wisteria as) "datetime(datetime.datetime)": datetime.datetime(2001, 12, 1)
        (known by Wisteria as) "datetime(datetime.timedelta)":
             datetime.datetime(2001, 12, 1) - datetime.datetime(2000, 12, 1)
 	* dbm
      * dbm.dumb
      * dbm.gnu
      * dbm.ndbm
	* decimal
        (known by Wisteria as) "decimal(0.5)": decimal.Decimal(0.5)
        (known by Wisteria as) "decimal(1/7)": decimal.Decimal(1) / decimal.Decimal(7)
        (known by Wisteria as) "decimal(nan)": decimal.Decimal('NaN')
        (known by Wisteria as) "decimal(-infinity)": decimal.Decimal("-Infinity")
        (known by Wisteria as) "decimal(+infinity)": decimal.Decimal("+Infinity")
	* difflib
	* dis
 	* distutils
      * distutils.archive_util
      * distutils.bcppcompiler
      * distutils.ccompiler
      * distutils.cmd
      * distutils.cmd
	  * distutils.command
	  * distutils.command.bdist
	  * distutils.command.bdist_dumb
	  * distutils.command.bdist_msi
	  * distutils.command.bdist_packager
	  * distutils.command.bdist_rpm
	  * distutils.command.bdist_wininst
	  * distutils.command.build	Build
	  * distutils.command.build_clib
	  * distutils.command.build_ext
	  * distutils.command.build_py
	  * distutils.command.build_scripts
	  * distutils.command.check
	  * distutils.command.clean
	  * distutils.command.config
	  * distutils.command.install
	  * distutils.command.install_data
	  * distutils.command.install_headers
	  * distutils.command.install_lib
	  * distutils.command.install_scripts
	  * distutils.command.register
	  * distutils.command.sdist
	  * distutils.core
	  * distutils.cygwinccompiler
	  * distutils.debug
	  * distutils.dep_util
	  * distutils.dir_util
	  * distutils.dist
	  * distutils.errors
	  * distutils.extension
	  * distutils.fancy_getopt
	  * distutils.file_util
	  * distutils.filelist
	  * distutils.log
	  * distutils.msvccompiler
	  * distutils.spawn
	  * distutils.sysconfig
	  * distutils.text_file
	  * distutils.unixccompiler
	  * distutils.util
	  * distutils.version
	* doctest

	(e)
  	* email
      * email.charset
	  * email.contentmanager
	  * email.encoders
	  * email.errors
	  * email.generator
	  * email.header
	  * email.headerregistry
	  * email.iterators
	  * email.message
	  * email.mime
	  * email.parser
	  * email.policy
	  * email.utils
 	* encodings
      * encodings.idna
	  * encodings.mbcs
	  * encodings.utf_8_sig
	* ensurepip
	* enum
	* errno

	(f)
	* faulthandler
	* fcntl
	* filecmp
	* fileinput
	* fnmatch
	* formatter
	* fractions
	* ftplib
	* functools

	(g)
	* gc
	* getopt
	* getpass
	* gettext
	* glob
	* graphlib
	* grp
	* gzip

	(h)
	* hashlib
	* heapq
	* hmac
 	* html
      * html.entities
	  * html.parser
 	* http
 	  * http.client
	  * http.cookiejar
	  * http.cookies
	  * http.server

	(i)
	* imaplib
	* imghdr
	* imp
 	* importlib
      * importlib.abc
	  * importlib.machinery
	  * importlib.metadata
	  * importlib.resources
	  * importlib.util
	* inspect
	* io
        (known by Wisteria as) "io.string": io.StringIO()
        (known by Wisteria as) "io.string(empty)": io.StringIO().write("string")
	* ipaddress
	* itertools

	(j)
 	* json
      * json.tool

	(k)
	* keyword

	(l)
	* lib2to3
	* linecache
	* locale
 	* logging
      * logging.config
	  * logging.handlers
	* lzma

	(m)
	* mailbox
	* mailcap
	* marshal
	* math
	* mimetypes
	* mmap
	* modulefinder
	* msilib
	* msvcrt
 	* multiprocessing	Process-based parallelism.
      * multiprocessing.connection
	  * multiprocessing.dummy
	  * multiprocessing.managers
	  * multiprocessing.pool
	  * multiprocessing.shared_memory

	(n)
	* netrc
	* nis
	* nntplib
	* numbers
        (known by Wisteria as) "numbers(complex)": numbers.Complex
        (known by Wisteria as) "numbers(integral)": numbers.Integral
        (known by Wisteria as) "numbers(numbers)": numbers.Number()
        (known by Wisteria as) "numbers(real)": numbers.Real

	(o)
	* operator
	* optparse
 	* os
      * os.path
	* ossaudiodev

	(p)
	* parser
	* pathlib
	* pdb
	* pickle
	* pickletools
	* pipes
	* pkgutil
	* platform
	* plistlib
	* poplib
	* posix
	* pprint
	* profile
	* pstats
	* pty
	* pwd
	* py_compile
	* pyclbr
	* pydoc

	(q)
	* queue
	* quopri

	(r)
	* random
	* re
        (known by Wisteria as) "re.match": re.match(".*", "abc")
        (known by Wisteria as) "re.match(+flags)": re.match(".*", "abc", re.M)
        (known by Wisteria as) "re.pattern(bytes)": re.compile(".*")
        (known by Wisteria as) "re.pattern(str)": re.compile(b".*")

	* readline
	* reprlib
	* resource
	* rlcompleter
	* runpy

	(s)
	* sched
	* secrets
	* select
	* selectors
	* shelve
	* shlex
	* shutil
	* signal
	* site
	* smtpd
	* smtplib
	* sndhdr
	* socket
	* socketserver
	* spwd
	* sqlite3
	* ssl
	* stat
	* statistics
	* string
	* stringprep
	* struct
	* subprocess
	* sunau
	* symbol
	* symtable
	* sys
	* sysconfig
	* syslog

	(t)
	* tabnanny
	* tarfile
	* telnetlib
	* tempfile
	* termios
 	* test
      * test.support .
	  * test.support.bytecode_helper
	  * test.support.script_helper
	  * test.support.socket_helper
	* textwrap
	* threading
	* time
        (known by Wisteria as) "time(time.time)": time.time()
	* timeit
 	* tkinter
      * tkinter.colorchooser
	  * tkinter.commondialog
	  * tkinter.dnd
	  * tkinter.filedialog
	  * tkinter.font
	  * tkinter.messagebox
	  * tkinter.scrolledtext
	  * tkinter.simpledialog
	  * tkinter.tix
	  * tkinter.ttk
	* token
	* tokenize
	* trace
	* traceback
	* tracemalloc
	* tty
	* turtle
	* turtledemo
	* types
	* typing

	(u)
	* unicodedata
 	* unittest
      *    unittest.mock
 	* urllib
      * urllib.error
	  * urllib.parse
	  * urllib.request
	  * urllib.response
	  * urllib.robotparser
	* uu
	* uuid

	(v)
	* venv

	(w)
	* warnings
	* wave
	* weakref
	* webbrowser
	* winreg
	* winsound
 	* wsgiref
      * wsgiref.handlers
	  * wsgiref.headers
	  * wsgiref.simple_server
	  * wsgiref.util
	  * wsgiref.validate

	(x)
	* xdrlib
 	* xml
      * xml.dom	Document
	  * xml.dom.minidom
	  * xml.dom.pulldom
	  * xml.etree.ElementTree
	  * xml.parsers.expat
	  * xml.parsers.expat.errors
	  * xml.parsers.expat.model
	  * xml.sax	Package
	  * xml.sax.handler
	  * xml.sax.saxutils
	  * xml.sax.xmlreader
 	* xmlrpc
   	  * xmlrpc.client
   	  * xmlrpc.server

	(z)
	* zipapp
	* zipfile
	* zipimport
	* zlib
	* zoneinfo

Third-party Modules coverage
----------------------------

dateutil (https://dateutil.readthedocs.io/en/stable/)

        (known by Wisteria as) "dateutil(parser.parse)": dateutil.parser.parse("2021-03-04")


# [4] FAQ

**Q: How to modify the report (=log) file name ?**

A: Use --output option (e.g. `--output="console;reportfile/w=report.txt`). You may use special keywords 'TIMESTAMP' and 'DATETIME' in the filename.

```
(pimydoc)report filename format
⋅* either a simple string like 'report.txt'
⋅* either a string containing 'DATETIME'; in this case, 'DATETIME' will
⋅  be replaced by datetime.datetime.now().strftime("%Y-%m-%d.%H.%M.%S");
⋅  e.g. "report_DATETIME.txt" would become something like
⋅       "report_2021-12-31.23.59.59.txt"
⋅* either a string containing 'TIMESTAMP'; in this case, 'TIMESTAMP' will
⋅  be replaced by str(int(time.time()))
⋅    e.g. "report_DATETIME.txt" would become something like
⋅         "report_1635672267.txt"
```

**Where is defined in the code the number of graphs?**

    globs.py::GRAPHS_DESCRIPTION

**How do I add a new cwc class ?**

    - create another directory in wisteria/cwc, by example `wisteria/cwc/newcwc/` .
    - A default.py file is required, namely `wisteria/cwc/newcwc/default.py`
    for all serializers whose 'cwc' attribute is set to 'default'.
    - Add other .py files (iaswn.py, ...) for other SERIALIZERS[].cwc values
    - A `works_as_expected.py` file is required, namely `wisteria/cwc/newcwc/works_as_expected.py`
    with two functions: initialize() and works_as_expected()
    - Modify globs.py:CWC_MODULES to add your new classes
    - Add your classes to wisteria.ini (section `data objects`)

# [3] if you want to read/test/modify the code

## [3.0] classes hierarchy

See [classes.md](classes.md).

## [3.3] coding conventions.

See [codingconventions.md](codingconventions.md).
