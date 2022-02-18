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
    Wisteria project : wisteria/cwc/cwc_utils.py

    Various functions to be used with cwc modules.


    (pimydoc)cwc modules names
    ⋅
    ⋅cwc modules names start with the "wisteria.cwc" string (cf is_a_cwc_name())
    ⋅
    ⋅moduleininame        : e.g. "wisteria.cwc.pgnreader.cwc_default.chessgames"
    ⋅modulefullrealname   : e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames"
    ⋅waemodulename        : e.g. "wisteria.cwc.pgnreader.works_as_expected"
    ⋅classname            : e.g. "ChessGames" (NOT "chessgames")
    ⋅modulerealname       : e.g. "wisteria.cwc.pgnreader.cwc_default"
    ⋅
    ⋅- `moduleininame` are defined in config file;
    ⋅- conversion from `moduleininame` to `modulefullrealname` is defined in
    ⋅  data.py:DATA and is made by function
    ⋅  cwc_utils.py:moduleininame_to_modulefullrealname()
    ⋅- conversion from `modulefullrealname` to `modulerealname` is made by
    ⋅  function cwc_utils.py:modulefullrealname_to_modulerealname()
    ⋅- DATA keys (for cwc modules) use `moduleininame`, NOT `modulefullrealname`
    ___________________________________________________________________________

    o  are_two_cwc_variants_of_the_same_cwc(name1, name2)
    o  count_dataobjs_number_without_cwc_variant(dataobjs)
    o  is_a_cwc_name(data_object_name)
    o  is_this_an_appropriate_module_for_serializer(data_name__module, serializer)
    o  modulefullrealname_to_classname(modulefullrealname)
    o  modulefullrealname_to_modulerealname(modulefullrealname)
    o  modulefullrealname_to_waemodulename(modulefullrealname)
    o  moduleininame_to_modulefullrealname(moduleininame)
    o  select__works_as_expected__function(data_object_name)
    o  serializer_is_compatible_with_dataobj(serializer, dataobj)
    o  shorten_cwc_name(cwc_name)
