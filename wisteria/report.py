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
    Wisteria project : wisteria/report.py

    Functions that print the report, especially report().
    ___________________________________________________________________________

    o  cmpdata2phrase(cmpdata)
    o  humanratio(ratio)
    o  open_reportfile(mode=None)
    o  ratio2phrase(ratio, base_string)

    o  partial_report__data()
    o  partial_report__serializers()

    o  report_section_a0(results, s1s2d)
    o  report_section_a1(results, s1s2d)
    o  report_section_a2(results, s1s2d)
    o  report_section_a3(results, s1s2d)
    o  report_section_a4(results, s1s2d)
    o  report_section_a5(results, s1s2d)
    o  report_section_b1a(results, s1s2d)
    o  report_section_b1b(results, s1s2d)
    o  report_section_b1c(results, s1s2d)
    o  report_section_b1d(results, s1s2d)
    o  report_section_b2a(results, s1s2d)
    o  report_section_b2b(results, s1s2d)
    o  report_section_b3(results, s1s2d)
    o  report_section_c1a(results, s1s2d)
    o  report_section_c1b(results, s1s2d)
    o  report_section_c2a(results, s1s2d)
    o  report_section_c2b(results, s1s2d)
    o  report_section_c2c__allvsall(results, s1s2d)
    o  report_section_c2c__serializervsall(results, s1s2d)
    o  report_section_c2c__serializervsserializer(results, s1s2d)
    o  report_section_c2c(results, s1s2d)
    o  report_section_d1a(results, s1s2d)
    o  report_section_d1b(results, s1s2d)
    o  report_section_graphs(results, s1s2d)

    o  report(results, s1s2d)
