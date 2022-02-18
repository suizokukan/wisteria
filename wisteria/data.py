#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/data.py

    All objects used as data by serializers are stored in the DATA dict.
    ___________________________________________________________________________

    o  anyfunc()
    o  check(config)
    o  constant_factory()
    o  init_data()
    o  works_as_expected(data_name, obj=None)
"""
import array
import calendar
import collections
import datetime
import decimal
import hashlib
import io
import numbers
import re
import time

import wisteria.globs
from wisteria.globs import TMPFILENAME, CWC_MODULES, VERBOSITY_DEBUG
from wisteria.classesexamples.simpleclasses import MetaClass, RegularClass
from wisteria.classesexamples.simpleclasses import RegularClassInheritedDict
from wisteria.classesexamples.simpleclasses import RegularClassInheritedList
from wisteria.cwc.cwc_utils import is_a_cwc_name
from wisteria.cwc.cwc_utils import modulefullrealname_to_modulerealname
from wisteria.cwc.cwc_utils import modulefullrealname_to_waemodulename
from wisteria.utils import trytoimport
from wisteria.wisteriaerror import WisteriaError
from wisteria.msg import msginfo, msgerror, msgdebug


def anyfunc():
    """
        anyfunc()

        Fake function used by the DATA dict.
    """


def check(config):
    """
        check()

        Check DATA/UNAVAILABLE_DATA consistency:
        o check #1:
          are all DATA/UNAVAILABLE_DATA keys defined in the configuration file, and vice-versa ?

        This function should be called after a call to read_cfgfile().
        ________________________________________________________________________

        ARGUMENT: (dict)config, the value returned by read_cfgfile()

        RETURNED VALUE: (bool)ok
                        If an error is detected, msgerror() will be called and the returned
                        value will be False.
    """
    res_ok = True

    # check #1:
    # are all DATA/UNAVAILABLE_DATA keys defined in the
    # configuration file, and vice-versa ?
    for dataobject_name in wisteria.globs.DATA:
        if dataobject_name not in config['data objects']:
            res_ok = False
            msgerror(f"(ERRORID037) '{dataobject_name}' is defined as a wisteria.globs.DATA key "
                     "but is not defined in the configuration file.")
    for dataobject_name in wisteria.globs.UNAVAILABLE_DATA:
        if dataobject_name not in config['data objects']:
            res_ok = False
            msgerror(f"(ERRORID038) '{dataobject_name}' is defined as "
                     "a wisteria.globs.UNAVAILABLE_DATA key "
                     "but is not defined in the configuration file.")
    for dataobject_name in config['data objects']:
        if dataobject_name not in wisteria.globs.DATA and \
           dataobject_name not in wisteria.globs.UNAVAILABLE_DATA:
            if is_a_cwc_name(dataobject_name):
                msginfo(f"cwc data object '{dataobject_name}' must be skipped. "
                        "This is normally not a problem: "
                        "it just means that a module has not be installed. "
                        "By example, if the Iaswn serializer has not been installed "
                        "you can't use the "
                        "'wisteria.cwc.pgnreader.cwc_iaswn.chessgames' data object.")
                # res_ok is NOT set to False: this situation is indeed normal.
                wisteria.globs.UNAVAILABLE_DATA[dataobject_name] = \
                    "this cwc module couldn't be imported: " \
                    "normally it's just because a module has not been installed. " \
                    "By example, if the Iaswn serializer has not been installed " \
                    "you can't use the " \
                    "'wisteria.cwc.pgnreader.cwc_iaswn.chessgames' data object."
            else:
                res_ok = False
                msgerror(f"(ERRORID039) '{dataobject_name}' is defined as a data key "
                         "in the configuration file "
                         "but is not defined as a wisteria.globs.DATA key "
                         "or as a wisteria.globs.UNAVAILABLE_DATA key.")
    return res_ok


def constant_factory(value):
    """
        constant_factory()

        Used to initialize defaultdict objects
    """
    return lambda: value


def init_data():
    """
        init_data()

        Initialize wisteria.globs.DATA.

        PLEASE SYNCHRONIZE THIS LIST OF DATA WITH THE LIST IN THE
        CONFIG FILE(S) AND THE LIST IN README.MD.

        (pimydoc)DATA format
        ⋅Initialized by data.py::init_data()
        ⋅
        ⋅- for Python basic types, DATA values are the real value:
        ⋅    e.g. DATA["bool/false"] = False
        ⋅- for cwc modules, DATA keys are the ini name (not the real name)
        ⋅  and DATA values are the real name:
        ⋅    e.g. DATA["wisteria.cwc.pgnreader.iaswn.ChessGames"] =
        ⋅        "wisteria.cwc.pgnreader.iaswn.chessgames"
        ⋅- for third party types, DATA values are the real value:
        ⋅    e.g. DATA["dateutil(parser.parse)"] = dateutil.parser.parse("2021-03-04")
    """
    # -------------------------------------------------------------------------
    # -------------------- 1/3 basic Python types -----------------------------
    # -------------------------------------------------------------------------
    wisteria.globs.DATA = {
        "array(b)":  array.array('b', (-1, 2)),
        "array(b/empty)": array.array('b'),
        "array(b_unsigned)": array.array('b', (1, 2)),
        "array(b_unsigned/empty)": array.array('B'),
        "array(u)": array.array('u', 'hello \u2641'),
        "array(u/empty)": array.array('u'),
        "array(h)": array.array('h', (-1, 2)),
        "array(h/empty)": array.array('h'),
        "array(h_unsigned)": array.array('H', (1, 2)),
        "array(h_unsigned/empty)": array.array('H'),
        "array(i)": array.array('i', (-1, 2)),
        "array(i/empty)": array.array('i'),
        "array(i_unsigned)": array.array('I', (1, 2)),
        "array(i_unsigned/empty)": array.array('I'),
        "array(l)": array.array('l', [-1, 2, 3, 4, 5]),
        "array(l/empty)": array.array('l'),
        "array(l_unsigned)": array.array('L', (1, 2)),
        "array(l_unsigned/empty)": array.array('L'),
        "array(q)": array.array('q', (-1, 2)),
        "array(q/empty)": array.array('q'),
        "array(q_unsigned)": array.array('Q', (1, 2)),
        "array(q_unsigned/empty)": array.array('Q'),
        "array(f)": array.array('f', (1.3, float('nan'))),
        "array(f/empty)": array.array('f'),
        "array(d)": array.array('d', [1.0, 2.0, 3.14]),
        "array(d/empty)": array.array('d'),

        "bool/false": False,
        "bool/true": True,

        "bytearray": bytearray(b"123"),
        "bytearray(empty)": bytearray(),

        "bytes": b"123",
        "bytes(empty)": b"",

        "calendar(calendar(3))": calendar.Calendar(3),

        "collections.chainmap(empty)": collections.ChainMap(),
        "collections.chainmap": collections.ChainMap({1: 2}, {2: 3}),
        "collections.counter(empty)": collections.Counter(),
        "collections.counter": collections.Counter((1, 2)),
        "collections.defaultdict(empty)": collections.defaultdict(),
        "collections.defaultdict(func)": collections.defaultdict(constant_factory('<missing>')),
        "collections.defaultdict(int)": collections.defaultdict(int, {"a": 1, "b": 10}),
        "collections.defaultdict(list)": collections.defaultdict(list, {1: [2, 3]}),
        "collections.defaultdict(none)": collections.defaultdict(None, {1: [2, 3]}),
        "collections.defaultdict(set)": collections.defaultdict(set, {1: set((2, 3))}),
        "collections.deque(empty)": collections.deque(),
        "collections.deque": collections.deque((1, 2)),
        "collections.ordereddict(empty)": collections.OrderedDict(),
        "collections.ordereddict": collections.OrderedDict({1: 2}),

        "complex": 1+2j,

        "datetime(datetime.datetime)": datetime.datetime(2001, 12, 1),
        "datetime(datetime.timedelta)":
        datetime.datetime(2001, 12, 1) - datetime.datetime(2000, 12, 1),

        "decimal(0.5)": decimal.Decimal(0.5),
        "decimal(1/7)": decimal.Decimal(1) / decimal.Decimal(7),
        "decimal(nan)": decimal.Decimal('NaN'),
        "decimal(-infinity)": decimal.Decimal("-Infinity"),
        "decimal(+infinity)": decimal.Decimal("+Infinity"),

        "dict(keys/bool)": {False: "False", True: "True"},
        "dict(keys/float)": {1.1: "value1.1", 2.2: "value2.2"},
        "dict(keys/int)": {0: "value0", 1: "value1", 2: "value2"},
        "dict(keys/str)": {"key1": "value1", "key2": "value2"},
        "dict(keys/str+subdicts)": {"key1": "value1", "key2": "value2", "key3": {"key4": "key4", }},

        # DATA["file descriptor"] contains a file descriptor which will be closed
        # by
        #   pylint: disable=consider-using-with
        "file descriptor": open(TMPFILENAME,
                                encoding="utf-8"),

        "float": 1.1,
        "float(nan)": float('nan'),

        "frozenset": frozenset(("1", "2",)),
        "frozenset(empty)": frozenset(),

        "function": anyfunc,
        "function(python)": print,

        "hashlib(hashlib.sha1)": hashlib.sha1(b"some string"),
        "hashlib(hashlib.sha224)": hashlib.sha224(b"some string"),
        "hashlib(hashlib.sha256)": hashlib.sha256(b"some string"),
        "hashlib(hashlib.sha384)": hashlib.sha384(b"some string"),
        "hashlib(hashlib.sha512)": hashlib.sha512(b"some string"),

        "imported module": re,
        "imported module(class)": re.Pattern,
        "imported module(function)": re.sub,

        "int": 1,

        "io.string": io.StringIO(),
        "io.string(empty)": io.StringIO().write("string"),

        "list": ["1", "2", ],
        "list(empty)": [],
        "list(+sublists)": ["1", "2", ["3", ["4", ]]],

        "metaclass": MetaClass(),

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

        "regularclass": RegularClass(),
        "regularclass(async_method)": RegularClass.async_method,
        "regularclass(class_method)": RegularClass.class_method,
        "regularclass(generator)": RegularClass.generator,
        "regularclass(method)": RegularClass.method,
        "regularclass(static_method)": RegularClass.static_method,
        "regularclassinheriteddict": RegularClassInheritedDict(),
        "regularclassinheritedlist": RegularClassInheritedList(),

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

        "time(time.time)": time.time(),

        "tuple": ("1", "2",),
        "tuple(empty)": (),
        "tuple(+subtuples)": ("1", "2", ("3", ("4",))),

        "type(str)": str,
        "type(type(str))": type(str),

        # (pimydoc)demonstration_dataobj_a5
        # ⋅Data object used to show the encoded strings created by the serializers,
        # ⋅see A5 report section.
        # ⋅
        # ⋅The choice of data is very small because all serializers must be able
        # ⋅to encode it. By example, no None object because of Amazon Ion Python.
        "demonstration_dataobj_a5": {"key1": "value1",
                                     "key2": ["1", 2, False, True, ],
                                     "key3": {"subkey1": "subvalue1", },
                                     "key4": [[], [[]]],
                                     },
    }

    # -------------------------------------------------------------------------
    # --------------------------- 2/3 cwc modules -----------------------------
    # -------------------------------------------------------------------------
    # (pimydoc)cwc modules names
    # ⋅
    # ⋅cwc modules names start with the "wisteria.cwc" string (cf is_a_cwc_name())
    # ⋅
    # ⋅moduleininame        : e.g. "wisteria.cwc.pgnreader.cwc_default.chessgames"
    # ⋅modulefullrealname   : e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames"
    # ⋅waemodulename        : e.g. "wisteria.cwc.pgnreader.works_as_expected"
    # ⋅classname            : e.g. "ChessGames" (NOT "chessgames")
    # ⋅modulerealname       : e.g. "wisteria.cwc.pgnreader.cwc_default"
    # ⋅
    # ⋅- `moduleininame` are defined in config file;
    # ⋅- conversion from `moduleininame` to `modulefullrealname` is defined in
    # ⋅  data.py:DATA and is made by function
    # ⋅  cwc_utils.py:moduleininame_to_modulefullrealname()
    # ⋅- conversion from `modulefullrealname` to `modulerealname` is made by
    # ⋅  function cwc_utils.py:modulefullrealname_to_modulerealname()
    # ⋅- DATA keys (for cwc modules) use `moduleininame`, NOT `modulefullrealname`
    for cwc_moduleininame, cwc_modulefullrealname in CWC_MODULES:
        # cwc_modulefullrealname: main module, like "wisteria.cwc.pgnreader.cwc_default.ChessGames"
        if not trytoimport(modulefullrealname_to_modulerealname(cwc_modulefullrealname)):
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"cwc module '{cwc_moduleininame}' ('{cwc_modulefullrealname}') "
                         "is defined in wisteria.globs.CWC_MODULES "
                         "but must be skipped (=added to wisteria.glob.UNAVAILABmsgdebugLE_DATA) "
                         "since module "
                         f"'{modulefullrealname_to_modulerealname(cwc_modulefullrealname)}' "
                         "can't be imported.")
        else:
            wisteria.globs.DATA[cwc_moduleininame] = cwc_modulefullrealname

        # wae (=works as expected module), like "wisteria.cwc.pgnreader.works_as_expected"
        if not trytoimport(modulefullrealname_to_waemodulename(cwc_modulefullrealname)):
            raise WisteriaError(
                "(ERRORID048) "
                "Internal error: can't import 'works_as_expected' cwc module "
                f"'{modulefullrealname_to_waemodulename(cwc_modulefullrealname)}' .")

    # -------------------------------------------------------------------------
    # --------------------------- 3/3 third party types -----------------------
    # -------------------------------------------------------------------------
    try:
        # The following 'import' statement has deliberately placed here and
        # not at the beginning of the file.
        #   pylint: disable=import-outside-toplevel
        #   pylint: disable=import-error
        import dateutil.parser
        wisteria.globs.DATA["dateutil(parser.parse)"] = dateutil.parser.parse("2021-03-04")
    except ImportError:
        wisteria.globs.UNAVAILABLE_DATA["dateutil(parser.parse)"] = "missing package: dateutil"

    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        msgdebug(f"wisteria.globs.DATA={wisteria.globs.DATA}")
        msgdebug(f"wisteria.globs.UNAVAILABLE_DATA={wisteria.globs.UNAVAILABLE_DATA}")


# I don't want to split this function into different parts:
#   pylint: disable=too-many-return-statements
def works_as_expected(data_name,
                      obj=None):
    """
        works_as_expected()

        works_as_expected() function for basic types defined DATA/UNAVAILABLE_DATA.
        _______________________________________________________________________

        (pimydoc)works_as_expected arguments and returned value
        ⋅All works_as_expected() functions are supposed to (1) say if <data_name> is in
        ⋅the scope of this function (2) and say if <obj> works as expected.
        ⋅
        ⋅ARGUMENTS:
        ⋅    o  data_name:   (str)data_name of the <obj>ect
        ⋅    o  obj:         (None or any object) object to be checked
        ⋅
        ⋅RETURNED VALUE:
        ⋅    (<obj> is None)     (bool)<data_name> is known
        ⋅    (<obj> is not None) <obj> works as expected.
    """
    if data_name == "list":
        if obj is None:
            # yes, this data_name is known:
            return True
        # <obj> is not None: does <obj> work as expected ?
        obj.clear()
        if len(obj) != 0:
            return False
        obj.append("1")
        obj.append("2")
        if obj[1] != "2":
            return False
        return True

    # there's no
    #       if data_name == "collections.defaultdict(func)"
    # since no serializer can transcode these objects; their validation is
    # by consequence useless.

    if data_name == "collections.defaultdict(int)":
        if obj is None:
            # yes, this data_name is known:
            return True
        # <obj> is not None: does <obj> work as expected ?
        obj.clear()
        try:
            obj[555] += 1
        except KeyError:
            return False
        return obj[555] == 1

    if data_name == "collections.defaultdict(list)":
        if obj is None:
            # yes, this data_name is known:
            return True
        # <obj> is not None: does <obj> work as expected ?
        obj.clear()
        try:
            obj[555].append("555")
        except KeyError:
            return False
        return obj[555] == ["555", ]

    if data_name == "collections.defaultdict(none)":
        if obj is None:
            # yes, this data_name is known:
            return True
        # <obj> is not None: does <obj> work as expected ?
        obj.clear()
        try:
            obj[555].append("555")
        except KeyError:
            return True
        return False

    if data_name == "collections.defaultdict(set)":
        if obj is None:
            # yes, this data_name is known:
            return True
        # <obj> is not None: does <obj> work as expected ?
        obj.clear()
        try:
            obj[555].add("555")
        except KeyError:
            return False
        return obj[555] == set(("555",))

    # unknown data_name:
    return False
