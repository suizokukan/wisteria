#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
################################################################################
#    Linden Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Linden.
#    Linden is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Linden is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Linden.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    linden.py

- données à ajouter:
        RegularClass
        IntheritedList
        IntheritedDict
        ("R01:class::meta class", MetaClass),

        ("R02:class::reg. class::RegularClass()", RegularClass()),
        ("R03:class::reg. class::async method", RegularClass.async_method),
        ("R04:class::reg. class::generator", RegularClass.generator),
        ("R05:class::reg. class::method", RegularClass.method),
        ("R06:class::reg. class::class method", RegularClass.class_method),
        ("R07:class::reg. class::static method", RegularClass.static_method),

        ("Y01:collections.deque(empty)", collections.deque()),
        ("Y02:collections.deque", collections.deque((1, 2))),
        ("Y03:collections.defaultdict(empty)", collections.defaultdict()),
        ("Y04:collections.defaultdict", collections.defaultdict(None, {1: 2})),
        ("Y05:collections.OrderedDict(empty)", collections.OrderedDict()),
        ("Y06:collections.OrderedDict", collections.OrderedDict({1: 2})),
        ("Y07:collections.Counter(empty)", collections.Counter()),
        ("Y08:collections.Counter", collections.Counter((1, 2))),
        ("Y09:collections.ChainMap", collections.ChainMap()),
        ("Y10:collections.ChainMap", collections.ChainMap({1: 2}, {2: 3})),
        ("Y11:collections.abc.Awaitable", collections.abc.Awaitable),
        ("Y12:collections.abc.Coroutine", collections.abc.Coroutine),
        ("Y13:collections.abc.AsyncIterable", collections.abc.AsyncIterable),
        ("Y14:collections.abc.AsyncIterator", collections.abc.AsyncIterator),
        ("Y15:collections.abc.AsyncGenerator", collections.abc.AsyncGenerator),
        ("Y16:collections.abc.Reversible", collections.abc.Reversible),
        ("Y17:collections.abc.Container", collections.abc.Container),
        ("Y18:collections.abc.Collection", collections.abc.Collection),
        ("Y19:collections.abc.Callable", collections.abc.Callable),
        ("Y20:collections.abc.Set", collections.abc.Set),
        ("Y21:collections.abc.MutableSet", collections.abc.MutableSet),
        ("Y22:collections.abc.Sequence", collections.abc.Sequence),
        ("Y23:collections.abc.MutableSequence", collections.abc.MutableSequence),
        ("Y24:collections.abc.ByteString", collections.abc.ByteString),
        ("Y25:collections.abc.MappingView", collections.abc.MappingView),
        ("Y26:collections.abc.KeysView", collections.abc.KeysView),
        ("Y27:collections.abc.ItemsView", collections.abc.ItemsView),
        ("Y28:collections.abc.ValuesView", collections.abc.ValuesView),
        ("Y29:contextlib.AbstractContextManager", contextlib.AbstractContextManager),
        ("Y30:contextlib.AbstractAsyncContextManager", contextlib.AbstractAsyncContextManager),

        ("Z01:decimal.localcontext", decimal.localcontext()),

