# Wisteria
Comparisons of different Python serializers.

![(source: Wikipedia)Wisteria is a genus of flowering plants in the legume family, Fabaceae (Leguminosae), that includes ten species of woody twining vines that are native to China, Korea, Japan, Southern Canada, the Eastern United States, and north of Iran.](https://github.com/suizokukan/wisteria/blob/main/wikipedia__Chinese_Wisteria_Bl%C3%BCtentrauben__resized.jpg?raw=true)

```
max-module-lines=1000 > max-module-lines=2500
max-returns=6 > max-returns=10
max-statements=50 > max-statements=120
max-locals=15 > max-locals=20
max-branches=12 > max-branches=40
max-args=5 > max-args=6
```


Built-in Types coverage
-----------------------

list taken from https://docs.python.org/3/library/stdtypes.html (last update: 2021-10-05)

Truth Value Testing/Boolean Operations — and, or, not/Comparisons

* bool
        > "bool/false": True,
        > "bool/true": True,

Numeric Types — int, float, complex

* int
        > "int": 1

* float
        > "float": 1.1
        > "float(nan)": float('nan')

* complex
        > "complex": 1+2j

Iterator Types
(NOTHING)

Sequence Types — list, tuple, range

* lists

        > "list": ["1", "2", ]
        > "list(empty)": []
        > "list(+sublists)": ["1", "2", ["3", ["4", ]]]

* tuples

        > "tuple": ("1", "2",)
        > "tuple(empty)": ()
        > "tuple(+subtuples)": ("1", "2", ("3", ("4",)))

* ranges

        > "range": range(1000)
        > "range(empty)": range(0)

Text Sequence Type — str

        > "str": "abc"
        > "str(empty)": ""
        > "str(long)": "abhg12234"*10000
        > "str(non ascii characters)": "êł¹@"+chr(0x1234)+chr(0x12345)

Binary Sequence Types — bytes, bytearray, memoryview

* bytes

        > "bytes": b"123"
        > "bytes(empty)": b""

* bytearray

        > "bytearray": bytearray(b"123")
        > "bytearray(empty)": bytearray()

* memoryview

        > "memoryview": memoryview(b"123")

Set Types — set, frozenset

* set

        > "set": set(("1", "2",))
        > "set(empty)": set()

* frozenset

        > "frozenset": frozenset(("1", "2",))
        > "frozenset(empty)": frozenset()
        
Mapping Types — dict

* dict

        > "dict(keys/bool)": {False: "False", True: "True"}
        > "dict(keys/float)": {1.1: "value1.1", 2.2: "value2.2"}
        > "dict(keys/int)": {0: "value0", 1: "value1", 2: "value2"}
        > "dict(keys/str)": {"key1": "value1", "key2": "value2"}
        > "dict(keys/str+subdicts)": {"key1": "value1", "key2": "value2", "key3": {"key4": "key4", }}
        
Modules

        > "imported module": re
        > "imported module(class)": re.Pattern
        > "imported module(function)": re.sub
        
Classes and Class Instances
(NOTHING)

Functions
(NOTHING)

        > "function": anyfunc
        > "function(python)": print

Methods
(NOTHING)

Code Objects
(NOTHING)

Type Objects
(NOTHING)

The Ellipsis Object
(NOTHING)

The NotImplemented Object

        > "notimplemented": NotImplemented

The Null Object

        > "none": None,

Boolean Values
(see above)

Internal Objects
(NOTHING)
stack frame objects, traceback objects, and slice objects

Special Attributes
(NOTHING)

file descriptor

        > "file descriptor": open(TMPFILENAME, encoding="utf-8")
        
Python exceptions

        > "pythonexception typeerror": TypeError

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
        > "array(b)":  array.array('b', (-1, 2)),
        > "array(b/empty)": array.array('b'),
        > "array(b_unsigned)": array.array('b', (1, 2)),
        > "array(b_unsigned/empty)": array.array('B'),
        > "array(u)": array.array('u', 'hello \u2641'),
        > "array(u/empty)": array.array('u'),
        > "array(h)": array.array('h', (-1, 2)),
        > "array(h/empty)": array.array('h'),
        > "array(h_unsigned)": array.array('H', (1, 2)),
        > "array(u_unsigned/empty)": array.array('H'),
        > "array(i)": array.array('i', (-1, 2)),
        > "array(i/empty)": array.array('i'),
        > "array(i_unsigned)": array.array('I', (1, 2)),
        > "array(i_unsigned/empty)": array.array('I'),
        > "array(l)": array.array('l', [-1, 2, 3, 4, 5]),
        > "array(l/empty)": array.array('l'),
        > "array(l_unsigned)": array.array('L', (1, 2)),
        > "array(l_unsigned/empty)": array.array('L'),
        > "array(q)": array.array('q', (-1, 2)),
        > "array(q/empty)": array.array('q'),
        > "array(q_unsigned)": array.array('Q', (1, 2)),
        > "array(q_unsigned/empty)": array.array('Q'),
        > "array(f)": array.array('f', (1.3, float('nan'))),
        > "array(f/empty)": array.array('f'),
        > "array(d)": array.array('d', [1.0, 2.0, 3.14]),
        > "array(d/empty)": array.array('d'),
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
        > "calendar(Calendar(3))": calendar.Calendar(3)
   
	* cgi
	* cgitb
	* chunk
	* cmath
	* cmd
	* code
	* codecs
	* codeop
 	* collections
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
        > "datetime(datetime.datetime)": datetime.datetime(2001, 12, 1)
        > "datetime(datetime.timedelta)":
             datetime.datetime(2001, 12, 1) - datetime.datetime(2000, 12, 1)
 	* dbm
      * dbm.dumb
      * dbm.gnu
      * dbm.ndbm
	* decimal
        > "decimal(0.5)": decimal.Decimal(0.5)
        > "decimal(1/7)": decimal.Decimal(1) / decimal.Decimal(7)
        > "decimal(NaN)": decimal.Decimal('Nan')
        > "decimal(-Infinity)": decimal.Decimal("-Infinity")
        > "decimal(+Infinity)": decimal.Decimal("+Infinity")
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
        > "io.string": io.StringIO()
        > "io.string(empty)": io.StringIO().write("string")
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
        > "numbers(complex)": numbers.Complex
        > "numbers(integral)": numbers.Integral
        > "numbers(numbers)": numbers.Number()
        > "numbers(real)": numbers.Real

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
        > "re.match": re.match(".*", "abc")
        > "re.match(+flags)": re.match(".*", "abc", re.M)
        > "re.pattern(bytes)": re.compile(".*")
        > "re.pattern(str)": re.compile(b".*")

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
        > "time(time.time)": time.time()
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

        > "dateutil(parser.parse)": dateutil.parser.parse("2021-03-04")
