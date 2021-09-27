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
    report.py

    report() function which prints the report.

    ___________________________________________________________________________

    o  cmpdata2prefix()
    o  ratio2phrase()

    o  report_section_a()
    o  report_section_b1a(results)
    o  report_section_b1b(results)
    o  report_section_b1c(results)
    o  report_section_b1d(results)
    o  report_section_b2a(results)
    o  report_section_b2b(results)
    o  report_section_c1a(results)
    o  report_section_c1b(results)
    o  report_section_c2b(results)
TODO : il en manque !
    o  report(results, s1s2d)
"""
import rich.table
from rich import print as rprint

import wisteria.globs
from wisteria.wisteriaerror import WisteriaError
from wisteria.utils import shortenedstr


def humanratio(ratio):
    """
        humanratio()

        Since ratio are difficult to understand when being smaller than 1, this function
        computes, if necessary, the inverse of <ratio> and returns it.

        _______________________________________________________________________

        ARGUMENT: (float)ratio, the ratio to be returned

        RETURNED VALUE: (float)ratio or (float)1/ratio.
    """
    if ratio < 1:
        return 1/ratio
    return ratio


def cmpdata2phrase(cmpdata):
    """
    TODO
    """
    assert cmpdata in ('all', 'ini', 'cwc')

    if cmpdata == "all":
        return "According to the tests " \
            "conducted on all data, "
    if cmpdata == "ini":
        return "According to the tests " \
            "conducted on the data defined in the configuration file "
    # cmpdata == "cwc"
    return "According to the tests " \
        "conducted on data of the 'comparing what is comparable' type "


def ratio2phrase(ratio,
                 base_string):
    """
        ratio2phrase()

        Convert a (float)<ratio> (e.g. 0.5, 2, 4...) to an adverbial phrase
        like "much slower".

        _______________________________________________________________________

        ARGUMENTS:
        o  (float)ratio
        o  (str)base_string: "slow/fast" or "long/short"

        RETURNED VALUE: (str)an adverbial phrase
    """
    assert base_string in ('slow/fast', 'long/short', 'large/small')

    if base_string == "slow/fast":
        if ratio > 10:
            expression = "extremly slower"
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
            expression = "extremly faster"

    elif base_string == "long/short":
        if ratio > 10:
            expression = "extremly longer"
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
            expression = "extremly shorter"

    elif base_string == "large/small":
        if ratio > 10:
            expression = "extremly larger"
        elif ratio > 2:
            expression = "much larger"
        elif ratio > 1.4:
            expression = "larger"
        elif ratio > 1.1:
            expression = "slightly larger"
        elif ratio > 0.9:
            expression = "slightly smaller"
        elif ratio > 0.5:
            expression = "smaller"
        elif ratio > 0.1:
            expression = "much smaller"
        else:
            expression = "extremly smaller"

    return expression


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_a1(results,
                      s1s2d):
    """
        report_section_a1()

        Sub-function of report() for report section "A1"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](A1) REPORT with --cmp set to "
               f"'[italic]{wisteria.globs.ARGS.cmp}[/italic]'[/bold white on blue]")
        rprint()