"""
import os
import sys

import rich.table
from rich.console import Console
from rich import print as rprint

import wisteria.globs
from wisteria.globs import UNITS
from wisteria.globs import REPORT_SHORTCUTS
from wisteria.globs import VERBOSITY_DETAILS, VERBOSITY_DEBUG
from wisteria.globs import DEBUG_CONSOLEWIDTH
from wisteria.wisteriaerror import WisteriaError
from wisteria.utils import shortenedstr, strdigest, trytoimport, normpath
from wisteria.msg import msgreport, msgreporttitle, msgdebug, msgerror
from wisteria.reprfmt import fmt_serializer, fmt_data, fmt_percentage, fmt_list
from wisteria.reprfmt import fmt_nounplural, fmt_mem_usage, fmt_be3s
from wisteria.reprfmt import fmt_exaequowith, fmt_exaequowith_hall, fmt_projectversion
from wisteria.cmdline_mymachine import mymachine
from wisteria.textandnotes import TextAndNotes
from wisteria.matplotgraphs import hbar2png_resultshall
from wisteria.cwc.cwc_utils import select__works_as_expected__function
from wisteria.helpmsg import help_cmdline_output


def cmpdata2phrase(cmpdata):
    """
        cmpdata2phrase()

        Convert <cmpdata> to a phrase describing <cmpdata>.
        _______________________________________________________________________

        ARGUMENT: (str)<cmpdata>: 'all', 'ini', 'cwc' or 'allbutcwc'

        RETURNED VALUE: (str)a string describing <cmpdata>
    """
    assert cmpdata in ('all', 'ini', 'cwc', 'allbutcwc')

    if cmpdata == 'all':
        return "According to the tests " \
            "carried out on all data, "
    if cmpdata == 'ini':
        return "According to the tests " \
            "carried out on the data defined in the configuration file, "
    if cmpdata == 'allbutcwc':
        return "According to the tests " \
            "carried out on all data but cwc data, "
    # cmpdata == 'cwc'
    return "According to the tests " \
        "conducted on data of the 'comparing what is comparable' type, "


def humanratio(ratio,
               explanations=None,
               numbersformat="raw"):
    """
        humanratio()

        Since ratio are difficult to understand when being smaller than 1, this function
        computes, if necessary, the inverse of <ratio> and returns it.

        - if <explanations> is None, return the (float)ratio value;
        - if <explanations> is not None, return an (str)explanation describing the
        (float)ratio value.

        Use <numbersformat> to modify the appearance of numbers in the explanation.
        Please note all ratios computed are not affected by <numbersformat>.
        _______________________________________________________________________

        ARGUMENTS:
        o  (float)ratio, the ratio to be returned
        o  (None|list of str)explanations:
                (str)ratio1_str, (float)ratio1, (str)ratio2_str, (float)ratio2,
                (None if no unit or str)unit_name
        o  numbersformat: "raw" or ".3f" to modify the appearance of numbers in the
                          explanation (ratios are not affected by <numbersformat>)

        RETURNED VALUE: (float)ratio or (float)1/ratio.
    """
    def numbersfmt_raw(number):
        """
            numbersfmt_raw()

            Return <number>.
        """
        return number

    def numbersfmt_3f(number):
        """
            numbersfmt_3f()

            Return a formatted version of <number>, with 3 decimal after the
            decimal point.
        """
        return f"{number:.3f}"

    # ---- explanations is None > let's return a (float)value -----------------
    if explanations is None:
        if ratio < 1:
            return 1/ratio
        return ratio

    if numbersformat == "raw":
        numbersfmt = numbersfmt_raw
    elif numbersformat == ".3f":
        numbersfmt = numbersfmt_3f

    # ---- explanations is not None > let's return a (str)explanation ---------
    ratio1_str, ratio1, ratio2_str, ratio2, unit_name = explanations
    unit_str = "" if unit_name is None else UNITS[unit_name]
    if ratio < 1:
        ratio = 1/ratio
        res = f"factor {ratio:.3f} = {ratio2_str} / {ratio1_str} " \
            f"= {numbersfmt(ratio2)} {unit_str} / {numbersfmt(ratio1)} {unit_str}" \
            "\n" \
            f"{ratio1_str} * {ratio:.3f} = {numbersfmt(ratio1)} {unit_str} * {ratio:.3f} = " \
            f"{ratio2_str} = {numbersfmt(ratio2)} {unit_str}"
    else:
        res = f"factor {ratio:.3f} = {ratio1_str} / {ratio2_str} " \
            f"= {numbersfmt(ratio1)} {unit_str} / {numbersfmt(ratio2)} {unit_str}" \
            "\n" \
            f"{ratio2_str} * {ratio:.3f} = {numbersfmt(ratio2)} {unit_str} * {ratio:.3f} " \
            f"= {ratio1_str} = {numbersfmt(ratio1)} {unit_str}"
    return res


def open_reportfile(mode=None):
    """
        open_reportfile()

        Open the report file, as defined in wisteria.globs.OUTPUT.
        Note that this file is closed by exit_handler().
        _______________________________________________________________________

        ARGUMENT: (None|str)mode: 'r', 'w'... if None, will be wisteria.globs.OUTPUT[2]

        RETURNED RESULT: (the report file descriptor or None if an error occured,
                          the (str)path to the report file or None if an error occured)
    """
    try:
        if mode is None:
            mode = wisteria.globs.OUTPUT[2]
        # pylint: disable=consider-using-with
        #  this object will be closed by exit_handler()
        obj = open(wisteria.globs.OUTPUT[3], mode, encoding="utf-8")
        return obj, os.path.dirname(obj.name)
    except FileNotFoundError as err:
        # a special case: we can't use here msgerror() since there's no report file.
        rprint(f"(ERRORID053) Can't open/create report file '{wisteria.globs.OUTPUT[3]}' "
               f"('{normpath(wisteria.globs.OUTPUT[3])}')"
               f" with opening mode='{mode}'; "
               f"error message is: {err} .")
        rprint("About --ouptput:")
        rprint(help_cmdline_output(details=True))
        return None, None


def ratio2phrase(ratio,
                 base_string):
    """
        ratio2phrase()

        Convert a (float)<ratio> (e.g. 0.5, 2, 4...) to an adverbial phrase
        like "much slower".
        _______________________________________________________________________

        ARGUMENTS:
        o  (float)ratio
        o  (str)base_string: 'slow/fast', 'long/short', 'good/bad', or 'more/less'

        RETURNED VALUE: (str)an adverbial phrase
    """
    assert base_string in ('slow/fast', 'long/short', 'good/bad', 'more/less')

    if base_string == "slow/fast":
        if ratio > 10:
            expression = "extremely slower"
        elif ratio > 2:
            expression = "much slower"
        elif ratio > 1.4:
            expression = "slower"
        elif ratio > 1.1:
            expression = "slightly slower"
        elif ratio > 0.9:
            expression = "slightly faster"
        elif ratio > 0.5:
            expression = "faster"
        elif ratio > 0.1:
            expression = "much faster"
        else:
            expression = "extremely faster"

    elif base_string == "long/short":
        if ratio > 10:
            expression = "extremely longer"
        elif ratio > 2:
            expression = "much longer"
        elif ratio > 1.4:
            expression = "longer"
        elif ratio > 1.1:
            expression = "slightly longer"
        elif ratio > 0.9:
            expression = "slightly shorter"
        elif ratio > 0.5:
            expression = "shorter"
        elif ratio > 0.1:
            expression = "much shorter"
        else:
            expression = "extremely shorter"

    elif base_string == "good/bad":
        if ratio > 10:
            expression = "much, much better"
        elif ratio > 2:
            expression = "much better"
        elif ratio > 1.4:
            expression = "better"
        elif ratio > 1.1:
            expression = "slightly better"
        elif ratio > 0.9:
            expression = "slightly worse"
        elif ratio > 0.5:
            expression = "worse"
        elif ratio > 0.1:
            expression = "much worse"
        else:
            expression = "much, much worse"

    elif base_string == "more/less":
        if ratio > 10:
            expression = "much, much more"
        elif ratio > 2:
            expression = "much more"
        elif ratio > 1.4:
            expression = "more"
        elif ratio > 1.1:
            expression = "slightly more"
        elif ratio > 0.9:
            expression = "slightly less"
        elif ratio > 0.5:
            expression = "less"
        elif ratio > 0.1:
            expression = "much less"
        else:
            expression = "much, much less"

    return expression


def partial_report__data(show_all_data,
                         show_planned_data):
    """
        partial_report__data()

        Display a mini report about data.
        _______________________________________________________________________

        ARGUMENTS:
        o  (bool)show_all_data    : if True, all DATA and UNAVAILABLE DATA will be displayed.
        o  (bool)show_planned_data: if True, all data defined in PLANNED_TRANSCODINGS will be
                                    displayed.
    """
    # ---- all DATA/UNAVAILABLE_DATA ------------------------------------------
    if show_all_data:
        msgreporttitle(
            f"{len(wisteria.globs.DATA)} Available Data "
            f"{fmt_nounplural('Object', len(wisteria.globs.DATA))}")

        string = []
        # for data_object_name, data_object in ...
        for data_object_name, _ in sorted(wisteria.globs.DATA.items()):
            wae = ""
            if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
                wae_func = select__works_as_expected__function(data_object_name)
                if wae_func:
                    wae = f"({wae_func.__module__}.{wae_func.__name__}())"
            string.append(f"{fmt_data(data_object_name)}{wae}")
        msgreport("; ".join(string))

        if wisteria.globs.UNAVAILABLE_DATA:
            msgreport()
            msgreporttitle(
                f"{len(wisteria.globs.UNAVAILABLE_DATA)} Unavailable Data "
                f"{fmt_nounplural('Object', len(wisteria.globs.UNAVAILABLE_DATA))}")

            # why maximallength=300 ?
            # Some error messages (see UNAVAILABLE_DATA structure)
            # are important and must be readable; on the other side
            # some objects may have a huge representation and must be cut.
            msgreport(
                "; ".join(
                    f"{fmt_data(dataobject_name)}"
                    f"({shortenedstr(repr(dataobject), maximallength=300)})"
                    for dataobject_name, dataobject in
                    sorted(wisteria.globs.UNAVAILABLE_DATA.items())))

        # ---- debug message --------------------------------------------------
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            console = Console(width=DEBUG_CONSOLEWIDTH)

            all_dataobjects = sorted(tuple(wisteria.globs.DATA.keys()) +
                                     tuple(wisteria.globs.UNAVAILABLE_DATA.keys()))
            msgdebug(
                f"all data objects ({len(all_dataobjects)} "
                f"data obj., unvailable+available/console width={DEBUG_CONSOLEWIDTH}):")

            console.print('; '.join(data_object_name for data_object_name in all_dataobjects))

        msgreport()

    # ---- only the data defined in PLANNED_TRANSCODINGS ----------------------
    if show_planned_data:
        console = Console(width=DEBUG_CONSOLEWIDTH)
        # (pimydoc)PLANNED_TRANSCODINGS
        # ⋅a list:
        # ⋅    - (str)serializer,
        # ⋅    - (str)data name,
        # ⋅    - (str)fingerprint
        # ⋅
        # ⋅Initialized by results.py:init_planned_transcodings()
        planned_data_names = set(
            data_name for _, data_name, _ in wisteria.globs.PLANNED_TRANSCODINGS)

        msgreporttitle(
            f"{len(planned_data_names)} Data Types to be Used After Selection")

        string = []
        for data_object_name in sorted(planned_data_names):
            wae = ""
            if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
                wae_func = select__works_as_expected__function(data_object_name)
                if wae_func:
                    wae = f"({wae_func.__module__}.{wae_func.__name__}())"
            string.append(f"- {fmt_data(data_object_name)}{wae}")
        msgreport("\n".join(string))


def partial_report__serializers(show_all_serializers,
                                show_planned_serializers):
    """
        partial_report__serializers()

        Display a mini report about serializers.
        _______________________________________________________________________

        ARGUMENTS:
        o  (bool)show_all_serializers    : if True, all SERIALIZERS and UNAVAILABLE SERIALIZERS
                                           will be displayed.
        o  (bool)show_planned_serializers: if True, all serializers defined in PLANNED_TRANSCODINGS
                                           will be displayed.
    """
    if show_all_serializers:
        msgreporttitle(
            f"{len(wisteria.globs.SERIALIZERS)} Available "
            f"{fmt_nounplural('Serializer', len(wisteria.globs.SERIALIZERS))}")

        for serializer in wisteria.globs.SERIALIZERS.values():
            msgreport(f"- {serializer.checkup_repr()}")
            if serializer.name != serializer.human_name:
                # please don't use fmt_serializer() with the following line since
                # we want the raw name of the serializer:
                msgreport(f"  > use '{serializer.name}' in --cmp string.")
            if serializer.comment:
                msgreport(f"  > {serializer.comment}")

        if wisteria.globs.UNAVAILABLE_SERIALIZERS:
            msgreport()

            msgreporttitle(
                f"{len(wisteria.globs.UNAVAILABLE_SERIALIZERS)} Unavailable "
                f"{fmt_nounplural('Serializer', len(wisteria.globs.UNAVAILABLE_SERIALIZERS))}")
            msgreport(
                "- " +
                "\n- ".join(f"{fmt_serializer(serializer.name)}, "
                            f"see {fmt_serializer(serializer.internet)}"
                            for serializer in wisteria.globs.UNAVAILABLE_SERIALIZERS.values()))

        # ---- debug message ------------------------------------------------------
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            console = Console(width=DEBUG_CONSOLEWIDTH)
            all_serializers = sorted(tuple(wisteria.globs.SERIALIZERS.keys()) +
                                     tuple(wisteria.globs.UNAVAILABLE_SERIALIZERS.keys()))

            msgdebug(
                f"({len(all_serializers)} serializers, "
                f"unvailable+available/console width={DEBUG_CONSOLEWIDTH}):")

            console.print('; '.join(serializer_name for serializer_name in all_serializers))

    if show_planned_serializers:
        console = Console(width=DEBUG_CONSOLEWIDTH)
        # (pimydoc)PLANNED_TRANSCODINGS
        # ⋅a list:
        # ⋅    - (str)serializer,
        # ⋅    - (str)data name,
        # ⋅    - (str)fingerprint
        # ⋅
        # ⋅Initialized by results.py:init_planned_transcodings()
        planned_data_serializers = set(
            serializer for serializer, _, _ in wisteria.globs.PLANNED_TRANSCODINGS)

        msgreporttitle(
            f"{len(planned_data_serializers)} Serializers to be Used After Selection")

        for _serializer in planned_data_serializers:
            serializer = wisteria.globs.SERIALIZERS[_serializer]
            msgreport(f"- {serializer.checkup_repr()}")
            if serializer.name != serializer.human_name:
                # please don't use fmt_serializer() with the following line since
                # we want the raw name of the serializer:
                msgreport(f"  > use '{serializer.name}' in --cmp string.")
            if serializer.comment:
                msgreport(f"  > {serializer.comment}")


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_a0(results,
                      s1s2d):
    """
        report_section_a0()

        Sub-function of report() for report section "A1"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle(
            "(A0) Command Line Arguments")
        msgreport()

    # In sys.argv, there's no quotes ("...") anymore.
    # So, let's add quotes around parameters, so that e.g. --cmp=pickle vs json(ini) becomes
    # --cmp="pickle vs json(ini)"
    res = []
    for arg in sys.argv:
        if "=" not in arg:
            res.append(arg)
        else:
            index = arg.index("=")
            res.append(arg[:index+1]+'"'+arg[index+1:]+'"')
    msgreport(" ".join(res))

    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_a1(results,
                      s1s2d):
    """
        report_section_a1()

        Sub-function of report() for report section "A1"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle(
            "(A1) Options Used to Create Reports")
        msgreport()

    msgreport(fmt_projectversion(add_timestamp=True))

    mymachine(detailslevel=0)

    msgreport()

    msgreport(
            "* --cmp = "
            f"'[italic]{wisteria.globs.ARGS.cmp}[/italic]'")
    msgreport(
            "* --filter = "
            f"'[italic]{wisteria.globs.ARGS.filter}[/italic]'")
    msgreport(
            "* --method = "
            f"'[italic]{wisteria.globs.ARGS.method}[/italic]'")
    msgreport(
            "* --report = "
            f"'[italic]{wisteria.globs.ARGS.report}[/italic]'")

    msgreport()


def report_section_a2(results,
                      s1s2d):
    """
        report_section_a2()

        Sub-function of report() for report section "A2"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc' cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(A2) List of Serializers to Be Used Because they have been Selected")
        msgreport()
    partial_report__serializers(show_all_serializers=False,
                                show_planned_serializers=True)

    msgreport()

    if wisteria.globs.DISCARDED_SERIALIZERS:
        msgreporttitle(
            f"Because of the filter value, "
            f"There {fmt_be3s(len(wisteria.globs.DISCARDED_SERIALIZERS))} "
            f"{len(wisteria.globs.DISCARDED_SERIALIZERS)} "
            "discarded "
            f"{fmt_nounplural('serializer', len(wisteria.globs.DISCARDED_SERIALIZERS))}")
        msgreport("; ".join(wisteria.globs.DISCARDED_SERIALIZERS))

    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_a3(results,
                      s1s2d):
    """
        report_section_a3()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(A3) List of Data Objects to Be Used Because they have been Selected")
        msgreport()

    partial_report__data(show_all_data=False,
                         show_planned_data=True)

    msgreport()

    if wisteria.globs.DISCARDED_DATA:
        msgreporttitle(
            f"Because of the filter value, "
            f"There {fmt_be3s(len(wisteria.globs.DISCARDED_DATA))} "
            f"{len(wisteria.globs.DISCARDED_DATA)} "
            "discarded "
            f"{fmt_nounplural('data object', len(wisteria.globs.DISCARDED_DATA))}")
        msgreport("; ".join(wisteria.globs.DISCARDED_DATA))

    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_a4(results,
                      s1s2d):
    """
        report_section_a4()

        Sub-function of report() for report section "A4"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(A4) List of the Planned Transcodings")
        msgreport()

    # (pimydoc)PLANNED_TRANSCODINGS
    # ⋅a list:
    # ⋅    - (str)serializer,
    # ⋅    - (str)data name,
    # ⋅    - (str)fingerprint
    # ⋅
    # ⋅Initialized by results.py:init_planned_transcodings()
    planned_transcodings_number = len(wisteria.globs.PLANNED_TRANSCODINGS)
    for (transcoding_index,
         (serializer,
          data_name,
          fingerprint)) in enumerate(wisteria.globs.PLANNED_TRANSCODINGS):
        msgreport(f"- ({transcoding_index+1}/{planned_transcodings_number}) "
                  f"'{serializer}' x '{data_name}' [{fingerprint}]")


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_a5(results,
                      s1s2d):
    """
        report_section_a5()

        Sub-function of report() for report section "A5"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle(
            "(A5) What do the Encoded Strings Look Like? (basic types/demonstration_dataobj)")
        msgreport("")

    msgreport("Please note that, in this report section, "
              "the object to be encoded is a simple object made of basic "
              "Python types. [bold]The choice of this object "
              "is independent of the data object(s) you choosed to transcode.[/bold]")
    msgreport()

    demonstration_dataobj = wisteria.globs.DATA["demonstration_dataobj"]
    msgreport("- raw demonstration object (as seen by Python, i.e. 'demonstration_dataobj') is ")
    msgreport(f"{demonstration_dataobj}")

    for serializer in results.serializers:
        encoded_string = wisteria.globs.SERIALIZERS[serializer].transcodefunc(
            action="encode",
            obj=demonstration_dataobj)
        msgreport(f"- encoded string created by {fmt_serializer(serializer)}:")
        msgreport(encoded_string)


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_b1a(results,
                       s1s2d):
    """
        report_section_b1a()

        Sub-function of report() for report section "B1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1a) Full Details: Serializer * Data Object")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer > Data Object", width=28)
    table.add_column("Encod. Ok ?", width=11)
    table.add_column(f"Encod. Time ({UNITS['time']})", width=11)
    table.add_column(f"Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column("Decod. Ok ?", width=11)
    table.add_column(f"Decod. Time ({UNITS['time']})", width=11)
    table.add_column("Reversibility ?", width=16)
    table.add_column("Memory", width=12)
    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        table.add_column("Fingerprint ( serial. + dataobj)", width=9)

    for serializer in results.serializers:
        table.add_row(f"{fmt_serializer(serializer)} :")
        for dataobj in results.dataobjs:
            if dataobj in results[serializer]:
                if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
                    # everything but debug mode:
                    table.add_row(
                        "> " + f"{fmt_data(dataobj)}",
                        results.repr_attr(serializer, dataobj, "encoding_success"),
                        results.repr_attr(serializer, dataobj, "encoding_time"),
                        results.repr_attr(serializer, dataobj, "encoding_strlen"),
                        results.repr_attr(serializer, dataobj, "decoding_success"),
                        results.repr_attr(serializer, dataobj, "decoding_time"),
                        results.repr_attr(serializer, dataobj, "reversibility"),
                        results.repr_attr(serializer, dataobj, "mem_usage"),)
                else:
                    # debug mode:
                    table.add_row(
                        "> " + f"{fmt_data(dataobj)}",
                        results.repr_attr(serializer, dataobj, "encoding_success"),
                        results.repr_attr(serializer, dataobj, "encoding_time"),
                        results.repr_attr(serializer, dataobj, "encoding_strlen"),
                        results.repr_attr(serializer, dataobj, "decoding_success"),
                        results.repr_attr(serializer, dataobj, "decoding_time"),
                        results.repr_attr(serializer, dataobj, "reversibility"),
                        results.repr_attr(serializer, dataobj, "mem_usage"),
                        "["+strdigest(serializer+dataobj)+"]")

    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_b1b(results,
                       s1s2d):
    """
        report_section_b1b()

        Sub-function of report() for report section "B1b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1b) Full Details: Serializers")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer", width=28)
    table.add_column(f"Encod. Ok ? (Max={results.dataobjs_number})", width=11)
    table.add_column(f"Σ Encoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column(f"Decod. Ok ? (Max={results.dataobjs_number})", width=11)
    table.add_column(f"Σ Decoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Reversibility ? (Max={results.dataobjs_number})", width=16)
    table.add_column("Σ memory", width=12)

    for serializer in results.serializers:
        table.add_row(
            f"{fmt_serializer(serializer)}",
            f"{results.ratio_encoding_success(serializer=serializer)}",
            f"{results.total_encoding_time(serializer=serializer)}",
            f"{results.total_encoding_strlen(serializer=serializer)}",
            f"{results.ratio_decoding_success(serializer=serializer)}",
            f"{results.total_decoding_time(serializer=serializer)}",
            f"{results.ratio_reversibility(serializer=serializer)}",
            f"{results.total_mem_usage(serializer=serializer)}",
        )
    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_b1c(results,
                       s1s2d):
    """
        report_section_b1c()

        Sub-function of report() for report section "B1c"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1c) Full Details: Serializers, Hall of Fame")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("#", width=2)
    table.add_column(f"Encod. Ok ? (Max={results.dataobjs_number})", width=17)
    table.add_column(f"Σ Encoded Time ({UNITS['time']})", width=17)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})", width=17)
    table.add_column(f"Decod. Ok ? (Max={results.dataobjs_number})", width=17)
    table.add_column(f"Σ Decoded Time ({UNITS['time']})", width=17)
    table.add_column(f"Reversibility (Coverage Rate) (Max={results.dataobjs_number})", width=17)
    table.add_column("memory", width=12)

    for index in range(results.serializers_total_number):
        table.add_row(
            f"{index+1}",
            f"{results.get_hall('encoding_success', index)}",
            f"{results.get_hall('encoding_time', index)}",
            f"{results.get_hall('encoding_strlen', index)}",
            f"{results.get_hall('decoding_success', index)}",
            f"{results.get_hall('decoding_time', index)}",
            f"{results.get_hall('reversibility', index)}",
            f"{results.get_hall('mem_usage', index)}",
        )

    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_b1d(results,
                       s1s2d):
    """
        report_section_b1d()

        Sub-function of report() for report section "B1d"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1d) Full Details: Which Serializer(s) Can't Handle Data Objects ?")

    for serializer in results.serializers:
        _list = tuple(dataobj for dataobj in results[serializer]
                      if results[serializer][dataobj] is None or
                      results[serializer][dataobj].reversibility is None or
                      not results[serializer][dataobj].reversibility)
        if not _list:
            msgreport(f"* ({fmt_serializer(serializer)}) "
                      "There's no data object that serializer "
                      f"{fmt_serializer(serializer)} can't handle.")
        else:
            msgreport(f"* ({fmt_serializer(serializer)}) "
                      f"Serializer {fmt_serializer(serializer)} "
                      "can't handle the following data objects:")
            for dataobj in _list:
                msgreport(f"  - {fmt_data(dataobj)}")
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_b2a(results,
                       s1s2d):
    """
        report_section_b2a()

        Sub-function of report() for report section "B2a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B2a) full details: data object * serializer")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Data Object > Serializer", width=28)
    table.add_column("Encod. Ok ?", width=11)
    table.add_column(f"Encod. Time ({UNITS['time']})", width=11)
    table.add_column(f"Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column("Decod. Ok ?", width=11)
    table.add_column(f"Decod. Time ({UNITS['time']})", width=11)
    table.add_column("Reversibility ?", width=16)
    table.add_column("Memory", width=12)
    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        table.add_column("Fingerprint ( serial. + dataobj)", width=9)

    for dataobj in results.dataobjs:
        table.add_row(f"{fmt_data(dataobj)} :")
        for serializer in results.serializers:
            if dataobj in results[serializer]:
                if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
                    # everything but debug mode:
                    table.add_row(
                        "> " + f"{fmt_serializer(serializer)}",
                        results.repr_attr(serializer, dataobj, "encoding_success"),
                        results.repr_attr(serializer, dataobj, "encoding_time"),
                        results.repr_attr(serializer, dataobj, "encoding_strlen"),
                        results.repr_attr(serializer, dataobj, "decoding_success"),
                        results.repr_attr(serializer, dataobj, "decoding_time"),
                        results.repr_attr(serializer, dataobj, "reversibility"),
                        results.repr_attr(serializer, dataobj, "mem_usage")
                    )
                else:
                    # debug mode:
                    table.add_row(
                        "> " + f"{fmt_serializer(serializer)}",
                        results.repr_attr(serializer, dataobj, "encoding_success"),
                        results.repr_attr(serializer, dataobj, "encoding_time"),
                        results.repr_attr(serializer, dataobj, "encoding_strlen"),
                        results.repr_attr(serializer, dataobj, "decoding_success"),
                        results.repr_attr(serializer, dataobj, "decoding_time"),
                        results.repr_attr(serializer, dataobj, "reversibility"),
                        results.repr_attr(serializer, dataobj, "mem_usage"),
                        "["+strdigest(serializer+dataobj)+"]")
    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_b2b(results,
                       s1s2d):
    """
        report_section_b2b()

        Sub-function of report() for report section "B2b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B2b) Full Details: Data Objects")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Data Object",
                     width=28)
    table.add_column(f"Encod. Ok ? (Max={results.serializers_total_number})",
                     width=11)
    table.add_column(f"Σ Encoded Time ({UNITS['time']})",
                     width=11)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})",
                     width=13)
    table.add_column(f"Decod. Ok ? (Max={results.serializers_total_number})",
                     width=11)
    table.add_column(f"Σ Decoded Time ({UNITS['time']})",
                     width=11)
    table.add_column(f"Reversibility (Coverage Rate) (Max={results.serializers_total_number})",
                     width=16)
    table.add_column("Σ memory",
                     width=12)

    for dataobj in results.dataobjs:
        table.add_row(
            f"{fmt_data(dataobj)}",
            f"{results.ratio_encoding_success(dataobj=dataobj)}",
            f"{results.total_encoding_time(dataobj=dataobj)}",
            f"{results.total_encoding_strlen(dataobj=dataobj)}",
            f"{results.ratio_decoding_success(dataobj=dataobj)}",
            f"{results.total_decoding_time(dataobj=dataobj)}",
            f"{results.ratio_reversibility(dataobj=dataobj)}",
            f"{results.total_mem_usage(dataobj=dataobj)}",
        )
    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_b3(results,
                      s1s2d):
    """
        report_section_b3()

        Sub-function of report() for report section "B2b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B3) Encoded String for all Data Objects, for all Serializers")

    for (serializer,
         data_name,
         fingerprint) in wisteria.globs.PLANNED_TRANSCODINGS:
        msgreport(f"o  '{serializer}' x '{data_name}' [{fingerprint}]")

        if serializer not in results or \
           data_name not in results[serializer]:
            msgreport("   o  NOT COMPUTED")
        elif not results[serializer][data_name].encoding_success:
            msgreport("   o  this object could not be successfully encoded")
        else:
            msgreport(f"   o  type: {type(results[serializer][data_name].encoded_object).__name__}")
            msgreport(f"   o  len:  {len(results[serializer][data_name].encoded_object)}")
            msgreport(f"   o  repr: {repr(results[serializer][data_name].encoded_object)}")
        msgreport()


