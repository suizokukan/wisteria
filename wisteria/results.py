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
    results.py
"""
from dataclasses import dataclass

from rich import print as rprint
from rich.console import Console
from rich.progress_bar import ProgressBar

import wisteria.data
import wisteria.globs
from wisteria.globs import VERBOSITY_DETAILS, VERBOSITY_DEBUG
from wisteria.wisteriaerror import WisteriaError


@dataclass
class SerializerDataObj:
    """
        SerializerDataObj class

        Nothing but an easy way to set (serializer, dataobj)
    """
    serializer: str = None
    dataobj: str = None


def get_serializers_selection(serializer1,
                              serializer2):
    """
        get_serializers_selection()

        Return a tuple of all serializers defined by (str)<serializer1>, (str)<serializer1>.

        _______________________________________________________________________

        ARGUMENTS:
        o    <serializer1> : value returned by read_cmpstring()
        o    <serializer2> : value returned by read_cmpstring()

        RETURNED VALUE: a tuple of str
    """
    res = set()

    if serializer1 == "all":
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer1)

    if serializer2 == "all":
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer2)

    return tuple(res)


def get_data_selection(data,
                       config):
    """
        get_data_selection()

        Return a tuple of the data objects names selected by the <config>.

        _______________________________________________________________________

        ARGUMENTS:
        o  data:   (str)"all" or "ini"
        o  config: (dict) dict returned by read_cfgfile()

        RETURNED VALUE: (tuple) a tuple of (str)data keys
    """
    res = []

    if data == "all":
        res = tuple(wisteria.globs.DATA.keys())
    elif data == "ini":
        if config["data selection"]["data selection"] == "all":
            res = tuple(config["objects"].keys())
        elif config["data selection"]["data selection"] == "only if yes":
            res = (data_name for data_name in config["data objects"]
                   if config["data objects"][data_name])
        elif config["data selection"]["data selection"].startswith("data set/"):
            res = tuple(config["data sets"][config["data selection"]["data selection"]])
        else:
            raise WisteriaError(
                "Can't understand a value given to \\[data selection]'data selection': "
                f"what is '{config['data selection']['data selection']}' ? "
                "Known values are 'all', 'ini' and 'data set/xxx' "
                "where xxx is a string.")
    else:
        raise WisteriaError(
            "Can't understand a value given to the 'data' part in --cmp: "
            f"what is '{data}' ? "
            "Known values are 'all' and 'ini'. ")

    return res


class SerializationResults(dict):
    """
        SerializationResults class

        SerializationResults objects are used to store all results created during the tests.

        A SerializationResults object has the following structure:
                SerializationResults[(str)serializer][(str)dataobj] = SerializationResult object

        Do not forget to call .finish_initialization() once you have finished initializing <self>.

        _______________________________________________________________________

        o  (list)serializers        : list of str
        o  (list)dataobjs           : list of str
        o  (int) serializers_number : =len(self.serializers)
        o  (int) dataobjs_number    : =len(self.dataobjs)

        o  __init__(self)
        o  finish_initialization(self)
        o  _format_base100(bool_is_base100_reference, float_base100)
        o  _format_ratio(inttotal_and_floatratio)
        o  _format_stringlength(int_stringlength)
        o  _format_success(self, bool_success)
        o  _format_time(floattime)
        o  get_base(self, attribute)
        o  get_dataobjs_base(self, attribute)
        o  get_serializers_base(self, attribute)
        o  ratio_decoding_success(self, serializer=None, dataobj=None)
        o  ratio_encoding_success(self, serializer=None, dataobj=None)
        o  ratio_similarity(self, serializer=None, dataobj=None)
        o  repr_attr(self, serializer, dataobj, attribute_name, output="fmtstr")
        o  total_decoding_time(self, serializer=None, dataobj=None, output="fmtstr")
        o  total_encoding_plus_decoding_time(self, serializer=None, dataobj=None, output="fmtstr")
        o  total_encoding_strlen(self, serializer=None, dataobj=None, output="fmtstr")
        o  total_encoding_time(self, serializer=None, dataobj=None, output="fmtstr")
    """
    def __init__(self):
        """
            SerializationResults.__init__()
        """
        dict.__init__(self)
        self.serializers = []
        self.dataobjs = []
        self.serializers_number = None
        self.dataobjs_number = None
        self.halloffame = None  # TODO {'encoding_success' = [(0.24, 'marshal'), (0.22, 'pickle')]}
        self.overallscores = None

    def get_halloffame(self,
                       attribute,
                       index):
        """
        TODO