- transformer les print en logging.
"""
import argparse
import configparser
import importlib
import numbers
import io
import re
import timeit

from rich import print as rprint

from linden.aboutproject import __projectname__, __version__

TIMEITNUMBER = 10

MODULES = {}

TMPFILE = "linden.tmp"
with open("linden.tmp", "w") as tmpfile:
    pass

PARSER = \
    argparse.ArgumentParser(description="Comparisons of different Python serializers",
                            epilog=f"{__projectname__}: {__version__}",
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('--version', '-v',
                    action='version',
                    version=f"{__projectname__}: {__version__}",
                    help="Show the version and exit")
PARSER.add_argument('--showwarmup',
                    action='store_true',
                    default=False,
                    help="Show warm up.")
PARSER.add_argument('--debug',
                    action='store_true',
                    default=False,
                    help="Show debug details.")
ARGS = PARSER.parse_args()

if ARGS.showwarmup or ARGS.debug:
    rprint(__projectname__, __version__)


class LindenError(Exception):
    """
    """


class SerializationResult:
    def __init__(self,
                 encoding_success=False,
                 encoding_time=None,
                 encodingstring_length=None,
                 decoding_success=False,
                 decoding_time=None,
                 identity=False):
        self.encoding_success = encoding_success
        self.encoding_time = encoding_time
        self.encodingstring_length = encodingstring_length
        self.decoding_success = decoding_success
        self.decoding_time = decoding_time
        self.identity = identity
    def __repr__(self):
        return f"{self.encoding_success=}; {self.encoding_time=}; {self.encodingstring_length=}; " \
            f"{self.decoding_success=}; {self.decoding_time=}; {self.identity=}"


class SerializerData:
    def __init__(self,
                 available,
                 func):
        self.available = available
        self.version = None
        self.func = func
    def __repr__(self):
        return f"{self.available=}; {self.version=}; {self.func=}"


def trytoimport(module_name):
    """
        trytoimport()

        Try to import <module_name> module.
        _______________________________________________________________________

        ARGUMENT:
        o  (str)module_name: the module to be imported

        RETURNED VALUE: (bool)success
    """
    res = True
    try:
        MODULES[module_name] = importlib.import_module(module_name)
        if ARGS.showwarmup or ARGS.debug:
            rprint(f"Module '{module_name}' successfully imported.")
    except ModuleNotFoundError:
        res = False
    return res


def _len(obj):
    if type(obj) is str:
        return len(bytes(obj, "utf-8"))
    return len(obj)


def read_inifile(filename="linden.ini"):
    # TODO : quid si le .ini est mal formé ?
    res = {"serializers": {},
           "data sets": {},
           "data": {},
           "tasks": {},
           }
    try:
        config = configparser.ConfigParser()
        config.read(filename)
    except configparser.DuplicateOptionError:
        # TODO : quelles autres exceptions sont-elles à prévoir ?
        pass

    for serializer in config['serializers']:
        res['serializers'][serializer] = config['serializers'].getboolean(serializer)
    for data in config['data']:
        res['data'][data] = config['data'].getboolean(data)
    for data_set in config['data sets']:
        res['data sets'][data_set] = \
            (data for data in config['data sets'][data_set].split(";") if data.strip() != "")
    for task in config['tasks']:
        res['tasks'][task] = config['tasks'][task]
    res['tasks']["tasks"] = (task for task in res['tasks']["tasks"].split(";") if task.strip() != "")

    if ARGS.showwarmup or ARGS.debug:
        rprint(f"Init file '{filename}' has been read.")

    return res


def serializer_iaswn(action="serialize",
                     obj=None):
    """
        serializer_iaswn()

        Serializer for the Iaswn module.

        Like every serializer_xxx() function:
        * None is returned if an error occured.
        * this function may return the version of the concerned module.
        * this function may try to encode/decode an <obj>ect.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["iaswn"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return module.__version__

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise LindenError(f"Unknown 'action' keyword '{action}'.")
        return None

    res = SerializationResult()

    _error = False
    try:
        _res = module.encode(obj)
        _timeit = timeit.Timer('module.encode(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encodingstring_length = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except module.IaswnError:
        _error = True

    if not _error:
        try:
            _res2 = module.decode(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.decode(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.identity = True
        except module.IaswnError:
            pass

    return res


def serializer_jsonpickle(action="serialize",
                          obj=None):
    """
        This function assumes that the module 'jsonpickle' has already be imported.
    """
    module = MODULES["jsonpickle"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise LindenError(f"Unknown 'action' keyword '{action}'.")
        return None

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encodingstring_length = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError:
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.identity = True
        except (TypeError, AttributeError):
            pass

    return res


def serializer_json(action="serialize",
                    obj=None):
    module = MODULES["json"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise LindenError(f"Unknown 'action' keyword '{action}'.")
        return None

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encodingstring_length = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError:
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.identity = True
        except (TypeError, AttributeError):
            pass

    return res


DATA = {
    "bool/false": True,
    "bool/true": True,

    "bytearray": bytearray(b"123"),
    "bytearray(empty)": bytearray(),

    "bytes": b"123",
    "bytes(empty)": b"",

    "complex": 1+2j,

    "dict(keys/bool)": {False:"False", True:"True"},
    "dict(keys/float)": {1.1:"value1.1", 2.2:"value2.2"},
    "dict(keys/int)": {0: "value0", 1:"value1", 2:"value2"},
    "dict(keys/str)": {"key1":"value1", "key2":"value2"},
    "dict(keys/str+subdicts)": {"key1":"value1", "key2":"value2", "key3": {"key4": "key4",}},

    "file descriptor": open(TMPFILE),

    "float": 1.1,

    "frozenset": frozenset(("1", "2",)),
    "frozenset(empty)": frozenset(),

    "function": _len,
    "function(python)": print,

    "imported module": timeit,
    "imported module(class)": timeit.Timer,
    "imported module(function)": timeit.timeit,

    "int": 1,

    "io.string": io.StringIO(),
    "io.string(empty)": io.StringIO().write("string"),

    "list": ["1", "2",],
    "list(empty)": [],
    "list(+sublists)": ["1", "2", ["3", ["4",]]],

    "memoryview": memoryview(b"123"),

    "none": None,

    "notimplemented": NotImplemented,

    "numbers(complex)": numbers.Complex,
    "numbers(integral)": numbers.Integral,
    "numbers(numbers)": numbers.Number(),
    "numbers(real)": numbers.Real,

    "pythonexception typeerror": TypeError,

    "range": range(1000),
    "range(empty)": range(0),

    "re.match": re.match(".*", "abc"),
    "re.match(+flags)": re.match(".*", "abc", re.M),

    "re.pattern(bytes)": re.compile(".*"),
    "re.pattern(str)": re.compile(b".*"),

    "set": set(("1", "2",)),
    "set(empty)": set(),

    "str": "abc",
    "str(empty)": "",
    "str(long)": "abhg12234"*10000,
    "str(non ascii characters)": "êł¹@"+chr(0x1234)+chr(0x12345),

    "tuple": ("1", "2",),
    "tuple(empty)": (),
    "tuple(+subtuples)": ("1", "2", ("3", ("4",))),
    }
if ARGS.debug:
    rprint("* known data:", list(DATA.keys()))

SERIALIZERS = {
    "iaswn": SerializerData(available=trytoimport("iaswn"),
                            func=serializer_iaswn),
    "json": SerializerData(available=trytoimport("json"),
                           func=serializer_json),
    "jsonpickle": SerializerData(available=trytoimport("jsonpickle"),
                                 func=serializer_jsonpickle),
    }
for serializer in SERIALIZERS:
    if SERIALIZERS[serializer].available:
        SERIALIZERS[serializer].version = SERIALIZERS[serializer].func("version")
if ARGS.debug:
    rprint("* known serializers:", SERIALIZERS)

CONFIG = read_inifile()

def get_data_selection(config):
    # TODO
    # pourquoi ne pas remplacer <config> par la globale CONFIG ?

    res = []

    if config["tasks"]["data selection"] == "all":
        res = config["data"]
    elif config["tasks"]["data selection"] == "only if yes":
        res = (data for data in config["data"] if config["data"][data])
    elif config["tasks"]["data selection"].startswith("data set/"):
        res = config["data sets"][config["tasks"]["data selection"]]
    else:
        # TODO
        # erreur: unknown order
        pass

    # TODO
    # vérification: est-ce que le contenu de <res> est connu de DATA ?
    _res = []
    for data in res:
        if data not in DATA:
            raise LindenError(f"! ERROR: unknown data '{data}'.")
        else:
            _res.append(data)
    return _res


def get_serializers_selection(config):
    """
    None if error
    """
    # TODO
    # pourquoi ne pas remplacer <config> par la globale CONFIG ?

    res = []

    if config["tasks"]["serializers selection"] == "all":
        res = config["serializers"]
    elif config["tasks"]["serializers selection"] == "only if yes":
        res = (serializer for serializer in config["serializers"] if config["serializers"][serializer])
    else:
        raise LindenError(f"ERROR: unknown serializer selection keyword '{config['tasks']['serializers selection']}'")
        return None

    # TODO
    # vérification: est-ce que le contenu de <res> est connu de SERIALIZERS ?
    _res = []
    for serializer in res:
        if serializer not in SERIALIZERS:
            raise LindenError(f"! ERROR: unknown serializer '{serializer}'.")
        else:
            _res.append(serializer)

    return _res

def main():
    try:
        for task in CONFIG["tasks"]["tasks"]:

            if task == "data selection * serializers selection":
                for data in get_data_selection(CONFIG):
                    for serializer in get_serializers_selection(CONFIG):
                        result = SERIALIZERS[serializer].func(action="serialize",
                                                          obj=DATA[data])
    except LindenError as exception:
        rprint(exception)

if __name__ == '__main__':
    main()