def report_section_c1a(results,
                       s1s2d):
    """
        report_section_c1a()

        Sub-function of report() for report section "C1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    def show(serializer,
             cmpdata):
        """
            show()

            Print the message for serializer (str)<serializer> and for <cmpdata>.

            ___________________________________________________________________

            ARGUMENTS:
            o  (str)serializer
            o  (str)cmpdata              -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
        """
        data = wisteria.globs.DATA

        _list = []  # list of the data_name that CAN'T BE HANDLED by <serializer>.
        for data_name in results.dataobjs:
            if data_name in results[serializer] and \
               results[serializer][data_name] is not None and \
               results[serializer][data_name].reversibility:
                _list.append(data_name)

        if not data:
            msgreport(
                f"{fmt_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                "no data objects may be used: therefore there's no conclusion about the objects "
                f"data serializer {fmt_serializer(serializer)} can handle.")
        elif not _list:
            msgreport(
                f"{fmt_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                "there's no data object "
                f"among the {results.dataobjs_number} used data objects "
                f"that serializer {fmt_serializer(serializer)} can handle (0%).")
        elif len(_list) == 1:
            msgreport(
                f"{fmt_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{fmt_serializer(serializer)} can handle one data object "
                f"among {results.dataobjs_number} "
                f"({fmt_percentage(100*len(_list)/results.dataobjs_number)}), namely "
                f"{fmt_list(_list, fmt_data)} .")
        else:
            msgreport(
                f"{fmt_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{fmt_serializer(serializer)} can handle {len(_list)} data objects "
                f"among {results.dataobjs_number} "
                f"({fmt_percentage(100*len(_list)/results.dataobjs_number)}), namely "
                f"{fmt_list(_list, fmt_data)} .")

    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C1a) Conclusion: Data Objects Handled by the Serializer(s)")
        msgreport()

    seria1, seria2, cmpdata = s1s2d
    if seria1 != 'all':
        show(seria1, cmpdata)
        msgreport()
    if seria2 != 'all':
        show(seria2, cmpdata)
        msgreport()

    # Other serializers, leaving apart <seria1> and <seria2> ?
    _serializers = list(wisteria.globs.SERIALIZERS.keys())
    if seria1 != 'all':
        _serializers.remove(seria1)
    if seria2 != 'all':
        _serializers.remove(seria2)
    if _serializers and (seria1 == 'all' or seria2 == 'all'):
        if seria1 != 'all' or seria2 != 'all':
            msgreport("[bold]Other serializers:[/bold]")
        for __serializer in _serializers:
            show(__serializer, cmpdata)
        msgreport()


def report_section_c1b(results,
                       s1s2d):
    """
        report_section_c1b()

        Sub-function of report() for report section "C1b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    def show(serializer,
             cmpdata):
        """
            show()

            Print the message for serializer (str)<serializer> and for <cmpdata>.
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)serializer
            o  (str)cmpdata              -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
        """
        data = wisteria.globs.DATA

        _list = []  # list of the data_name that CAN BE HANDLED by <serializer>.
        for data_name in results.dataobjs:
            if data_name in results[serializer] and \
               results[serializer][data_name] is not None and \
               not results[serializer][data_name].reversibility:
                _list.append(data_name)

        if not data:
            msgreport(
                f"{fmt_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                "no data objects may be used: therefore there's no conclusion about the objects "
                f"data serializer {fmt_serializer(serializer)} can't handle.")
        elif not _list:
            msgreport(f"{fmt_serializer(serializer)}: "
                      f"{cmpdata2phrase(cmpdata)}"
                      "there's no data object "
                      f"among the {results.dataobjs_number} used data objects "
                      f"that serializer {fmt_serializer(serializer)} can't handle (0%).")
        elif len(_list) == 1:
            msgreport(
                f"{fmt_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{fmt_serializer(serializer)} can't handle one data object "
                f"among {results.dataobjs_number} "
                f"({fmt_percentage(100*len(_list)/results.dataobjs_number)}), namely "
                f"{fmt_list(_list, fmt_data)} .")
        else:
            msgreport(
                f"{fmt_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{fmt_serializer(serializer)} can't handle {len(_list)} data objects "
                f"among {results.dataobjs_number} "
                f"({fmt_percentage(100*len(_list)/results.dataobjs_number)}), namely "
                f"{fmt_list(_list, fmt_data)} .")

    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C1b) Conclusion: "
                       "Data Objects [italic]NOT[/italic] Handled by the Serializer(s)")
        msgreport()

    seria1, seria2, cmpdata = s1s2d
    if seria1 != 'all':
        show(seria1, cmpdata)
        msgreport()
    if seria2 != 'all':
        show(seria2, cmpdata)
        msgreport()

    # Other serializers, leaving apart <seria1> and <seria2> ?
    _serializers = list(wisteria.globs.SERIALIZERS.keys())
    if seria1 != 'all':
        _serializers.remove(seria1)
    if seria2 != 'all':
        _serializers.remove(seria2)
    if _serializers and (seria1 == 'all' or seria2 == 'all'):
        if seria1 != 'all' or seria2 != 'all':
            msgreport("[bold]Other serializers:[/bold]")
        for __serializer in _serializers:
            show(__serializer, cmpdata)
        msgreport()