def report_section_a2(results,
                      s1s2d):
    """
        report_section_a2()

        Sub-function of report() for report section "A2"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    from wisteria.serializers import SERIALIZERS

    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](A2) List of serializers to be used"
               "[/bold white on blue]")
        rprint()

    for serializer in SERIALIZERS.values():
        rprint("  - ", serializer.simple_repr())
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_a3(results,
                      s1s2d):
    """
        report_section_a3()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    from wisteria.data import DATA

    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](A3) List of data objects to be used"
               "[/bold white on blue]")
        rprint()

    for dataobj_name, dataobj_value in DATA.items():
        rprint("  - ", dataobj_name, ":", shortenedstr(repr(dataobj_value)))
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1a(results,
                       s1s2d):
    """
        report_section_b1a()

        Sub-function of report() for report section "B1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](B1a) full details: "
               "serializer * data object[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer/data object", width=25)
    table.add_column("enc. ok ?", width=12)
    table.add_column("enc. time", width=10)
    table.add_column("jsonstr. len.", width=13)
    table.add_column("dec. ok ?", width=12)
    table.add_column("dec. time", width=10)
    table.add_column("enc ⇆ dec ?", width=12)

    for serializer in results.serializers:
        table.add_row("[yellow]" + serializer + ":" + "[/yellow]")
        for dataobj in results.dataobjs:
            table.add_row(
                "> " + "[bold white]" + dataobj + "[/bold white]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time"),
                results.repr_attr(serializer, dataobj, "encoding_strlen"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time"),
                results.repr_attr(serializer, dataobj, "similarity"))
    rprint(table)
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1b(results,
                       s1s2d):
    """
        report_section_b1b()

        Sub-function of report() for report section "B1b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](B1b) full details: serializers[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer", width=25)
    table.add_column(f"enc. ok ? (max={results.dataobjs_number})", width=12)
    table.add_column("Σ enc. time", width=10)
    table.add_column("Σ jsonstr. len.", width=13)
    table.add_column(f"dec. ok ? (max={results.dataobjs_number})", width=12)
    table.add_column("Σ dec. time", width=10)
    table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

    for serializer in results.serializers:
        table.add_row(
            f"[yellow]{serializer}[/yellow]",
            f"{results.ratio_encoding_success(serializer=serializer)}",
            f"{results.total_encoding_time(serializer=serializer)}",
            f"{results.total_encoding_strlen(serializer=serializer)}",
            f"{results.ratio_decoding_success(serializer=serializer)}",
            f"{results.total_decoding_time(serializer=serializer)}",
            f"{results.ratio_similarity(serializer=serializer)}",
        )
    rprint(table)
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1c(results,
                       s1s2d):
    """
        report_section_b1c()

        Sub-function of report() for report section "B1c"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](B1c) full details: "
               "serializers, hall of fame[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("#", width=2)
    table.add_column(f"enc. ok ? (max={results.dataobjs_number})", width=15)
    table.add_column("Σ enc. time", width=10)
    table.add_column("Σ jsonstr. len.", width=13)
    table.add_column(f"dec. ok ? (max={results.dataobjs_number})", width=15)
    table.add_column("Σ dec. time", width=10)
    table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

    for index in range(results.serializers_number):
        table.add_row(
            f"{index+1}",
            f"{results.get_halloffame('encoding_success', index)}",
            f"{results.get_halloffame('encoding_time', index)}",
            f"{results.get_halloffame('encoding_strlen', index)}",
            f"{results.get_halloffame('decoding_success', index)}",
            f"{results.get_halloffame('decoding_time', index)}",
            f"{results.get_halloffame('similarity', index)}",
        )

    rprint(table)
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1d(results,
                       s1s2d):
    """
        report_section_b1d()

        Sub-function of report() for report section "B1d"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](B1d) full details: "
               "serializer <S> can't handle <dataobj>[/bold white on blue]")
    for serializer in results.serializers:
        _list = tuple(dataobj for dataobj in results[serializer]
                      if not results[serializer][dataobj].similarity)
        if not _list:
            rprint(f"* [yellow]({serializer})[/yellow] "
                   "There's no data object that serializer "
                   f"'[yellow]{serializer}[/yellow]' can't handle.")
        else:
            rprint(f"* [yellow]({serializer})[/yellow] "
                   f"Serializer '[yellow]{serializer}[/yellow]' "
                   "can't handle the following data objects:")
            for dataobj in _list:
                rprint("  - ", "[bold white]" + dataobj + "[/bold white]")
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b2a(results,
                       s1s2d):
    """
        report_section_b2a()

        Sub-function of report() for report section "B2a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](B2a) full details: "
               "data object * serializer[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object/serializer", width=25)
    table.add_column("enc. ok ?", width=12)
    table.add_column("enc. time", width=10)
    table.add_column("jsonstr. len.", width=13)
    table.add_column("dec. ok ?", width=12)
    table.add_column("dec. time", width=10)
    table.add_column("enc ⇆ dec ?", width=12)

    for dataobj in results.dataobjs:
        table.add_row("[bold white]" + dataobj + ":" + "[/bold white]")
        for serializer in results.serializers:
            table.add_row(
                "> " + "[yellow]" + serializer + "[/yellow]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time"),
                results.repr_attr(serializer, dataobj, "encoding_strlen"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time"),
                results.repr_attr(serializer, dataobj, "similarity")
            )
    rprint(table)
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b2b(results,
                       s1s2d):
    """
        report_section_b2b()

        Sub-function of report() for report section "B2b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](B2b) full details: data objects[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object", width=25)
    table.add_column(f"enc. ok ? (max={results.serializers_number})", width=12)
    table.add_column("Σ enc. time", width=10)
    table.add_column("Σ jsonstr. len.", width=13)
    table.add_column(f"dec. ok ? (max={results.serializers_number})", width=12)
    table.add_column("Σ dec. time", width=10)
    table.add_column(f"enc ⇆ dec ? (max={results.serializers_number})", width=12)

    for dataobj in results.dataobjs:
        table.add_row(
            f"[bold white]{dataobj}[/bold white]",
            f"{results.ratio_encoding_success(dataobj=dataobj)}",
            f"{results.total_encoding_time(dataobj=dataobj)}",
            f"{results.total_encoding_strlen(dataobj=dataobj)}",
            f"{results.ratio_decoding_success(dataobj=dataobj)}",
            f"{results.total_decoding_time(dataobj=dataobj)}",
            f"{results.ratio_similarity(dataobj=dataobj)}",
        )
    rprint(table)
    rprint()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_c1a(results,
                       s1s2d):
    """
        report_section_c1a()

        Sub-function of report() for report section "C1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](C1a) full details: "
               "serializer * data object (base 100)[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer/data object", width=25)
    table.add_column("enc. ok ?", width=12)

    if base100 := results.get_base('encoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_time')
        table.add_column(f"enc. time (base 100 = {result})", width=10)
    else:
        table.add_column("enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results.get_base('encoding_strlen'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_strlen')
        table.add_column(f"jsonstr. len. (base 100 = {result})", width=13)
    else:
        table.add_column("jsonstr. len. [red](NO BASE 100)[/red]",
                         width=13)

    table.add_column("dec. ok ?", width=12)

    if base100 := results.get_base('decoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='decoding_time')
        table.add_column(f"dec. time (base 100 = {result})", width=10)
    else:
        table.add_column("dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column("enc ⇆ dec ?", width=12)

    for serializer in results.serializers:
        table.add_row("[yellow]" + serializer + ":" + "[/yellow]")
        for dataobj in results.dataobjs:
            table.add_row(
                "> " + "[bold white]" + dataobj + "[/bold white]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time", output="base100"),
                results.repr_attr(serializer, dataobj, "encoding_strlen", output="base100"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time", output="base100"),
                results.repr_attr(serializer, dataobj, "similarity"))
    rprint(table)
    rprint()


def report_section_c1b(results,
                       s1s2d):
    """
        report_section_c1b()

        Sub-function of report() for report section "C1b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](C1b) full details: "
               "serializers (base 100)[/bold white on blue]")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer", width=25)
    table.add_column(f"enc. ok ? (max={results.dataobjs_number})", width=12)
    if base100 := results.get_serializers_base('encoding_time'):
        table.add_column("Σ enc. time "
                         f"(base 100 = {results.total_encoding_time(serializer=base100)})",
                         width=10)
    else:
        table.add_column("Σ enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results.get_serializers_base('encoding_strlen'):
        table.add_column("Σ jsonstr. len. "
                         f"(base 100 = {results.total_encoding_strlen(serializer=base100)})",
                         width=13)
    else:
        table.add_column("Σ jsonstr. len. [red](NO BASE 100)[/red]", width=13)

    table.add_column(f"dec. ok ? (max={results.dataobjs_number})", width=12)

    if base100 := results.get_serializers_base('decoding_time'):
        table.add_column("Σ dec. time "
                         f"(base 100 = {results.total_decoding_time(serializer=base100)})",
                         width=10)
    else:
        table.add_column("Σ dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

    for serializer in results.serializers:
        table.add_row(
            f"[yellow]{serializer}[/yellow]",
            f"{results.ratio_encoding_success(serializer=serializer)}",
            f"{results.total_encoding_time(serializer=serializer, output='base100')}",
            f"{results.total_encoding_strlen(serializer=serializer, output='base100')}",
            f"{results.ratio_decoding_success(serializer=serializer)}",
            f"{results.total_decoding_time(serializer=serializer, output='base100')}",
            f"{results.ratio_similarity(serializer=serializer)}",
        )
    rprint(table)
    rprint()


def report_section_c2a(results,
                       s1s2d):
    """
        report_section_c2a()

        Sub-function of report() for report section "C2a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](C2a) full details: "
               "data object * serializer (base 100)[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object/serializer", width=25)

    table.add_column("enc. ok ?", width=12)

    if base100 := results.get_base('encoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_time')
        table.add_column(f"enc. time (base 100 = {result})", width=10)
    else:
        table.add_column("enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results.get_base('encoding_strlen'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_strlen')
        table.add_column(f"jsonstr. len. (base 100 = {result})", width=13)
    else:
        table.add_column("jsonstr. len. [red](NO BASE 100)[/red]",
                         width=13)

    table.add_column("dec. ok ?", width=12)

    if base100 := results.get_base('decoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='decoding_time')
        table.add_column(f"dec. time (base 100 = {result})", width=10)
    else:
        table.add_column("dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column("enc ⇆ dec ?", width=12)

    for dataobj in results.dataobjs:
        table.add_row("[bold white]" + dataobj + ":" + "[/bold white]")
        for serializer in results.serializers:
            table.add_row(
                "> " + "[yellow]" + serializer + "[/yellow]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time", output='base100'),
                results.repr_attr(serializer, dataobj, "encoding_strlen", output='base100'),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time", output='base100'),
                results.repr_attr(serializer, dataobj, "similarity")
            )
    rprint(table)
    rprint()


def report_section_c2b(results,
                       s1s2d):
    """
        report_section_c2b()

        Sub-function of report() for report section "C2b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](C2b) full details: "
               "data objects (base 100)[/bold white on blue]")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object", width=25)
    table.add_column(f"enc. ok ? (max={results.serializers_number})", width=12)

    if base100 := results.get_dataobjs_base('encoding_time'):
        table.add_column("Σ enc. time "
                         f"(base 100 = {results.total_encoding_time(dataobj=base100)})",
                         width=10)
    else:
        table.add_column("Σ enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results.get_dataobjs_base('encoding_strlen'):
        table.add_column("Σ jsonstr. len. "
                         f"(base 100 = {results.total_encoding_strlen(dataobj=base100)})",
                         width=13)
    else:
        table.add_column("Σ jsonstr. len. [red](NO BASE 100)[/red]", width=13)

    table.add_column(f"dec. ok ? (max={results.serializers_number})", width=12)

    if base100 := results.get_dataobjs_base('decoding_time'):
        table.add_column("Σ dec. time "
                         f"(base 100 = {results.total_decoding_time(dataobj=base100)})",
                         width=10)
    else:
        table.add_column("Σ dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column(f"enc ⇆ dec ? (max={results.serializers_number})", width=12)

    for dataobj in results.dataobjs:
        table.add_row(
            f"[bold white]{dataobj}[/bold white]",
            f"{results.ratio_encoding_success(dataobj=dataobj)}",
            f"{results.total_encoding_time(dataobj=dataobj, output='base100')}",
            f"{results.total_encoding_strlen(dataobj=dataobj, output='base100')}",
            f"{results.ratio_decoding_success(dataobj=dataobj)}",
            f"{results.total_decoding_time(dataobj=dataobj, output='base100')}",
            f"{results.ratio_similarity(dataobj=dataobj)}",
        )
    rprint(table)
    rprint()


def report_section_d1a(results,
                       s1s2d):
    """
        report_section_d1a()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    def show(serializer,
             data):
        """
            show()

            Print the message for serializer (str)<serializer> and for cmp data <data>.

            ___________________________________________________________________

            ARGUMENTS:
            o  (str)serializer
            o  (str)data              -> "all" or "ini" or "cwc", cf read_cmpstring()
        """
        _list = []
        for dataobj_name in DATA:
            if results[serializer][dataobj_name].similarity:
                _list.append(dataobj_name)

        if not DATA:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   "no data objects may be used: therefore there's no conclusion about the objects "
                   f"data serializer [yellow]'{serializer}'[/yellow] can handle.")
        elif not _list:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   "there's no data object "
                   f"among the {len(DATA)} used data objects "
                   f"that serializer [yellow]'{serializer}'[/yellow] can handle (0%).")
        elif len(_list) == 1:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   f"[yellow]'{serializer}'[/yellow] can handle one data object "
                   f"among {len(DATA)} ({100*len(_list)/len(DATA)}%), namely:")
            rprint("; ".join("'"+dataobj+"'" for dataobj in _list))
        else:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   f"[yellow]'{serializer}'[/yellow] can handle {len(_list)} data objects "
                   f"among {len(DATA)} ({100*len(_list)/len(DATA)}%), namely:")
            rprint("; ".join("'"+dataobj+"'" for dataobj in _list))

    from wisteria.data import DATA
    from wisteria.serializers import SERIALIZERS

    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](D1a) conclusion: data objects handled by the serializer(s)"
               "[/bold white on blue]")
        rprint()

    serializer1, serializer2, data = s1s2d
    if serializer1 != "all":
        show(serializer1, data)
        rprint()
    if serializer2 != "all":
        show(serializer2, data)
        rprint()

    # Other serializers, leaving apart <serializer1> and <serializer2> ?
    _serializers = list(SERIALIZERS.keys())
    if serializer1 != "all":
        _serializers.remove(serializer1)
    if serializer2 != "all":
        _serializers.remove(serializer2)
    if _serializers and (serializer1 == "all" or serializer2 == "all"):
        rprint("[bold]Other serializers:[/bold]")
        for __serializer in _serializers:
            show(__serializer, data)
        rprint()


def report_section_d1b(results,
                       s1s2d):
    """
        report_section_d1b()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    def show(serializer,
             data):
        """
            show()

            Print the message for serializer (str)<serializer> and for cmp data <data>.

            ___________________________________________________________________

            ARGUMENTS:
            o  (str)serializer
            o  (str)data              -> "all" or "ini" or "cwc", cf read_cmpstring()
        """
        _list = []
        for dataobj_name in DATA:
            if not results[serializer][dataobj_name].similarity:
                _list.append(dataobj_name)

        if not DATA:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   "no data objects may be used: therefore there's no conclusion about the objects "
                   f"data serializer [yellow]'{serializer}'[/yellow] can't handle.")
        elif not _list:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   "there's no data object "
                   f"among the {len(DATA)} used data objects "
                   f"that serializer [yellow]'{serializer}'[/yellow] can't handle (0%).")
        elif len(_list) == 1:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   f"[yellow]'{serializer}'[/yellow] can't handle one data object "
                   f"among {len(DATA)} ({100*len(_list)/len(DATA)}%), namely:")
            rprint("; ".join("'[bold white]"+dataobj+"/[bold white]'" for dataobj in _list))
        else:
            rprint(f"[yellow]'{serializer}'[/yellow]: "
                   f"{cmpdata2phrase(data)}"
                   f"[yellow]'{serializer}'[/yellow] can't handle {len(_list)} data objects "
                   f"among {len(DATA)} ({100*len(_list)/len(DATA)}%), namely:")
            rprint("; ".join("'[bold white]"+dataobj+"[/bold white]'" for dataobj in _list))

    from wisteria.data import DATA
    from wisteria.serializers import SERIALIZERS

    if "titles;" in wisteria.globs.ARGS.report:
        rprint(
            "[bold white on blue](D1b) conclusion: data objects NOT handled by the serializer(s)"
            "[/bold white on blue]")
        rprint()

    serializer1, serializer2, data = s1s2d
    if serializer1 != "all":
        show(serializer1, data)
        rprint()
    if serializer2 != "all":
        show(serializer2, data)
        rprint()

    # Other serializers, leaving apart <serializer1> and <serializer2> ?
    _serializers = list(SERIALIZERS.keys())
    if serializer1 != "all":
        _serializers.remove(serializer1)
    if serializer2 != "all":
        _serializers.remove(serializer2)
    if _serializers and (serializer1 == "all" or serializer2 == "all"):
        rprint("[bold]Other serializers:[/bold]")
        for __serializer in _serializers:
            show(__serializer, data)
        rprint()


