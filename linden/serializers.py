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
    serializers.py

    All known serializers are defined here, in the SERIALIZERS dict. Each serializer
    has its own serializer_xxx function.
    A reference to each module imported is added in the MODULES dict.

    ___________________________________________________________________________

    * MODULES dict

    *  trytoimport(module_name)
    *  _len(obj)

    * SerializationResult class
    * SerializationData class

    * serializer_iaswn(action="serialize", obj=None):
    * serializer_jsonpickle(action="serialize", obj=None):

    * SERIALIZERS dict
"""
import importlib
import timeit

from rich import print as rprint

from linden.globs import VERBOSITY_MINIMAL, VERBOSITY_NORMAL, VERBOSITY_DETAILS, VERBOSITY_DEBUG
from linden.globs import ARGS, TIMEITNUMBER

MODULES = {}


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
        if ARGS.verbosity>=VERBOSITY_DETAILS:
            rprint(f"Module '{module_name}' successfully imported.")
    except ModuleNotFoundError:
        res = False
    return res


def _len(obj):
    if type(obj) is str:
        return len(bytes(obj, "utf-8"))
    return len(obj)


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
                 human_name,
                 internet,
                 available,
                 func):
        self.human_name = human_name
        self.internet = internet
        self.available = available
        self.version = None
        self.func = func
    def __repr__(self):
        return f"{human_name=}; {internet=}; {self.available=}; {self.version=}; {self.func=}"
    def checkup_repr(self):
        if self.available:
            return f"(available)     '{self.human_name}' ({self.version}), see {self.internet}."
        return f"(not available) '{self.human_name}' (see {self.internet})."


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
        serializer_jsonpickle()

        Serializer for the jsonpickle module.

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


SERIALIZERS = {
    "iaswn": SerializerData(human_name="Iaswn",
                            internet="https://github.com/suizokukan/iaswn",
                            available=trytoimport("iaswn"),
                            func=serializer_iaswn),
    "jsonpickle": SerializerData(human_name="jsonpickle",
                                 internet="https://jsonpickle.github.io/",
                                 available=trytoimport("jsonpickle"),
                                 func=serializer_jsonpickle),
    }
for serializer in SERIALIZERS:
    if SERIALIZERS[serializer].available:
        SERIALIZERS[serializer].version = SERIALIZERS[serializer].func("version")