def report_section_c2a(results,
                       s1s2d):
    """
        report_section_c2a()

        Sub-function of report() for report section "C2a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C2a) Conclusion: Serializers ([italic]Not Sorted[/italic])")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer", width=25)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})", width=16)
    table.add_column(f"Σ Encod.+Decod. Time ({UNITS['time']})", width=16)
    table.add_column(f"Reversibility (Coverage Rate) (Max={results.dataobjs_number})", width=16)
    table.add_column("Memory", width=12)

    seria1, seria2, _ = s1s2d
    _serializers = []
    if seria1 != 'all':
        _serializers.append(seria1)
    if seria2 != 'all':
        _serializers.append(seria2)
    _serializers.append("-")
    for serializer in results.serializers:
        if serializer not in _serializers:
            _serializers.append(serializer)
    if _serializers[-1] == "-":
        # let's remove this useless '-' since there's no more serializer(s) after.
        _serializers.pop()

    for serializer in _serializers:
        if serializer != "-":
            table.add_row(
                f"{fmt_serializer(serializer)}",
                f"{results.total_encoding_strlen(serializer=serializer)}",
                f"{results.total_encoding_plus_decoding_time(serializer=serializer)}",
                f"{results.ratio_reversibility(serializer=serializer)}",
                f"{results.total_mem_usage(serializer=serializer)}")
        else:
            table.add_row(
                "-",
                "-",
                "-",
                "-")

    msgreport(table)
    msgreport()


def report_section_c2b(results,
                       s1s2d):
    """
        report_section_c2b()

        Sub-function of report() for report section "C2b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C2b) "
                       "Conclusion: Overall Score Based on 4 Comparisons Points "
                       "(Σ Encoded Str. Length/Σ Encod.+Decod. Time/Coverage Rate/Σ memory)")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer", width=25)
    table.add_column("Overall Score", width=13)

    seria1, seria2, _ = s1s2d
    _serializers = []
    if seria1 != 'all':
        _serializers.append(seria1)
    if seria2 != 'all':
        _serializers.append(seria2)
    _serializers.append("-")
    for serializer in results.serializers:
        if serializer not in _serializers:
            _serializers.append(serializer)
    if _serializers[-1] == "-":
        # let's remove this useless '-' since there's no more serializer(s) after.
        _serializers.pop()

    for serializer in _serializers:
        if serializer != "-":
            table.add_row(
                f"{fmt_serializer(serializer)}",
                f"{results.overallscores[serializer]}")
        else:
            table.add_row(
                "-",
                "-")

    msgreport(table)
    msgreport()