méthode pas à sa place, à déplacer plus bas dans le fichier
        """
        assert attribute in ('encoding_success',
                             'encoding_time',
                             'decoding_success',
                             'decoding_time',
                             'encoding_strlen',
                             'similarity')

        serializer = self.halloffame[attribute][index][1]
        value = self.halloffame[attribute][index][0]

        if attribute == 'encoding_success':
            return f"[yellow]{serializer}[/yellow] " \
                f"[{self.ratio_encoding_success(serializer=serializer)}]"

        if attribute == 'encoding_time':
            return f"[yellow]{serializer}[/yellow] " \
                f"[{self._format_time(value)}]"

        if attribute == 'decoding_success':
            return f"[yellow]{serializer}[/yellow] " \
                f"[{self.ratio_decoding_success(serializer=serializer)}]"

        if attribute == 'decoding_time':
            serializer = self.halloffame[attribute][index][1]
            return f"[yellow]{serializer}[/yellow] " \
                f"[{self._format_time(value)}]"

        if attribute == 'similarity':
            serializer = self.halloffame[attribute][index][1]
            return f"[yellow]{serializer}[/yellow] " \
                f"[{self.ratio_similarity(serializer=serializer)}]"

        if attribute == 'encoding_strlen':
            serializer = self.halloffame[attribute][index][1]
            return f"[yellow]{serializer}[/yellow] " \
                f"[{self._format_stringlength(value)}]"

        return None  # this line should never be executed.

    def get_overallscore_rank(self,
                              serializer):
        """
        TODO
pas à sa place
        """
        _rank = None

        # for rank, (score, _serializer) ...
        for rank, (_, _serializer) in enumerate(sorted(
                ((self.overallscores[serializer],
                  serializer) for serializer in self.serializers), reverse=True)):
            if serializer == _serializer:
                _rank = rank

        return _rank

    def comparison_inside_halloffame(self,
                                     serializer,
                                     attribute):
        """
        TODO
        pas à sa place
                par rapport à l'<attribute>, comment serializer est-il placé dans self.halloffame ?

        Renvoie les serializers mieux placés (=placés avant), les serializers moins bien placés