def report_section_d2a(results,
                       s1s2d):
    """
        report_section_d2a()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](D2a) conclusion: "
               "serializers (not sorted)[/bold white on blue]")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer", width=25)
    table.add_column("Σ jsonstr. len.", width=13)
    table.add_column("Σ enc.+dec. time", width=13)
    table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

    serializer1, serializer2, _ = s1s2d
    _serializers = []
    if serializer1 != "all":
        _serializers.append(serializer1)
    if serializer2 != "all":
        _serializers.append(serializer2)
    _serializers.append("-")
    for serializer in results.serializers:
        if serializer not in _serializers:
            _serializers.append(serializer)
    if _serializers[-1] == "-":
        # TODO
        # nous supprimons ce "-" inutile: il n'y aura pas de serializers placé après.
        _serializers.pop()

    for serializer in _serializers:
        if serializer != "-":
            table.add_row(
                f"[yellow]{serializer}[/yellow]",
                f"{results.total_encoding_strlen(serializer=serializer)}",
                f"{results.total_encoding_plus_decoding_time(serializer=serializer)}",
                f"{results.ratio_similarity(serializer=serializer)}")
        else:
            table.add_row(
                "-",
                "-",
                "-",
                "-")

    rprint(table)
    rprint()


def report_section_d2b(results,
                       s1s2d):
    """
        report_section_d2b()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue]"
               "(D2b) "
               "conclusion: overall score based on 3 points "
               "(Σ jsonstr.len./Σ enc.+dec. time/enc ⇆ dec)"
               "[/bold white on blue]")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer", width=25)
    table.add_column("overall score", width=13)

    serializer1, serializer2, _ = s1s2d
    _serializers = []
    if serializer1 != "all":
        _serializers.append(serializer1)
    if serializer2 != "all":
        _serializers.append(serializer2)
    _serializers.append("-")
    for serializer in results.serializers:
        if serializer not in _serializers:
            _serializers.append(serializer)
    if _serializers[-1] == "-":
        # TODO
        # nous supprimons ce "-" inutile: il n'y aura pas de serializers placé après.
        _serializers.pop()

    for serializer in _serializers:
        if serializer != "-":
            table.add_row(
                f"[yellow]{serializer}[/yellow]",
                f"{results.overallscores[serializer]}")
        else:
            table.add_row(
                "-",
                "-")

    rprint(table)
    rprint()