def report_section_c2c__allvsall(results,
                                 s1s2d):
    """
        report_section_c2c__allvsall()

        Sub-function of report_section_c2c() in the case where
        seria1==seria2=='all'.
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    def explicit(attribute,
                 meaning):
        """
            explicit()

            Using results.hall[], create sentences like:
            - "pickle is the slowest to encode/decode"
                (attribute='encoding_plus_decoding_time', meaning='-')
            - "pickle is the quickest to encode/decode"
                (attribute='encoding_plus_decoding_time', meaning='+')
            - "all serializers are equal when it comes to encoding/decoding time"
                (attribute='encoding_plus_decoding_time'; special case: equality)
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)attribute:  'mem_usage',
                                'reversibility',
                                'encoding_strlen',
                                'encoding_plus_decoding_time'
            o  (str)meaning:    '+' or '-'

            RETURNED VALUE: (str)a phrase
        """
        if attribute == 'mem_usage':
            string_equality = 'all serializers are equal when it comes to memory consumption'
            if meaning == '-':
                string_champion = 'uses the most memory'
            elif meaning == '+':
                string_champion = 'uses the least memory'
        elif attribute == 'reversibility':
            string_equality = 'all serializers are equal when it comes to data coverage'
            if meaning == '-':
                string_champion = 'has the worst coverage'
            elif meaning == '+':
                string_champion = 'has the best coverage'
        elif attribute == 'encoding_strlen':
            string_equality = 'all serializers are equal when it comes to encoded string length'
            if meaning == '-':
                string_champion = 'produces the longest strings'
            elif meaning == '+':
                string_champion = 'produces the shortest strings'
        elif attribute == 'encoding_plus_decoding_time':
            string_equality = 'all serializers are equal when it comes to encoding/decoding time'
            if meaning == '-':
                string_champion = 'is the slowest to encode/decode'
            elif meaning == '+':
                string_champion = 'is the quickest to encode/decode'

        equality = results.are_all_serializers_equal_in_the_hall(attribute)
        # ---- not equality ? ----
        if not equality:
            # if the meaning is positive (meaning == '+') we work with the first index;
            # if the meaning is negative (meaning == '-') we work with the last index:
            index = {'+': 0,
                     '-': -1}[meaning]

            return f"{fmt_serializer(results.hall[attribute][index][1])}" \
                f"{(fmt_exaequowith_hall(results, index, attribute))}" \
                f" {string_champion}"

        # ---- equality ? ----
        return string_equality

    _, _, cmpdata = s1s2d  # seria1, seria2, cmpdata

    text = TextAndNotes()
    text.append(cmpdata2phrase(cmpdata))

    text.append(f"{explicit('encoding_plus_decoding_time', '+')}, ")
    text.append(f"{explicit('encoding_strlen', '+')}, ")
    text.append(f"{explicit('reversibility', '+')} ")
    text.append(f"and {explicit('mem_usage', '+')}. ")

    bests = results.get_overallscore_bestrank()
    if len(bests) == 1:
        text.append(f"{fmt_serializer(bests[0])} is ranked #1 "
                    f"among {results.serializers_total_number} serializers, "
                    "according to the overall scores (__note:overallscore__).")
    else:
        text.append(f"{fmt_list(bests, fmt_serializer)} "
                    f"are ranked #1 among {results.serializers_total_number} serializers, "
                    "according to the overall scores (__note:overallscore__).")

    text.append("\nOn the contrary, ")
    text.append(f"{explicit('encoding_plus_decoding_time', '-')}, ")
    text.append(f"{explicit('encoding_strlen', '-')}, ")
    text.append(f"{explicit('reversibility', '-')} ")
    text.append(f"and {explicit('mem_usage', '-')}. ")

    worsts = results.get_overallscore_worstrank()
    if len(worsts) == 1:
        text.append(f"{fmt_serializer(worsts[0])} is ranked #{results.serializers_total_number} "
                    f"among {results.serializers_total_number} serializers, "
                    "according to the overall scores (__note:overallscore__).")
    else:
        text.append(f"{fmt_list(worsts, fmt_serializer)} "
                    f"are ranked #{results.serializers_total_number} among "
                    f"{results.serializers_total_number} serializers, "
                    "according to the overall scores (__note:overallscore__).")

    text.notes.append(
        ("overallscore",
         "a rank based on 4 comparisons points: "
         "Σ encoded str./Σ encod.+decod. time/Coverage Rate/Σ memory"))

    msgreport(text.output())
    msgreport()


def report_section_c2c__serializervsall(results,
                                        s1s2d):
    """
        report_section_c2c__serializervsall()

        Sub-function of report_section_c2c() in the case where
        seria1!='all' and where seria2=='all'.
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    seria1, seria2, cmpdata = s1s2d

    text = TextAndNotes()
    text.append(cmpdata2phrase(cmpdata))

    # <serializer> is the reference serializer against all others.
    if seria1 != 'all':
        serializer = seria1
    else:
        serializer = seria2
    rank = results.get_overallscore_rank(serializer)
    score = results.overallscores[serializer]
    text.append(
        f"{fmt_serializer(serializer)} "
        f"is ranked #{rank+1} among {results.serializers_total_number} serializers"
        f"{(fmt_exaequowith(serializer, results.get_serializers_whose_overallscore_is(score)))}"
        f" (__note:overallscore__)")
    text.append(". ")

    text.notes.append(
        ("overallscore",
         "a rank based on 4 comparisons points: "
         "Σ jsonstr.len./Σ encod.+decod. time/Coverage Rate/Σ memory"))

    def explicit(attribute):
        """
            explicit()

            Using results.hall[], create strings like:
            - "There's no serializer that is worse than pickle when it comes to data coverage."
                (attribute='reversibility')
            - "All serializers are equal when it comes to memory consumption."
                (attribute='mem_usage')
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)attribute:  'mem_usage',
                                'reversibility',
                                'encoding_strlen',
                                'encoding_plus_decoding_time'

            RETURNED VALUE: (str)a sentence
        """
        _less, _more = results.comparison_inside_hall(serializer, attribute)
        equality = results.are_all_serializers_equal_in_the_hall(attribute)

        if equality:
            if attribute == 'mem_usage':
                string = 'All serializers are equal when it comes to memory consumption.'
            elif attribute == "reversibility":
                string = 'All serializers are equal when it comes to data coverage.'
            elif attribute == "encoding_strlen":
                string = 'All serializers are equal when it comes to encoded string length.'

        elif attribute == "mem_usage":
            if not _less:
                string = "There's no serializer that consumes more memory than " \
                        f"{fmt_serializer(serializer)} "
            elif len(_less) == 1:
                string = f"Only {fmt_serializer(_less[0])} consumes more memory than " \
                         f"{fmt_serializer(serializer)} "
            else:
                string = f"There are {len(_less)} serializers" \
                          ", namely " \
                         f"{fmt_list(_less, fmt_serializer)}, " \
                         f"that consume more memory than {fmt_serializer(serializer)} "

            if not _more:
                string += "and there's no serializer that consumes less memory than " \
                          f"{fmt_serializer(serializer)}."
            elif len(_more) == 1:
                string += f"and only {fmt_serializer(_more[0])} consumes less memory than " \
                          f"{fmt_serializer(serializer)}."
            else:
                string += f"and there are {len(_more)} serializers" \
                           ", namely " \
                          f"{fmt_list(_more, fmt_serializer)}, " \
                          f"that consume less memory than {fmt_serializer(serializer)}."

        elif attribute == "reversibility":
            if not _less:
                string = "There's no serializer that is worse than " \
                        f"{fmt_serializer(serializer)} " \
                         "when it comes to data coverage."
            elif len(_less) == 1:
                string = f"Only {fmt_serializer(_less[0])} is worse than " \
                         f"{fmt_serializer(serializer)} " \
                         "when it comes to data coverage."
            else:
                string = f"There are {len(_less)} serializers" \
                          ", namely " \
                         f"{fmt_list(_less, fmt_serializer)}, " \
                         f"that are worse than {fmt_serializer(serializer)} " \
                         "when it comes to data coverage."

            if not _more:
                string += "and there's no serializer that is better than " \
                          f"{fmt_serializer(serializer)}." \
                          "when it comes to data coverage."
            elif len(_more) == 1:
                string += f"and only {fmt_serializer(_more[0])} is better than " \
                          f"{fmt_serializer(serializer)}." \
                          "when it comes to data coverage."
            else:
                string += f"and there are {len(_more)} serializers" \
                           ", namely " \
                          f"{fmt_list(_more, fmt_serializer)}, " \
                          f"are better than {fmt_serializer(serializer)}." \
                          "when it comes to data coverage."

        elif attribute == "encoding_strlen":
            if not _less:
                string = "There's no serializer that produces longer strings than " \
                        f"{fmt_serializer(serializer)} "
            elif len(_less) == 1:
                string = f"Only {fmt_serializer(_less[0])} is produces longer strings than " \
                         f"{fmt_serializer(serializer)} "
            else:
                string = f"There are {len(_less)} serializers" \
                          ", namely " \
                         f"{fmt_list(_less, fmt_serializer)}, " \
                         f"that produce longer strings than {fmt_serializer(serializer)} "

            if not _more:
                string += "and there's no serializer that produces shorter strings than " \
                          f"{fmt_serializer(serializer)}."
            elif len(_more) == 1:
                string += f"and only {fmt_serializer(_more[0])} produces shorter strings than " \
                          f"{fmt_serializer(serializer)}."
            else:
                string += f"and there are {len(_more)} serializers" \
                           ", namely " \
                          f"{fmt_list(_more, fmt_serializer)}, " \
                          f"that produces shorter strings than {fmt_serializer(serializer)}."

        elif attribute == "encoding_plus_decoding_time":
            if not _less:
                string = "There's no serializer slower than " \
                        f"{fmt_serializer(serializer)} "
            elif len(_less) == 1:
                string = f"Only {fmt_serializer(_less[0])} is slower than " \
                         f"{fmt_serializer(serializer)} "
            else:
                string = f"There are {len(_less)} serializers" \
                          ", namely " \
                         f"{fmt_list(_less, fmt_serializer)}, " \
                         f"that are slower than {fmt_serializer(serializer)} "

            if not _more:
                string += "and there's no serializer that is faster than " \
                          f"{fmt_serializer(serializer)}."
            elif len(_more) == 1:
                string += f"and only {fmt_serializer(_more[0])} is faster than " \
                          f"{fmt_serializer(serializer)}."
            else:
                string += f"and there are {len(_more)} serializers" \
                           ", namely " \
                          f"{fmt_list(_more, fmt_serializer)}, " \
                          f"that is faster than {fmt_serializer(serializer)}."

        return string

    for attribute in ("encoding_strlen",
                      "encoding_plus_decoding_time",
                      "reversibility",
                      "mem_usage",
                      ):
        text.append(explicit(attribute)+" ")

    msgreport(text.output())
    msgreport()