"""
import wisteria.globs


def are_two_cwc_variants_of_the_same_cwc(name1,
                                         name2):
    """
        are_two_cwc_variants_of_the_same_cwc()

        Return True if <name1> and <name2> are two cwc names and if the third element
        (=name.split(".")[2]) is the same, as in:
                'wisteria.cwc.pgnreader.cwc_default.ChessGames' and
                'wisteria.cwc.pgnreader.iaswn.ChessGames'
                ... where name.split(".")[2] is 'pgnreader'
    """
    if name1 == name2:
        return False
    if not is_a_cwc_name(name1):
        return False
    if not is_a_cwc_name(name2):
        return False

    return name1.split(".")[2] == name2.split(".")[2]


def count_dataobjs_number_without_cwc_variant(dataobjs):
    """
        count_dataobjs_number_without_cwc_variant()

        Return the number of data objects in <dataobjs> that are not a cwc variant
        of another data object in <dataobjs>.

        Unittest: CWCUtils.test_count_dataobjs_number_without_cwc_variant().

        if <dataobjs> is something like:
            {"wisteria.cwc.pgnreader.cwc_default.ChessGames": None,
             "wisteria.cwc.pgnreader.iaswn.ChessGames": None,
             "wisteria.cwc.pgnreader.xyz.ChessGames": None,
             "int": None,}      > the method will return 2
        _______________________________________________________________________

        ARGUMENT: (set of str)<dataobjs>, e.g.
            {'wisteria.cwc.pgnreader.cwc_default.ChessGames',
             'wisteria.cwc.pgnreader.iaswn.ChessGames'}

        RETURNED VALUE: (int)the number of data objects in <dataobjs> that are not
                        a cwc variant of another data object in <dataobjs>
    """
    cwc_variants = []
    res = 0
    for dataobj in dataobjs:
        if not is_a_cwc_name(dataobj):
            res += 1
        else:
            ok = True
            for cwc_variant in cwc_variants:
                if are_two_cwc_variants_of_the_same_cwc(cwc_variant,
                                                        dataobj):
                    ok = False
                    break
            if ok:
                res += 1
                cwc_variants.append(dataobj)

    return res


def is_a_cwc_name(data_object_name):
    """
        is_a_cwc_name()

        Return True if <data_object_name> starts with "wisteria.cwc".


        (pimydoc)cwc modules names
        ⋅
        ⋅cwc modules names start with the "wisteria.cwc" string (cf is_a_cwc_name())
        ⋅
        ⋅moduleininame        : e.g. "wisteria.cwc.pgnreader.cwc_default.chessgames"
        ⋅modulefullrealname   : e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames"
        ⋅waemodulename        : e.g. "wisteria.cwc.pgnreader.works_as_expected"
        ⋅classname            : e.g. "ChessGames" (NOT "chessgames")
        ⋅modulerealname       : e.g. "wisteria.cwc.pgnreader.cwc_default"
        ⋅
        ⋅- `moduleininame` are defined in config file;
        ⋅- conversion from `moduleininame` to `modulefullrealname` is defined in
        ⋅  data.py:DATA and is made by function
        ⋅  cwc_utils.py:moduleininame_to_modulefullrealname()
        ⋅- conversion from `modulefullrealname` to `modulerealname` is made by
        ⋅  function cwc_utils.py:modulefullrealname_to_modulerealname()
        ⋅- DATA keys (for cwc modules) use `moduleininame`, NOT `modulefullrealname`
        _______________________________________________________________________

        ARGUMENT: (str)data_object_name, the string to be checked.

        RETURNED VALUE: (bool)True if <data_object_name> is a cwc string.
    """
    return data_object_name.startswith("wisteria.cwc")


def is_this_an_appropriate_module_for_serializer(data_name__module,
                                                 serializer):
    """
        is_this_an_appropriate_module_for_serializer()

        Return True if <data_name__module> is a module appropriate to <serializer>:
            e.g. if data_name__module is "cwc.pgnreader.cwc_default" and
                 if SERIALIZERS[serializer].cwc is "default" > True

            e.g. if data_name__module is "cwc.pgnreader.cwc_default" and
                 if SERIALIZERS[serializer].cwc is "iaswn" > False - we skip.


        (pimydoc)cwc modules names
        ⋅
        ⋅cwc modules names start with the "wisteria.cwc" string (cf is_a_cwc_name())
        ⋅
        ⋅moduleininame        : e.g. "wisteria.cwc.pgnreader.cwc_default.chessgames"
        ⋅modulefullrealname   : e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames"
        ⋅waemodulename        : e.g. "wisteria.cwc.pgnreader.works_as_expected"
        ⋅classname            : e.g. "ChessGames" (NOT "chessgames")
        ⋅modulerealname       : e.g. "wisteria.cwc.pgnreader.cwc_default"
        ⋅
        ⋅- `moduleininame` are defined in config file;
        ⋅- conversion from `moduleininame` to `modulefullrealname` is defined in
        ⋅  data.py:DATA and is made by function
        ⋅  cwc_utils.py:moduleininame_to_modulefullrealname()
        ⋅- conversion from `modulefullrealname` to `modulerealname` is made by
        ⋅  function cwc_utils.py:modulefullrealname_to_modulerealname()
        ⋅- DATA keys (for cwc modules) use `moduleininame`, NOT `modulefullrealname`
        _______________________________________________________________________

        ARGUMENTS:
        o  (str)data_name__module
        o  (str)serializer

        RETURNED VALUE: (bool)True if <data_name__module> if appropriate to
                        <serializer>
    """
    return data_name__module.endswith(wisteria.globs.SERIALIZERS[serializer].cwc)


def modulefullrealname_to_classname(modulefullrealname):
    """
        modulefullrealname_to_classname()

        Convert module full real name into class name, something like:
                "wisteria.cwc.pgnreader.cwc_default.ChessGames" > "ChessGames"


        (pimydoc)cwc modules names
        ⋅
        ⋅cwc modules names start with the "wisteria.cwc" string (cf is_a_cwc_name())
        ⋅
        ⋅moduleininame        : e.g. "wisteria.cwc.pgnreader.cwc_default.chessgames"
        ⋅modulefullrealname   : e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames"
        ⋅waemodulename        : e.g. "wisteria.cwc.pgnreader.works_as_expected"
        ⋅classname            : e.g. "ChessGames" (NOT "chessgames")
        ⋅modulerealname       : e.g. "wisteria.cwc.pgnreader.cwc_default"
        ⋅
        ⋅- `moduleininame` are defined in config file;
        ⋅- conversion from `moduleininame` to `modulefullrealname` is defined in
        ⋅  data.py:DATA and is made by function
        ⋅  cwc_utils.py:moduleininame_to_modulefullrealname()
        ⋅- conversion from `modulefullrealname` to `modulerealname` is made by
        ⋅  function cwc_utils.py:modulefullrealname_to_modulerealname()
        ⋅- DATA keys (for cwc modules) use `moduleininame`, NOT `modulefullrealname`
        _______________________________________________________________________

        ARGUMENT: (str)modulefullrealname, the module full real name to be converted

        RETURNED VALUE: (str)class name
    """
    return modulefullrealname[modulefullrealname.rfind(".")+1:]


def modulefullrealname_to_modulerealname(modulefullrealname):
    """
        modulefullrealname_to_modulerealname()

        Convert module full real name into module read name, something like:
            "wisteria.cwc.pgnreader.cwc_default.ChessGames" > "wisteria.cwc.pgnreader.cwc_default"

        (pimydoc)cwc modules names
        ⋅
        ⋅cwc modules names start with the "wisteria.cwc" string (cf is_a_cwc_name())
        ⋅
        ⋅moduleininame        : e.g. "wisteria.cwc.pgnreader.cwc_default.chessgames"
        ⋅modulefullrealname   : e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames"
        ⋅waemodulename        : e.g. "wisteria.cwc.pgnreader.works_as_expected"
        ⋅classname            : e.g. "ChessGames" (NOT "chessgames")
        ⋅modulerealname       : e.g. "wisteria.cwc.pgnreader.cwc_default"
        ⋅
        ⋅- `moduleininame` are defined in config file;
        ⋅- conversion from `moduleininame` to `modulefullrealname` is defined in
        ⋅  data.py:DATA and is made by function
        ⋅  cwc_utils.py:moduleininame_to_modulefullrealname()
        ⋅- conversion from `modulefullrealname` to `modulerealname` is made by
        ⋅  function cwc_utils.py:modulefullrealname_to_modulerealname()
        ⋅- DATA keys (for cwc modules) use `moduleininame`, NOT `modulefullrealname`
        _______________________________________________________________________

        ARGUMENT: (str)modulefullrealname, the module full real name to be converted

        RETURNED VALUE: (str)module real name
    """
    return modulefullrealname[:modulefullrealname.rfind(".")]


def modulefullrealname_to_waemodulename(modulefullrealname):
    """
        modulefullrealname_to_waemodulename()

        Convert module full real name into a wae('works as expected') module name, something like:
                "wisteria.cwc.pgnreader.cwc_default.ChessGames" >
                        "wisteria.cwc.pgnreader.works_as_expected"
        _______________________________________________________________________

        ARGUMENT: (str)modulefullrealname, the module full real name to be converted

        RETURNED VALUE: (str)wae('works as expected') module name

    """
    name = modulefullrealname[:modulefullrealname.rfind(".")]
    name = name[:name.rfind(".")]
    return name + ".works_as_expected"


def moduleininame_to_modulefullrealname(moduleininame):
    """
        moduleininame_to_modulefullrealname()

        Convert module ini name into module full real name, something like:
            "cwc.pgnreader.cwc_default.chessgames" > "cwc.pgnreader.cwc_default.ChessGames"


        (pimydoc)cwc modules names
        ⋅
        ⋅cwc modules names start with the "wisteria.cwc" string (cf is_a_cwc_name())
        ⋅
        ⋅moduleininame        : e.g. "wisteria.cwc.pgnreader.cwc_default.chessgames"
        ⋅modulefullrealname   : e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames"
        ⋅waemodulename        : e.g. "wisteria.cwc.pgnreader.works_as_expected"
        ⋅classname            : e.g. "ChessGames" (NOT "chessgames")
        ⋅modulerealname       : e.g. "wisteria.cwc.pgnreader.cwc_default"
        ⋅
        ⋅- `moduleininame` are defined in config file;
        ⋅- conversion from `moduleininame` to `modulefullrealname` is defined in
        ⋅  data.py:DATA and is made by function
        ⋅  cwc_utils.py:moduleininame_to_modulefullrealname()
        ⋅- conversion from `modulefullrealname` to `modulerealname` is made by
        ⋅  function cwc_utils.py:modulefullrealname_to_modulerealname()
        ⋅- DATA keys (for cwc modules) use `moduleininame`, NOT `modulefullrealname`
        _______________________________________________________________________

        ARGUMENT: (str)moduleininame, the module ini name to be converted

        RETURNED VALUE: (str)module full real name
    """
    return wisteria.globs.DATA[moduleininame]


def select__works_as_expected__function(data_object_name):
    """
        select__works_as_expected__function()

        Return a "works_as_expected" function apppropriate to <data_object_name>.
        _______________________________________________________________________

        ARGUMENT: (str)<data_object_name>

        RETURNED VALUE: None or a callable
    """
    if not is_a_cwc_name(data_object_name):
        # <data_object_name> is a simple type like "int" (and not a cwc type)
        return None if not wisteria.data.works_as_expected(data_name=data_object_name) \
            else wisteria.data.works_as_expected

    # <data_object_name> is a cwc name:
    #  e.g. "wisteria.cwc.pgnreader.cwc_default.ChessGames" >
    #               "wisteria.cwc.pgnreader.works_as_expected.works_as_expected
    return getattr(wisteria.globs.MODULES[modulefullrealname_to_waemodulename(data_object_name)],
                   "works_as_expected")


def serializer_is_compatible_with_dataobj(serializer,
                                          dataobj):
    """
        serializer_is_compatible_with_dataobj()

        Return True if <serializer> can handle <dataobj>, i.e.
        (a) if <dataobj> is not a cwc name (since all serializers know how to handle
            non-cwc dataobjs).
        (b) if <dataobj> is a cwc name and if <serializer> is compatible with this <dataobj>,
            e.g. pickle knows how to handle "wisteria.cwc.pgnreader.cwc_default.ChessGames",
                        ... since SERIALIZERS["pickle"].cwc is "default"
                 iaswn knows how to handle "wisteria.cwc.pgnreader.iaswn.ChessGames",
                        ... since SERIALIZERS["iaswn"].cwc is "iaswn"

        _______________________________________________________________________

        ARGUMENTS:
        o  (str)serializer
        o  (str)dataobj

        RETURNED VALUE: (bool)
    """
    if not is_a_cwc_name(dataobj):
        return True

    return is_this_an_appropriate_module_for_serializer(
        modulefullrealname_to_modulerealname(dataobj), serializer)


def shorten_cwc_name(cwc_name):
    """
        shorten_cwc_name()

        Shorten <cwc_name> by removing a useless prefix.
        _______________________________________________________________________

        ARGUMENT: (str)cwc_name, the string to be shortened

        RESULT: (str)the shortened string
    """
    return "cwc:" + cwc_name[len("wisteria.cwc."):]