def report_section_d2c(results,
                       s1s2d):
    """
        report_section_d2c()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        rprint("[bold white on blue](D2c) conclusion[/bold white on blue]")

    serializer1, serializer2, data = s1s2d

    text = [cmpdata2phrase(data), ]

    if serializer1 != "all" and serializer2 != "all":
        # ---- encoding/decoding time -----------------------------------------
        total_encoding_time_ratio = \
            results.total_encoding_plus_decoding_time(serializer=serializer1, output='value') \
            / results.total_encoding_plus_decoding_time(serializer=serializer2,
                                                        output='value')

        if total_encoding_time_ratio == 1:
            text.append(f"[yellow]{serializer1}[/yellow] "
                        f"and [yellow]{serializer2}[/yellow] "
                        "seem to require exactly the same time to encode and decode; ")
        else:
            text.append(f"[yellow]{serializer1}[/yellow] "
                        f"is {ratio2phrase(total_encoding_time_ratio, 'slow/fast')} "
                        f"(by a factor of {humanratio(total_encoding_time_ratio):.3f})"
                        " than "
                        f"[yellow]{serializer2}[/yellow] "
                        "to encode and decode; ")

        # ---- total_encoding_strlen -----------------------------------------
        total_encoding_strlen_ratio = \
            results.total_encoding_strlen(serializer=serializer1, output='value') \
            / results.total_encoding_strlen(serializer=serializer2,
                                            output='value')

        if total_encoding_strlen_ratio == 1:
            text.append(f"[yellow]{serializer1}[/yellow] "
                        f"and [yellow]{serializer2}[/yellow] "
                        "seem to produce strings that have exactly the same size; ")
        else:
            text.append("strings produced by "
                        f"[yellow]{serializer1}[/yellow] "
                        f"are {ratio2phrase(total_encoding_strlen_ratio, 'long/short')} "
                        f"(by a factor of {humanratio(total_encoding_strlen_ratio):.3f})"
                        " than "
                        f"strings produced by [yellow]{serializer2}[/yellow]; ")

        # ---- ratio_similarity -----------------------------------------------
        similarity_ratio = \
            results.ratio_similarity(serializer=serializer1, output='value') \
            / results.ratio_similarity(serializer=serializer2,
                                       output='value')

        if similarity_ratio == 1:
            text.append(f"[yellow]{serializer1}[/yellow] "
                        f"and [yellow]{serializer2}[/yellow] "
                        "seem to have exactly the same data coverage.")
        else:
            text.append(f"[yellow]{serializer1}[/yellow]'s coverage "
                        f"is {ratio2phrase(similarity_ratio, 'large/small')} "
                        f"(by a factor of {humanratio(similarity_ratio):.3f})"
                        " than "
                        f"[yellow]{serializer2}[/yellow]'s coverage.")

    else:
        # TODO serializer servant de référence ?
        if serializer1 != "all":
            serializer = serializer1
        else:
            serializer = serializer2
        rank = results.get_overallscore_rank(serializer)
        text.append(f"[yellow]{serializer}[/yellow]"
                    f" is ranked #{rank} among {len(results.serializers)} serializers(¹)")
        text.append(". ")

        for attribute in ("encoding_strlen",
                          "encoding_plus_decoding_time",
                          "similarity",
                          ):
            subtext = []
            _less, _more = results.comparison_inside_halloffame(serializer, attribute)

            if attribute == "encoding_strlen":
                if not _less:
                    subtext.append(
                        "There's no serializer that produces longer strings than "
                        f"[yellow]{serializer}[/yellow] ")
                elif len(_less) == 1:
                    subtext.append(
                        f"Only [yellow]{_less[0]}[/yellow] produces longer string than "
                        f"[yellow]{serializer}[/yellow] ")
                else:
                    subtext.append(
                        f"There are {len(_less)} serializers "
                        "(namely "
                        f"{'; '.join(f'[yellow]{_serializer}[/yellow]' for _serializer in _less)}) "
                        f"that produce longer strings than [yellow]{serializer}[/yellow]")

                subtext.append(" and ")

                if not _more:
                    subtext.append(
                        "there's no serializer that produces shorter strings than "
                        f"[yellow]{serializer}[/yellow]")
                elif len(_more) == 1:
                    subtext.append(
                        f"only [yellow]{_more[0]}[/yellow] produces shorter string than "
                        f"[yellow]{serializer}[/yellow]")
                else:
                    subtext.append(
                        f"there are {len(_more)} serializers "
                        "(namely "
                        f"{'; '.join(f'[yellow]{_serializer}[/yellow]' for _serializer in _more)}) "
                        f"that produce shorter strings than [yellow]{serializer}[/yellow]")

                subtext.append(". ")

            elif attribute == "encoding_plus_decoding_time":
                if not _less:
                    subtext.append(
                        "There's no serializer slower than "
                        f"[yellow]{serializer}[/yellow] ")
                elif len(_less) == 1:
                    subtext.append(
                        f"Only [yellow]{_less[0]}[/yellow] is slower than "
                        f"[yellow]{serializer}[/yellow] ")
                else:
                    subtext.append(
                        f"There are {len(_less)} serializers "
                        "(namely "
                        f"{'; '.join(f'[yellow]{_serializer}[/yellow]' for _serializer in _less)}) "
                        f"that are slower than [yellow]{serializer}[/yellow]")

                subtext.append(" and ")

                if not _more:
                    subtext.append(
                        "there's no serializer that is faster than "
                        f"[yellow]{serializer}[/yellow]")
                elif len(_more) == 1:
                    subtext.append(
                        f"only [yellow]{_more[0]}[/yellow] is faster than "
                        f"[yellow]{serializer}[/yellow]")
                else:
                    subtext.append(
                        f"there are {len(_more)} serializers "
                        "(namely "
                        f"{'; '.join(f'[yellow]{_serializer}[/yellow]' for _serializer in _more)}) "
                        f"that are faster than [yellow]{serializer}[/yellow]")

                subtext.append(". ")

            elif attribute == "similarity":
                if not _less:
                    subtext.append(
                        "There's no serializer that covers less than "
                        f"[yellow]{serializer}[/yellow] ")
                elif len(_less) == 1:
                    subtext.append(
                        f"Only [yellow]{_less[0]}[/yellow] covers less than "
                        f"[yellow]{serializer}[/yellow] ")
                else:
                    subtext.append(
                        f"There are {len(_less)} serializers "
                        "(namely "
                        f"{'; '.join(f'[yellow]{_serializer}[/yellow]' for _serializer in _less)}) "
                        f"that covers less than [yellow]{serializer}[/yellow]")

                subtext.append(" and ")

                if not _more:
                    subtext.append(
                        "there's no serializer that covers better than "
                        f"[yellow]{serializer}[/yellow]")
                elif len(_more) == 1:
                    subtext.append(
                        f"only [yellow]{_more[0]}[/yellow] covers better than "
                        f"[yellow]{serializer}[/yellow]")
                else:
                    subtext.append(
                        f"there are {len(_more)} serializers "
                        "(namely "
                        f"{'; '.join(f'[yellow]{_serializer}[/yellow]' for _serializer in _more)}) "
                        f"that covers better than [yellow]{serializer}[/yellow]")

                subtext.append(". ")

            text.append("".join(subtext))

    text.append("\n\n")
    text.append("(¹) a rank based on 3 points: Σ jsonstr.len./Σ enc.+dec. time/enc ⇆ dec")

    rprint("".join(text))
    rprint()


def report(results,
           s1s2d):
    """
        report()

        Print an analyze of <results>.

        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)data            -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    str2reportsection = {
        "A": (report_section_a1,
              report_section_a2,
              report_section_a3,),
        "A1": (report_section_a1,),
        "A2": (report_section_a2,),
        "A3": (report_section_a3,),
        "B": (report_section_b1a,
              report_section_b1b,
              report_section_b1c,
              report_section_b2a,
              report_section_b2b,),
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
        "C": (report_section_c1a,
              report_section_c1b,
              report_section_c2a,
              report_section_c2b,),
        "C1": (report_section_c1a,
               report_section_c1b,),
        "C1a": (report_section_c1a,),
        "C1b": (report_section_c1b,),
        "C2": (report_section_c2b,),
        "C2a": (report_section_c2a,),
        "C2b": (report_section_c2b,),
        "D": (report_section_d1a,
              report_section_d1b,
              report_section_d2a,
              report_section_d2b,
              report_section_d2c,),
        "D1": (report_section_d1a,
               report_section_d1b,),
        "D1a": (report_section_d1a,),
        "D1b": (report_section_d1b,),
        "D2": (report_section_d2a,
               report_section_d2b,
               report_section_d2c),
        "D2a": (report_section_d2a,),
        "D2b": (report_section_d2b,),
        "D2c": (report_section_d2c,),
        }

    for report_section in wisteria.globs.ARGS.report.split(";"):
        if report_section in str2reportsection:
            for func in str2reportsection[report_section]:
                func(results, s1s2d)
        elif report_section in ("titles,"):
            # special keywords that don't match any function in <str2reportsection>.
            pass
        elif report_section.strip() != "":
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRORIDXXX
            # ⋅- checkup messages start with *
            raise WisteriaError(
                f"(ERRORID017) Can't interpret report section; "
                f"what is '{report_section}' ? args.report is '{wisteria.globs.ARGS.report}' .")