def report_section_c2c__serializervsserializer(results,
                                               s1s2d):
    """
        report_section_c2c__serializervsserializer()

        Sub-function of report_section_c2c() in the case where
        seria1 and seria2 !='all'.
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    seria1, seria2, cmpdata = s1s2d

    text = TextAndNotes()
    text.append(cmpdata2phrase(cmpdata))

    # ---- encoding/decoding time -----------------------------------------
    if results.total_encoding_plus_decoding_time(serializer=seria1, output='value') is None or \
       results.total_encoding_plus_decoding_time(serializer=seria2, output='value') is None:
        text.append("no information can be given about the total amount of times "
                    "required to encode and decode since at least one serializer "
                    "returns incoherent informations about this amount of time; ")
    else:
        total_encoding_time_ratio = \
            results.total_encoding_plus_decoding_time(serializer=seria1, output='value') \
            / results.total_encoding_plus_decoding_time(serializer=seria2,
                                                        output='value')

        if total_encoding_time_ratio == 1:
            text.append(
                f"{fmt_serializer(seria1)} "
                f"and {fmt_serializer(seria2)} "
                "seem to require exactly the same time to encode and decode; ")
        else:
            text.append(
                f"{fmt_serializer(seria1)} "
                f"is {ratio2phrase(total_encoding_time_ratio, 'slow/fast')} "
                f"- by a factor of {humanratio(total_encoding_time_ratio):.3f} "
                "(__note:total_encoding_time_ratio__) - "
                "than "
                f"{fmt_serializer(seria2)} "
                "to encode and decode; ")

            text.notes.append(
                ("total_encoding_time_ratio",
                 humanratio(
                     total_encoding_time_ratio,
                     explanations=(
                         f"{fmt_serializer(seria1)}'s Σ encod.+decod. time",
                         results.total_encoding_plus_decoding_time(serializer=seria1,
                                                                   output='value'),
                         f"{fmt_serializer(seria2)}'s Σ encod.+decod. time",
                         results.total_encoding_plus_decoding_time(serializer=seria2,
                                                                   output='value'),
                         'time',
                     ),
                     numbersformat=".3f"
                 )))

    # ---- total_encoding_strlen -----------------------------------------
    if results.total_encoding_strlen(serializer=seria1, output='value') is None or \
       results.total_encoding_strlen(serializer=seria2, output='value') is None:
        text.append("no information can be given about the length of "
                    "encoded strings since at least one serializer "
                    "returns incoherent informations about this length; ")
    else:
        total_encoding_strlen_ratio = \
            results.total_encoding_strlen(serializer=seria1, output='value') \
            / results.total_encoding_strlen(serializer=seria2,
                                            output='value')

        if total_encoding_strlen_ratio == 1:
            text.append(f"{fmt_serializer(seria1)} "
                        f"and {fmt_serializer(seria2)} "
                        "seem to produce strings that have exactly the same size; ")
        else:
            text.append("strings produced by "
                        f"{fmt_serializer(seria1)} "
                        f"are {ratio2phrase(total_encoding_strlen_ratio, 'long/short')} "
                        f"- by a factor of {humanratio(total_encoding_strlen_ratio):.3f} "
                        f"(__note:total_encoding_strlen_ratio__) - "
                        "than "
                        f"strings produced by {fmt_serializer(seria2)}; ")

            text.notes.append(
                ("total_encoding_strlen_ratio",
                 humanratio(
                     total_encoding_strlen_ratio,
                     explanations=(
                         f"{fmt_serializer(seria1)}'s jsonstring strlen",
                         results.total_encoding_strlen(serializer=seria1,
                                                       output='value'),
                         f"{fmt_serializer(seria2)}'s jsonstring strlen",
                         results.total_encoding_strlen(serializer=seria2,
                                                       output='value'),
                         'string length',
                     ),
                     numbersformat="raw",
                 )))

    # ---- ratio_reversibility -----------------------------------------------
    ratio_reversibility = \
        results.ratio_reversibility(serializer=seria1, output='value') \
        / results.ratio_reversibility(serializer=seria2,
                                      output='value')

    if ratio_reversibility == 1:
        text.append(f"{fmt_serializer(seria1)} "
                    f"and {fmt_serializer(seria2)} "
                    "seem to have exactly the same data coverage; ")
    else:
        text.append(f"{fmt_serializer(seria1)}'s coverage "
                    f"is {ratio2phrase(ratio_reversibility, 'good/bad')} "
                    f"- by a factor of {humanratio(ratio_reversibility):.3f} "
                    f"(__note:ratio_reversibility__) - "
                    "than "
                    f"{fmt_serializer(seria2)}'s coverage; ")

        text.notes.append(
            ("ratio_reversibility",
             humanratio(
                 ratio_reversibility,
                 explanations=(
                     f"{fmt_serializer(seria1)}'s reversibility ratio",
                     results.ratio_reversibility(serializer=seria1,
                                                 output='value'),
                     f"{fmt_serializer(seria2)}'s reversibility ratio",
                     results.ratio_reversibility(serializer=seria2,
                                                 output='value'),
                     None,
                 ),
                 numbersformat=".3f"
             )))

    # ---- total_mem_usage ------------------------------------------------
    if results.total_mem_usage(serializer=seria1, output='value') is None or \
       results.total_mem_usage(serializer=seria2, output='value') is None:
        text.append("no information can be given about the total amount of time "
                    "required to encode and decode strings since at least one serializer "
                    "returns incoherent informations about this amound of time; ")
    elif results.total_mem_usage(serializer=seria2,
                                 output='value') == 0:
        if results.total_mem_usage(serializer=seria1,
                                   output='value') == 0:
            # mem_usage==0 for both serializers:
            text.append(
                f"neither {fmt_serializer(seria1)} "
                f"nor {fmt_serializer(seria2)} seems to consume memory.")
        else:
            # mem_usage==0 for seria2:
            text.append(
                f"{fmt_serializer(seria1)} consumes "
                f"{fmt_mem_usage(results.total_mem_usage(serializer=seria1, output='value'))}"
                " but "
                f"{fmt_serializer(seria2)} seems to consume no memory.")
    else:
        # mem_usage!=0 for both serializers:
        total_mem_usage_ratio = \
            results.total_mem_usage(serializer=seria1, output='value') \
            / results.total_mem_usage(serializer=seria2,
                                      output='value')

        if total_mem_usage_ratio == 1:
            text.append(f"{fmt_serializer(seria1)} "
                        f"and {fmt_serializer(seria2)} seem "
                        "to consume exactly as much memory as each other. ")
        else:
            text.append(f"{fmt_serializer(seria1)} "
                        f"consumes {ratio2phrase(total_mem_usage_ratio, 'more/less')} memory "
                        f"- by a factor of {humanratio(total_mem_usage_ratio):.3f} "
                        f"(__note:total_mem_usage_ratio__) - "
                        "than "
                        f"{fmt_serializer(seria2)}. ")

            text.notes.append(
                ("total_mem_usage_ratio",
                 humanratio(
                     total_mem_usage_ratio,
                     explanations=(
                         f"{fmt_serializer(seria1)}'s used memory",
                         results.total_mem_usage(serializer=seria1,
                                                 output='value'),
                         f"{fmt_serializer(seria2)}'s used memory",
                         results.total_mem_usage(serializer=seria2,
                                                 output='value'),
                         'memory',
                     ),
                     numbersformat="raw",
                 )))

    msgreport(text.output())
    msgreport()


def report_section_c2c(results,
                       s1s2d):
    """
        report_section_c2c()

        Sub-function of report() for report section "C2c"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C2c) Conclusion")

    seria1, seria2, _ = s1s2d  # seria1, seria2, cmpdata

    if seria1 == 'all' and seria2 == 'all':
        report_section_c2c__allvsall(results, s1s2d)
    elif seria1 != 'all' and seria2 != 'all':
        report_section_c2c__serializervsserializer(results, s1s2d)
    else:
        report_section_c2c__serializervsall(results, s1s2d)


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_d1a(results,
                       s1s2d):
    """
        report_section_d1a()

        Sub-function of report() for report section "D1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle(
            "(D1a) Informations About The Machine ([italic]No Extensive Details[/italic])")

    mymachine(detailslevel=1)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_d1b(results,
                       s1s2d):
    """
        report_section_d1b()

        Sub-function of report() for report section "D1b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle(
            "(D1b) Informations About The Machine ([italic]Extensive Details[/italic])")

    mymachine(detailslevel=2)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