(=placés après)
        """
        _less = []
        _more = []

        before_serializer = False  # TODO deviendra True quand on sera tombé sur <serializer>
        for index in range(self.serializers_number):
            if self.halloffame[attribute][index][1] == serializer:
                before_serializer = True
            elif before_serializer:
                _less.append(self.halloffame[attribute][index][1])
            else:
                _more.append(self.halloffame[attribute][index][1])

        return _less, _more

    def finish_initialization(self):
        """
            SerializationResults.finish_initialization()

            Once the initialization of <self> is over, this method must be called to
            set self.self.serializers, self.dataobjs, self.serializers_number
            self.dataobjs_number, self.halloffame and self.overallscores

            ___________________________________________________________________

            RETURNED VALUE: (bool)success
        """
        self.serializers = sorted(self.keys())
        self.serializers_number = len(self.serializers)

        if self.serializers_number == 0:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint("ERRORID016: Incorrect data, there's no serializer.")
            return False

        first_serializer = tuple(self.serializers)[0]
        self.dataobjs = sorted(self[first_serializer].keys())
        self.dataobjs_number = len(self.dataobjs)

        self.halloffame = {
            "encoding_success": sorted(((self.ratio_encoding_success(serializer=serializer,
                                                                     output="value"),
                                         serializer) for serializer in self.serializers),
                                       reverse=True),
            "encoding_time": sorted(((self.total_encoding_time(serializer=serializer,
                                                               output="value"),
                                      serializer) for serializer in self.serializers),
                                    reverse=False),
            "decoding_success": sorted(((self.ratio_decoding_success(serializer=serializer,
                                                                     output="value"),
                                         serializer) for serializer in self.serializers),
                                       reverse=True),
            "decoding_time": sorted(((self.total_decoding_time(serializer=serializer,
                                                               output="value"),
                                      serializer) for serializer in self.serializers),
                                    reverse=False),
            "encoding_strlen": sorted(((self.total_encoding_strlen(serializer=serializer,
                                                                   output="value"),
                                        serializer) for serializer in self.serializers),
                                      reverse=False),
            "similarity": sorted(((self.ratio_similarity(serializer=serializer,
                                                         output="value"),
                                   serializer) for serializer in self.serializers),
                                 reverse=True),
            "encoding_plus_decoding_time": sorted(((self.total_encoding_time(serializer=serializer,
                                                                             output="value") +
                                                    self.total_decoding_time(serializer=serializer,
                                                                             output="value"),
                                                    serializer) for serializer in self.serializers),
                                                  reverse=False),
            }

        # TODO
        # calcul du overall score:
        #  si un serializer arrive #0 (première place) pour tel attribut,
        #     son score augmente de results.serializers_number-0.
        #  si un serializer arrive #1 (deuxième place) pour tel attribut,
        #     son score augmente de results.serializers_number-1.
        self.overallscores = {}
        for serializer in self.serializers:
            self.overallscores[serializer] = 0

            for attribute in ('encoding_plus_decoding_time',
                              'encoding_strlen',
                              'similarity',
                              ):
                for index in range(self.serializers_number):
                    if self.halloffame[attribute][index][1] == serializer:
                        self.overallscores[serializer] += self.serializers_number-index

        return True

    @staticmethod
    def _format_base100(bool_is_base100_reference,
                        float_base100):
        """
            SerializationResults._format_base100()
