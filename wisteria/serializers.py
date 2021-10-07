#!/usr/bin/env python3.9
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
    Wisteria project : wisteria/serializers.py

    All known serializers are defined here, in the SERIALIZERS dict. Each serializer
    has its own serializer_xxx function.
    A reference to each module imported is added in the MODULES dict.

    ___________________________________________________________________________

    o  _len(obj)
    o  serializer_iaswn(action="serialize", obj=None, fingerprint="")
    o  serializer_json(action="serialize", obj=None, fingerprint="")
    o  serializer_jsonpickle(action="serialize", obj=None, fingerprint="")
    o  serializer_jsonpickle_keystrue(action="serialize", obj=None, fingerprint="")
    o  serializer_marshal(action="serialize", obj=None, fingerprint="")
    o  serializer_pickle(action="serialize", obj=None, fingerprint="")
    o  serializer_pyyaml(action="serialize", obj=None, fingerprint="")

    o  init_serializers()
"""
import sys
import timeit

import wisteria.globs
from wisteria.globs import TIMEITNUMBER, MODULES
from wisteria.globs import VERBOSITY_DEBUG
from wisteria.wisteriaerror import WisteriaError
from wisteria.utils import trytoimport
from wisteria.serializers_classes import SerializerData, SerializationResult
from wisteria.msg import msgdebug


def _len(obj):
    """
        _len()

        Return the length of <obj>

        _______________________________________________________________________

        ARGUMENT: (bytes|str)<obj>

        RETURNED VALUE: the length of <obj>
    """
    if isinstance(obj, str):
        return len(bytes(obj, "utf-8"))
    return len(obj)


def serializer_iaswn(action="serialize",
                     obj=None,
                     fingerprint=""):
    """
        serializer_iaswn()

        Serializer for the Iaswn module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action:      (str) either "version" either "serialize"
        o  obj:         the object to be serialized
        o  fingerprint: a string describing the operation (usefull to debug)

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
        raise WisteriaError(f"(ERRORID030) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.encode(obj)
        _timeit = timeit.Timer('module.encode(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except module.IaswnError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.decode(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.decode(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except module.IaswnError as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    return res


def serializer_json(action="serialize",
                    obj=None,
                    fingerprint=""):
    """
        serializer_json()

        Serializer for the json module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized
        o  fingerprint: a string describing the operation (usefull to debug)

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["json"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise WisteriaError(f"(ERRORID031) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    return res


def serializer_jsonpickle(action="serialize",
                          obj=None,
                          fingerprint=""):
    """
        serializer_jsonpickle()

        Serializer for the jsonpickle module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized
        o  fingerprint: a string describing the operation (usefull to debug)

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["jsonpickle"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise WisteriaError(f"(ERRORID032) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    return res


def serializer_jsonpickle_keystrue(action="serialize",
                                   obj=None,
                                   fingerprint=""):
    """
        serializer_jsonpickle_keystrue()

        Serializer for the jsonpickle module (keys=True).

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized
        o  fingerprint: a string describing the operation (usefull to debug)

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["jsonpickle"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise WisteriaError(f"(ERRORID042) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj, keys=True)
        _timeit = timeit.Timer('module.dumps(obj, keys=True)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res, keys=True)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res, keys=True)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    return res


def serializer_marshal(action="serialize",
                       obj=None,
                       fingerprint=""):
    """
        serializer_marshal()

        Serializer for the marshal module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized
        o  fingerprint: a string describing the operation (usefull to debug)

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["marshal"]

    if action == "version":
        return f"version {module.version}; (Python version) {sys.version.replace(chr(0x0A), '- ')}"

    if action != "serialize":
        raise WisteriaError(f"(ERRORID033) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except (TypeError, ValueError) as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    return res


def serializer_pickle(action="serialize",
                      obj=None,
                      fingerprint=""):
    """
        serializer_pickle()

        Serializer for the pickle module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized
        o  fingerprint: a string describing the operation (usefull to debug)

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["pickle"]

    if action == "version":
        return f"(Python version) {sys.version.replace(chr(0x0A), '- ')}"

    if action != "serialize":
        raise WisteriaError(f"(ERRORID034) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    return res


def serializer_pyyaml(action="serialize",
                      obj=None,
                      fingerprint=""):
    """
        serializer_pyyaml()

        Serializer for the pyyaml module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized
        o  fingerprint: a string describing the operation (usefull to debug)

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["yaml"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise WisteriaError(f"(ERRORID044) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dump(obj, Dumper=module.Dumper)
        _timeit = timeit.Timer('module.dump(obj, Dumper=module.Dumper)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except (ValueError, TypeError) as error:
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"[{fingerprint}] '{module}': encoding failed ({error})")
        _error = True

    if not _error:
        try:
            _res2 = module.load(_res, Loader=module.Loader)
            res.decoding_success = True
            _timeit = timeit.Timer("module.load(_res, Loader=module.Loader)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (module.constructor.ConstructorError, ValueError) as error:
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"[{fingerprint}] '{module}': decoding failed ({error})")
            res = None

    return res


def init_serializers():
    """
        init_serializers()

        Initialize wisteria.globs.SERIALIZERS
    """
    for serializerdata in (
            SerializerData(
                name="iaswn",
                module_name="iaswn",
                human_name="Iaswn",
                internet="https://github.com/suizokukan/iaswn",
                func=serializer_iaswn),
            SerializerData(
                name="json",
                module_name="json",
                human_name="json",
                internet="https://docs.python.org/3/library/json.html",
                func=serializer_json),
            SerializerData(
                name="jsonpickle",
                module_name="jsonpickle",
                human_name="jsonpickle",
                internet="https://jsonpickle.github.io/",
                func=serializer_jsonpickle),
            SerializerData(
                name="jsonpickle_keystrue",
                module_name="jsonpickle",
                human_name="jsonpickle(keys=True)",
                internet="https://jsonpickle.github.io/",
                func=serializer_jsonpickle_keystrue),
            SerializerData(
                name="marshal",
                module_name="marshal",
                human_name="marshal",
                internet="https://docs.python.org/3/library/marshal.html#module-marshal",
                func=serializer_marshal),
            SerializerData(
                name="pickle",
                module_name="pickle",
                human_name="pickle",
                internet="https://docs.python.org/3/library/pickle.html",
                func=serializer_pickle),
            SerializerData(
                name="pyyaml",
                module_name="yaml",
                human_name="pyyaml",
                internet="https://pyyaml.org/",
                func=serializer_pyyaml),
            ):
        if trytoimport(serializerdata.module_name):
            wisteria.globs.SERIALIZERS[serializerdata.name] = serializerdata
            wisteria.globs.SERIALIZERS[serializerdata.name].version = serializerdata.func("version")
        else:
            wisteria.globs.UNAVAILABLE_SERIALIZERS[serializerdata.name] = serializerdata