#   pylint: disable=unused-argument
def report_section_graphs(results,
                          s1s2d):
    """
        report_section_graphs()

        Sub-function of report() for report section "D1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if not trytoimport("matplotlib.pyplot"):
        msgerror(
            "(ERRORID022) Can't draw graphs: missing package 'matplotlib'. "
            "Either you install matplotlib (see https://matplotlib.org/), either "
            "- if you don't want to draw graphs - "
            "you remove keyword 'graphs' from the --report string. "
            "Try --verbosity=3 and check report file for more informations about --report string.")
        return

    # (pimydoc)GRAPHS_DESCRIPTION format
    # ⋅Use GRAPHS_DESCRIPTION to store the description of each graph created by the
    # ⋅report; each description is passed to hbar2png_resultshall(). Note that
    # ⋅len(GRAPHS_DESCRIPTION) gives the number of graphs to be created.
    # ⋅
    # ⋅- (str)attribute   : hbar2png_resultshall will read results.hall[attribute]
    # ⋅- (str)fmtstring   : format string to be applied to each value when printed
    # ⋅                     on the graph; e.g. '{0}' or '{0:.1f}'
    # ⋅- (int)value_coeff : each value will be multiplied by this number
    # ⋅- (str)unit        : x unit
    # ⋅- (str)title       : graph title
    # ⋅- (str)filename    : file name to be written
    for (attribute,
         fmtstring,
         value_coeff,
         unit,
         title,
         filename) in wisteria.globs.GRAPHS_DESCRIPTION:
        if results.hall_without_none_for_attribute(attribute):
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"About to create a new graph named '{filename}' ({normpath(filename)}).")
            hbar2png_resultshall(results.hall[attribute],
                                 filename,
                                 unit,
                                 title,
                                 fmtstring,
                                 value_coeff)
        else:
            # incoherent data: no graph.
            msgreport(f"Can't create graph '{filename}' for attribute '{attribute}' since "
                      "data are not fully available for all serializers.")
            if os.path.exists(filename):
                msgreport(f"About to delete ancient '{filename}' graph ({normpath(filename)}).")
                os.remove(filename)
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"results.hall['{attribute}'] = {results.hall[attribute]}")


# STR2REPORTSECTION has two goals:
# (1) translate a (str)report section name > list of corresponding functions
# (2) store all known keys accepted in --report.
#
#  globs.py:STR2REPORTSECTION_KEYS should be nothing but STR2REPORTSECTION.keys()
#
# Why those two variables ?
# Because the program needs to know STR2REPORTSECTION.keys() at step A
# before STR2REPORTSECTION has been initialized. Since this initialization
# requires modules that can't fit step A, we have to create a distinct list
# of keys.
#
# check_str2reportsection_keys() checks that keys from STR2REPORTSECTION and
# from STR2REPORTSECTION_KEYS are exactly the same.
STR2REPORTSECTION = {
        "titles": None,
        "graphs": (report_section_graphs,),
        "A": (report_section_a0,
              report_section_a1,
              report_section_a2,
              report_section_a3,
              report_section_a4,
              report_section_a5,),
        "A0": (report_section_a0,),
        "A1": (report_section_a1,),
        "A2": (report_section_a2,),
        "A3": (report_section_a3,),
        "A4": (report_section_a4,),
        "A5": (report_section_a5,),
        "B": (report_section_b1a,
              report_section_b1b,
              report_section_b1c,
              report_section_b1d,
              report_section_b2a,
              report_section_b2b,
              report_section_b3,),
        "B1": (report_section_b1a,
               report_section_b1b,
               report_section_b1c,
               report_section_b1d,),
        "B1a": (report_section_b1a,),
        "B1b": (report_section_b1b,),
        "B1c": (report_section_b1c,),
        "B1d": (report_section_b1d,),
        "B2": (report_section_b2a,
               report_section_b2b,),
        "B2a": (report_section_b2a,),
        "B2b": (report_section_b2b,),
        "B3": (report_section_b3,),
        "C": (report_section_c1a,
              report_section_c1b,
              report_section_c2a,
              report_section_c2b,
              report_section_c2c,),
        "C1": (report_section_c1a,
               report_section_c1b,),
        "C1a": (report_section_c1a,),
        "C1b": (report_section_c1b,),
        "C2": (report_section_c2a,
               report_section_c2b,
               report_section_c2c),
        "C2a": (report_section_c2a,),
        "C2b": (report_section_c2b,),
        "C2c": (report_section_c2c,),
        "D": (report_section_d1a,
              report_section_d1b,),
        "D1": (report_section_d1a,
               report_section_d1b),
        "D1a": (report_section_d1a,),
        "D1b": (report_section_d1b,),
}


def report(results,
           s1s2d):
    """
        report()

        Print an analyze of <results>.

        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A0      : command line arguments
        ⋅  - A1      : options used to create reports
        ⋅  - A2      : list of the serializers to be used because they have been selected
        ⋅  - A3      : list of the data objects to be used because they have been selected
        ⋅  - A4      : list of the planned transcodings
        ⋅  - A5      : what do the encoded strings look like? (basic types/demonstration_dataobj)
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅  - B3      : encoded string of all data objects and of all serializers
        ⋅* C         : conclusions
        ⋅  - C1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . C1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . C1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - C2      : conclusion: final text and data
        ⋅    . C2a   : conclusion: serializers (not sorted)
        ⋅    . C2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . C2c   : conclusion
        ⋅* D         : various informations
        ⋅  - D1      : informations about the machine
        ⋅    . D1a   : informations about the machine (no extensive details)
        ⋅    . D1b   : informations about the machine (extensive details)
        ⋅* graphs    : graphic visualizations
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
        o  s1s2d: ( (str)seria1,
                    (str)seria2,
                    (str)cmpdata         -> 'all', 'ini', 'cwc' or 'allbutcwc', cf read_cmpstring()
                  )
    """
    if wisteria.globs.ARGS.report.strip() == ";":
        raise WisteriaError(
            "(ERRORID018) Can't interpret report section which is empty. "
            f"Accepted keywords are {tuple(STR2REPORTSECTION.keys())} . "
            f"You may use stand alone shortcuts {tuple(REPORT_SHORTCUTS.keys())} "
            "but be sure to use this shortcut alone, with nothing else in the --report string. "
            "More informations in the documentation.")

    for report_section in wisteria.globs.ARGS.report.split(";"):
        report_section = report_section.strip()

        if report_section == "":
            pass
        elif report_section in STR2REPORTSECTION and STR2REPORTSECTION[report_section] is not None:
            for func in STR2REPORTSECTION[report_section]:
                func(results, s1s2d)
        elif report_section in STR2REPORTSECTION and STR2REPORTSECTION[report_section] is None:
            # special keywords (like 'titles') that don't match any function in <STR2REPORTSECTION>.
            pass
        elif report_section.strip() != "":
            raise WisteriaError(
                f"(ERRORID017) Can't interpret report section; "
                f"what is '{report_section}' ? args.report is '{wisteria.globs.ARGS.report}' . "
                f"Accepted keywords are {tuple(STR2REPORTSECTION.keys())} . "
                f"You may use stand alone shortcuts {tuple(REPORT_SHORTCUTS.keys())} "
                "but be sure to use this shortcut alone, with nothing else in the --report string. "
                "More informations in the documentation.")