TODO
        """
        if float_base100 is None:
            return "[red](no data)[/red]"

        prefix = " "
        suffix = ""
        if bool_is_base100_reference:
            prefix = "[italic]*"
            suffix = "[/italic]"

        return f"{prefix}{float_base100:.2f}{suffix}"

    @staticmethod
    def _format_ratio(inttotal_and_floatratio):
        """
            SerializationResults._format_ratio()

            Format the input argument into a string. The input argument is an absolute
            (int)number and a (float)fraction, its ratio.
                ex: (3, 0.5) > "3 (50 %)"

            _______________________________________________________________

            ARGUMENT: (None|(int, float))inttotal_and_floatratio

            RETURNED VALUE: a formatted string representing the input argument.
        """
        if inttotal_and_floatratio != (None, None):
            return f"{inttotal_and_floatratio[0]} ({100*inttotal_and_floatratio[1]:.2f} %)"
        return "[red](no data)[/red]"

    @staticmethod
    def _format_stringlength(int_stringlength):
        """
            SerializationResults._format_stringlength()

            Format the input argument into a string. The input argument is a (int)number
            of characters
                ex: 3 > "3 chars"

            _______________________________________________________________

            ARGUMENT: (None|int)int_stringlength, a string number.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        if int_stringlength is None:
            return "[red](no data)[/red]"
        return f"{int_stringlength} chars"

    @staticmethod
    def _format_success(bool_success):
        """
            SerializationResults._format_success()

            Format the input argument into a string. The input argument is a (bool)success.
                ex: False > "NOT OK"

            _______________________________________________________________

            ARGUMENT: (bool)bool_success

            RETURNED VALUE: a formatted string representing the input argument.
        """
        if bool_success is None:
            return "[red](no data)[/red]"
        return "ok" if bool_success else "[red]NOT OK[/red]"

    @staticmethod
    def _format_time(floattime):
        """
            SerializationResults._format_time()

            Format the input argument into a string. The input argument is a (float)time laps.
                ex: 0.333345677 > "0.333345"
            _______________________________________________________________

            ARGUMENT: (None|float)floattime

            RETURNED VALUE: a formatted string representing the input argument.
        """
        if floattime is None:
            return "[red](no data)[/red]"
        return f"{floattime:.6f}"

    def get_base(self,
                 attribute):
        """
            SerializationResults.get_base()
TODO
        Return serializer+base data object for attribute <attribute>.

attribute: seulement 3 possibilités et non pas 5
        """
        assert attribute in ("encoding_time", "decoding_time", "encoding_strlen")

        if attribute == "encoding_time":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj].encoding_time:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        if attribute == "decoding_time":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj].decoding_time:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        if attribute == "encoding_strlen":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj].encoding_strlen:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        return None  # this line should never be executed.

    def get_dataobjs_base(self,
                          attribute):
        """
        TODO

        Return base data object for attribute <attribute>.
        """
        assert attribute in ("encoding_time", "decoding_time", "encoding_strlen")

        if attribute == "encoding_time":
            for dataobj in self.dataobjs:
                if self[self.serializers[0]][dataobj].encoding_success:
                    return dataobj
            return None

        if attribute == "encoding_strlen":
            for dataobj in self.dataobjs:
                if self[self.serializers[0]][dataobj].encoding_strlen:
                    return dataobj
            return None

        if attribute == "decoding_time":
            for dataobj in self.dataobjs:
                if self[self.serializers[0]][dataobj].decoding_success:
                    return dataobj
            return None

        return None  # this line should never be executed.

    def get_serializers_base(self,
                             attribute):
        """
        TODO

        Return base serializer for attribute <attribute>.
        """
        assert attribute in ("encoding_time", "decoding_time", "encoding_strlen")

        if attribute == "encoding_time":
            for serializer in self.serializers:
                if self[serializer][self.dataobjs[0]].encoding_success:
                    return serializer
            return None

        if attribute == "encoding_strlen":
            for serializer in self.serializers:
                if self[serializer][self.dataobjs[0]].encoding_strlen:
                    return serializer
            return None

        if attribute == "decoding_time":
            for serializer in self.serializers:
                if self[serializer][self.dataobjs[0]].decoding_success:
                    return serializer
            return None

        return None  # this line should never be executed.

    def ratio_decoding_success(self,
                               serializer=None,
                               dataobj=None,
                               output="fmtstr"):
        """
            SerializationResults.ratio_decoding_success()

            Compute and format the ratio of decoding success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
TODO : output
            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value')

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].decoding_success:
                    count += 1
            if output == "fmtstr":
                return SerializationResults._format_ratio((count, count/self.dataobjs_number))
            if output == "value":
                return count/self.dataobjs_number

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return SerializationResults._format_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj].decoding_success:
                count += 1
        if output == "fmtstr":
            return SerializationResults._format_ratio((count, count/self.serializers_number))
        if output == "value":
            return count/self.serializers_number

        return None  # this line should never be executed.

    def ratio_encoding_success(self,
                               serializer=None,
                               dataobj=None,
                               output="fmtstr"):
        """
            SerializationResults.ratio_encoding_success()

            Compute and format the ratio of encoding success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
        TODO output

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None
        assert output in ("fmtstr", "value")

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].encoding_success:
                    count += 1
            if output == "fmtstr":
                return SerializationResults._format_ratio((count, count/self.dataobjs_number))
            if output == "value":
                return count/self.dataobjs_number

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return SerializationResults._format_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj].encoding_success:
                count += 1
        if output == "fmtstr":
            return SerializationResults._format_ratio((count, count/self.serializers_number))
        if output == "value":
            return count/self.serializers_number

        return None  # this line should never be executed.

    def ratio_similarity(self,
                         serializer=None,
                         dataobj=None,
                         output="fmtstr"):
        """
            SerializationResults.ratio_similarity()

            Compute and/or format the ratio of similarity success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value')

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].similarity:
                    count += 1
            if output == "fmtstr":
                return SerializationResults._format_ratio((count, count/self.dataobjs_number))
            if output == "value":
                return count/self.dataobjs_number

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return SerializationResults._format_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj].similarity:
                count += 1

        if output == "fmtstr":
            return SerializationResults._format_ratio((count, count/self.serializers_number))
        if output == "value":
            return count/self.serializers_number

        return None  # this line should never be executed.

    def repr_attr(self,
                  serializer,
                  dataobj,
                  attribute_name,
                  output="fmtstr"):
        """
            SerializationResults.repr_attr()

            Format the value stored into self[serializer][dataobj].<attribute_name>.

            _______________________________________________________________
TODO
            ARGUMENT:
output="fmtstr" | "base100"

            RETURNED VALUE: a formatted string representing
                            self[serializer][dataobj].<attribute_name>
        """
        res = None  # unexpected result !

        # TODO
        # base100 n'existe que dans certains cas, il est donc impossible et inutile
        # de le calculer tout le temps.
        if output == "base100":
            base100_serializerdataobj = self.get_base(attribute=attribute_name)
            base100 = self[base100_serializerdataobj.serializer][base100_serializerdataobj.dataobj]

        if attribute_name == "decoding_success":
            if output == "fmtstr":
                res = SerializationResults._format_success(
                    self[serializer][dataobj].decoding_success)
            else:
                raise WisteriaError(
                    "Internal error. "
                    f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if attribute_name == "decoding_time":
            if output == "fmtstr":
                res = SerializationResults._format_time(
                    self[serializer][dataobj].decoding_time)
            else:
                # output == "base100"
                if self[serializer][dataobj].decoding_time is None:
                    res = "[red]no data[/red]"
                else:
                    res = SerializationResults._format_base100(
                        serializer == base100_serializerdataobj.serializer and
                        dataobj == base100_serializerdataobj.dataobj,
                        100*self[serializer][dataobj].decoding_time/base100.decoding_time)

        if attribute_name == "encoding_strlen":
            if output == "fmtstr":
                res = SerializationResults._format_stringlength(
                    self[serializer][dataobj].encoding_strlen)
            else:
                # output == "base100"
                if self[serializer][dataobj].encoding_strlen is None:
                    res = "[red]no data[/red]"
                else:
                    res = SerializationResults._format_base100(
                        serializer == base100_serializerdataobj.serializer and
                        dataobj == base100_serializerdataobj.dataobj,
                        100*self[serializer][dataobj].encoding_strlen/base100.encoding_strlen)

        if attribute_name == "encoding_time":
            if output == "fmtstr":
                res = SerializationResults._format_time(
                    self[serializer][dataobj].encoding_time)
            else:
                # output == "base100"
                if self[serializer][dataobj].encoding_time is None:
                    res = "[red]no data[/red]"
                else:
                    res = SerializationResults._format_base100(
                        serializer == base100_serializerdataobj.serializer and
                        dataobj == base100_serializerdataobj.dataobj,
                        100*self[serializer][dataobj].encoding_time/base100.encoding_time)

        if attribute_name == "encoding_success":
            if output == "fmtstr":
                res = SerializationResults._format_success(
                    self[serializer][dataobj].encoding_success)
            else:
                raise WisteriaError(
                    "Internal error. "
                    f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if attribute_name == "similarity":
            if output == "fmtstr":
                res = SerializationResults._format_success(
                    self[serializer][dataobj].similarity)
            else:
                raise WisteriaError(
                    "Internal error. "
                    f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {attribute_name=};")
        return res

    def total_decoding_time(self,
                            serializer=None,
                            dataobj=None,
                            output="fmtstr"):
        """
            SerializationResults.total_decoding_time()

            Compute and format the total decoding time used by a <serializer>
            OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)
            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_time(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].decoding_success:
                    total += self[serializer][_dataobj].decoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    serializer == self.get_serializers_base('decoding_time'),
                    100*total/self.total_decoding_time(
                        serializer=self.get_serializers_base('decoding_time'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                return SerializationResults._format_time(None)

            for _serializer in self:
                if self[_serializer][dataobj].decoding_success:
                    total += self[_serializer][dataobj].decoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    dataobj == self.get_dataobjs_base('decoding_time'),
                    100*total/self.total_decoding_time(
                        dataobj=self.get_dataobjs_base('decoding_time'),
                        output="value"))

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {output=};")
        return res

    def total_encoding_plus_decoding_time(self,
                                          serializer=None,
                                          dataobj=None,
                                          output="fmtstr"):
        """
            SerializationResults.total_encoding_plus_decoding_time()

            Compute and format the total encoding + decoding time used by a <serializer>
            OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    NOT "base100": formatted string based on a "base 100" value (str)

            RETURNED VALUE: a formatted string representing the input argument.
        """
        if output == "value":
            return self.total_encoding_time(serializer, dataobj, output) + \
                self.total_decoding_time(serializer, dataobj, output)
        if output == "fmtstr":
            return SerializationResults._format_time(
                self.total_encoding_time(serializer, dataobj, output='value') +
                self.total_decoding_time(serializer, dataobj, output='value'))

        raise WisteriaError("Internal error: the result could not be computed. "
                            f"{serializer=}; {dataobj=}; {output=};")

    def total_encoding_strlen(self,
                              serializer=None,
                              dataobj=None,
                              output="fmtstr"):
        """
            SerializationResults.total_encoding_strlen()

            Compute and format the total encoding string length created by a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_stringlength(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].encoding_strlen:
                    total += self[serializer][_dataobj].encoding_strlen
            if output == "value":
                res = total
            if output == "fmtstr":
                res = SerializationResults._format_stringlength(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    serializer == self.get_serializers_base('encoding_strlen'),
                    100*total/self.total_encoding_strlen(
                        serializer=self.get_serializers_base('encoding_strlen'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                return SerializationResults._format_stringlength(None)

            for _serializer in self:
                if self[_serializer][dataobj].encoding_strlen:
                    total += self[_serializer][dataobj].encoding_strlen
            if output == "value":
                res = total
            if output == "fmtstr":
                res = SerializationResults._format_stringlength(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    dataobj == self.get_dataobjs_base('encoding_strlen'),
                    100*total/self.total_encoding_strlen(
                        dataobj=self.get_dataobjs_base('encoding_strlen'),
                        output="value"))

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {output=};")
        return res

    def total_encoding_time(self,
                            serializer=None,
                            dataobj=None,
                            output="fmtstr"):
        """
            SerializationResults.total_encoding_time()

            Compute and format the total decoding time used by a <serializer>
            OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)
            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_time(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].encoding_success:
                    total += self[serializer][_dataobj].encoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    serializer == self.get_serializers_base('encoding_time'),
                    100*total/self.total_encoding_time(
                        serializer=self.get_serializers_base('encoding_time'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                res = SerializationResults._format_time(None)

            for _serializer in self:
                if self[_serializer][dataobj].encoding_success:
                    total += self[_serializer][dataobj].encoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    dataobj == self.get_dataobjs_base('encoding_time'),
                    100*total/self.total_encoding_time(
                        dataobj=self.get_dataobjs_base('encoding_time'),
                        output="value"))

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {output=};")
        return res


class SerializationResult:
    """
        SerializationResult class

        Class used to store tests results in a SerializationResults object.

        _______________________________________________________________________

        o  __init__(self)
        o  __repr__(self)
    """
    def __init__(self):
        """
            SerializationResult.__init__()
        """
        self.encoding_success = False
        self.encoding_time = None
        self.encoding_strlen = None
        self.decoding_success = False
        self.decoding_time = None
        self.similarity = False

    def __repr__(self):
        """
            SerializationResult.__repr__()
        """
        return f"{self.encoding_success=}; {self.encoding_time=}; {self.encoding_strlen=}; " \
            f"{self.decoding_success=}; {self.decoding_time=}; {self.similarity=}"


class SerializerData:
    """
        SerializerData class

        SerializerData are used to store infos. about serializers in the SERIALIZERS dict.

        _______________________________________________________________________

        o  __init__(self, human_name, internet, available, func)
        o  __repr__(self)
        o  checkup_repr(self)
        o  simple_repr(self)
    """
    def __init__(self,
                 human_name,
                 internet,
                 available,
                 func):
        """
            SerializerData.__init__()
        """
        self.human_name = human_name
        self.internet = internet
        self.available = available
        self.version = None
        self.func = func

    def __repr__(self):
        """
            SerializerData.__repr__()

            For the check up output, see .checkup_repr().
        """
        return f"{self.human_name=}; {self.internet=}; " \
            f"{self.available=}; {self.version=}; {self.func=}"

    def checkup_repr(self):
        """
            SerializerData.checkup_repr()

            Does the same as .__repr__() but for the check up output.
        """
        if self.available:
            return f"(available)     '{self.human_name}' ({self.version}), see {self.internet}."
        return f"(not available) '{self.human_name}' (see {self.internet})."

    def simple_repr(self):
        """
            SerializerData.simple_repr()

            Does the same as .__repr__() but for a simple output.
        """
        if self.available:
            return f"(available)     '{self.human_name}' ({self.version})"
        return f"(not available) '{self.human_name}'"


def compute_results(config,
                    serializer1,
                    serializer2,
                    cmpdata):
    """
        compute_results()

        Create a SerializationResults object and try to fill it with all
        required encodings/decodings defined by <serializer1>,
        <serializer2> and <cmpdata>.

        TODO : arguments

        RETURNED VALUE:    (SerializationResults, None) if no error occured
                        or (None, (int)exit_code) if an error occured
    """
    try:
        # serializers and data to be used through the tests:
        _serializers = get_serializers_selection(serializer1, serializer2)
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint("@ serializers to be used are: ", _serializers)
        _dataobjs = get_data_selection(cmpdata, config)
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint("@ data objs to be used are: ", _dataobjs)

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint("> Please wait until all required encodings/decodings have been computed.")

        results = SerializationResults()

        # (progress bar)
        # Please note that there can be NO progress bar if the debug mode is enabled:
        # the output can't display both correctly.
        if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
            console = Console()
            progressbar = ProgressBar(width=40, total=len(_serializers)*len(_dataobjs))
            console.show_cursor(False)
            progressbar_index = 0

        for serializer in _serializers:
            results[serializer] = {}
            for data_name in _dataobjs:
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    # (pimydoc)console messages
                    # ⋅- debug messages start with   @
                    # ⋅- info messages start with    >
                    # ⋅- error messages start with   ERRORIDXXX
                    # ⋅- checkup messages start with *
                    rprint(f"@ about to call function for serializer='{serializer}' "
                           f"and data name='{data_name}'")

                results[serializer][data_name] = wisteria.globs.SERIALIZERS[serializer].func(
                    action="serialize",
                    obj=wisteria.globs.DATA[data_name])

                # (progress bar)
                # Please note that there can be NO progress bar if the debug mode is enabled:
                # the output can't display both correctly.
                if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
                    progressbar_index += 1
                    progressbar.update(progressbar_index)
                    console.print(progressbar)
                    console.file.write("\r")

                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    # (pimydoc)console messages
                    # ⋅- debug messages start with   @
                    # ⋅- info messages start with    >
                    # ⋅- error messages start with   ERRORIDXXX
                    # ⋅- checkup messages start with *
                    rprint("@ result:", results[serializer][data_name])

        # (progress bar)
        # Please note that there can be NO progress bar if the debug mode is enabled:
        # the output can't display both correctly.
        if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
            console.show_cursor(True)

        if not results.finish_initialization():
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint("ERRORID015: incorrect data, the program has to stop.")

            # (pimydoc)exit codes
            # ⋅*  0: normal exit code
            # ⋅*  1: normal exit code after --checkup
            # ⋅*  2: normal exit code after --downloadconfigfile
            # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
            # ⋅* -2: error, ill-formed --cmp string
            # ⋅* -3: internal error, data can't be loaded
            return None, -3
        if results.dataobjs_number == 0:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            rprint("> No data to handle, the program can stop.")

            # (pimydoc)exit codes
            # ⋅*  0: normal exit code
            # ⋅*  1: normal exit code after --checkup
            # ⋅*  2: normal exit code after --downloadconfigfile
            # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
            # ⋅* -2: error, ill-formed --cmp string
            # ⋅* -3: internal error, data can't be loaded
            return None, 2

        return results, None

    except WisteriaError as exception:
        # (pimydoc)console messages
        # ⋅- debug messages start with   @
        # ⋅- info messages start with    >
        # ⋅- error messages start with   ERRORIDXXX
        # ⋅- checkup messages start with *
        rprint(f"> An error occured: {exception}")

        # (pimydoc)exit codes
        # ⋅*  0: normal exit code
        # ⋅*  1: normal exit code after --checkup
        # ⋅*  2: normal exit code after --downloadconfigfile
        # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
        # ⋅* -2: error, ill-formed --cmp string
        # ⋅* -3: internal error, data can't be loaded
        return None, -4  # TODO -4 n'est pas dans les exit codes
