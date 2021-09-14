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


class SerializationResults(dict):
    """
        SerializationResults class

        SerializationResults objects are used to store all results created during the tests.

        A SerializationResults object has the following structure:
                SerializationResults[(str)serializer][(str)data_obj] = SerializationResult object

        Do not forget to call ._finish_initialization() once you have finished initializing <self>.

        _______________________________________________________________________

        o  def __init__(self)
        o  def _finish_initialization(self)
        o  def _format_ratio(self, inttotal_and_floatratio)
        o  def _format_stringlength(self, int_stringlength)
        o  def _format_success(self, bool_success)
        o  def _format_time(self, floattime)
        o  def ratio_decoding_success(self, serializer=None, data_obj=None)
        o  def ratio_encoding_success(self, serializer=None, data_obj=None)
        o  def ratio_identify(self, serializer=None, data_obj=None)
        o  def repr_attr(self, serializer, data_obj, attribute_name)
        o  def total_decoding_time(self, serializer=None, data_obj=None)
        o  def total_encoding_stringlength(self, serializer=None, data_obj=None)
        o  def total_encoding_time(self, serializer=None, data_obj=None)
    """
    def __init__(self):
        """
            SerializationResults.__init__()
        """
        dict.__init__(self)
        self.serializers_number = None
        self.data_objs_number = None

    def _finish_initialization(self):
        """
            SerializationResults._finish_initialization()

            Once the initialization of <self> is over, this method must be called to
            set self.serializers_number and self.data_objs_number.
        """
        self.serializers_number = len(self)
        if self.serializers_number > 0:
            first_serializer = tuple(self.keys())[0]
            self.data_objs_number = len(self[first_serializer])

    def _format_ratio(self,
                      inttotal_and_floatratio):
        """
            SerializationResults._format_ratio()

            Format the input argument into a string. The input argument is an absolute
            (int)number and a (float)fraction, its ratio.
                ex: (3, 0.5) > "3 (50 %)"

            _______________________________________________________________

            ARGUMENT: (int, float)inttotal_and_floatratio

            RETURNED VALUE: a formatted string representing the input argument.
        """
        if inttotal_and_floatratio != (None, None):
            return f"{inttotal_and_floatratio[0]} ({100*inttotal_and_floatratio[1]:.2f} %)"
        return "(no data)"

    def _format_stringlength(self,
                             int_stringlength):
        """
            SerializationResults.

            Format the input argument into a string. The input argument is a (int)number
            of characters
                ex: 3 > "3 chars"

            _______________________________________________________________

            ARGUMENT: (int)int_stringlength, a string number.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        return f"{int_stringlength} chars"

    def _format_success(self,
                        bool_success):
        """
            SerializationResults.

            Format the input argument into a string. The input argument is a (bool)success.
                ex: False > "NOT OK"

            _______________________________________________________________

            ARGUMENT: (bool)bool_success

            RETURNED VALUE: a formatted string representing the input argument.
        """
        return "ok" if bool_success else "[red]NOT OK[/red]"

    def _format_time(self,
                     floattime):
        """
            SerializationResults.

            Format the input argument into a string. The input argument is a (float)time laps.
                ex: 0.333345677 > "0.333345"
            _______________________________________________________________

            ARGUMENT: (float)floattime

            RETURNED VALUE: a formatted string representing the input argument.
        """
        return f"{floattime:.6f}"

    def ratio_decoding_success(self,
                               serializer=None,
                               data_obj=None):
        """
            SerializationResults.

            Compute and format the ratio of decoding success for a <serializer>
            OR for a <data_obj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>data_obj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <data_obj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or data_obj is None

        count = 0  # number of serializers or data_objs that are taken in account.

        if serializer is not None:
            if self.serializers_number == 0:
                return self._format_ratio(None, None)

            for data_obj in self[serializer]:
                if self[serializer][data_obj].decoding_success:
                    count += 1
            return self._format_ratio((count, count/self.data_objs_number))

        if data_obj is not None:
            if self.data_objs_number == 0:
                return self._format_ratio(None, None)

            for serializer in self:
                if self[serializer][data_obj].decoding_success:
                    count += 1
            return self._format_ratio((count, count/self.data_objs_number))

    def ratio_encoding_success(self,
                               serializer=None,
                               data_obj=None):
        """
            SerializationResults.

            Compute and format the ratio of encoding success for a <serializer>
            OR for a <data_obj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>data_obj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <data_obj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or data_obj is None

        count = 0  # number of serializers or data_objs that are taken in account.

        if serializer is not None:
            if self.serializers_number == 0:
                return self._format_ratio((None, None))

            for data_obj in self[serializer]:
                if self[serializer][data_obj].encoding_success:
                    count += 1
            return self._format_ratio((count, count/self.serializers_number))

        if data_obj is not None:
            if self.data_objs_number == 0:
                return self._format_ratio((None, None))

            for serializer in self:
                if self[serializer][data_obj].encoding_success:
                    count += 1
            return self._format_ratio((count, count/self.serializers_number))

    def ratio_identity(self,
                       serializer=None,
                       data_obj=None):
        """
            SerializationResults.

            Compute and format the ratio of identity success for a <serializer>
            OR for a <data_obj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>data_obj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <data_obj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or data_obj is None

        count = 0  # number of serializers or data_objs that are taken in account.

        if serializer is not None:
            if self.serializers_number == 0:
                return self._format_ratio((None, None))

            for data_obj in self[serializer]:
                if self[serializer][data_obj].identity:
                    count += 1
            return self._format_ratio((count, count/self.data_objs_number))

        if data_obj is not None:
            if self.data_objs_number == 0:
                return self._format_ratio((None, None))

            for serializer in self:
                if self[serializer][data_obj].identity:
                    count += 1
            return self._format_ratio((count, count/self.data_objs_number))

    def repr_attr(self,
                  serializer,
                  data_obj,
                  attribute_name):
        """
            SerializationResults.

            Format the value stored into self[serializer][data_obj].<attribute_name>.

            _______________________________________________________________

            ARGUMENT:

            RETURNED VALUE: a formatted string representing
                            self[serializer][data_obj].<attribute_name>
        """
        if attribute_name == "decoding_success":
            return self._format_success(self[serializer][data_obj].decoding_success)
        if attribute_name == "decoding_time":
            return self._format_time(self[serializer][data_obj].decoding_time)
        if attribute_name == "encoding_stringlength":
            return self._format_stringlength(self[serializer][data_obj].encoding_stringlength)
        if attribute_name == "encoding_time":
            return self._format_time(self[serializer][data_obj].encoding_time)
        if attribute_name == "encoding_success":
            return self._format_success(self[serializer][data_obj].encoding_success)
        if attribute_name == "identity":
            return self._format_success(self[serializer][data_obj].identity)

    def total_decoding_time(self,
                            serializer=None,
                            data_obj=None):
        """
            SerializationResults.

            Compute and format the total decoding time used by a <serializer>
            OR by a <data_obj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>data_obj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <data_obj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or data_obj is None

        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return self._format_time(None)

            for data_obj in self[serializer]:
                if self[serializer][data_obj].decoding_success:
                    total += self[serializer][data_obj].decoding_time
            return self._format_time(total)

        if data_obj is not None:
            if self.data_objs_number == 0:
                return self._format_time(None)

            for serializer in self:
                if self[serializer][data_obj].decoding_success:
                    total += self[serializer][data_obj].decoding_time
            return self._format_time(total)

    def total_encoding_stringlength(self,
                                    serializer=None,
                                    data_obj=None):
        """
            SerializationResults.

            Compute and format the total encoding string length created by a <serializer>
            OR for a <data_obj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>data_obj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <data_obj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or data_obj is None

        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return self._format_stringlength(None)

            for data_obj in self[serializer]:
                if self[serializer][data_obj].encoding_stringlength:
                    total += self[serializer][data_obj].encoding_stringlength
            return self._format_stringlength(total)

        if data_obj is not None:
            if self.data_objs_number == 0:
                return self._format_stringlength(None)

            for serializer in self:
                if self[serializer][data_obj].encoding_stringlength:
                    total += self[serializer][data_obj].encoding_stringlength
            return self._format_stringlength(total)

    def total_encoding_time(self,
                            serializer=None,
                            data_obj=None):
        """
            SerializationResults.

            Compute and format the total decoding time used by a <serializer>
            OR by a <data_obj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>data_obj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <data_obj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or data_obj is None

        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return self._format_time(None)

            for data_obj in self[serializer]:
                if self[serializer][data_obj].encoding_success:
                    total += self[serializer][data_obj].encoding_time
            return self._format_time(total)

        if data_obj is not None:
            if self.data_objs_number == 0:
                return self._format_time(None)

            for serializer in self:
                if self[serializer][data_obj].encoding_success:
                    total += self[serializer][data_obj].encoding_time
            return self._format_time(total)


class SerializationResult:
    def __init__(self,
                 encoding_success=False,
                 encoding_time=None,
                 encoding_stringlength=None,
                 decoding_success=False,
                 decoding_time=None,
                 identity=False):
        self.encoding_success = encoding_success
        self.encoding_time = encoding_time
        self.encoding_stringlength = encoding_stringlength
        self.decoding_success = decoding_success
        self.decoding_time = decoding_time
        self.identity = identity
    def __repr__(self):
        return f"{self.encoding_success=}; {self.encoding_time=}; {self.encoding_stringlength=}; " \
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
        return f"{self.human_name=}; {self.internet=}; {self.available=}; {self.version=}; {self.func=}"
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
        res.encoding_stringlength = _len(_res)
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
        res.encoding_stringlength = _len(_res)
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
