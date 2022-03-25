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
    Wisteria project : wisteria/results.py

    Fonctions to compute results, especially compute_results().

    ___________________________________________________________________________

    o  average_raw_serializationresults(raw_results)
    o  compute_results(config, serializer1, serializer2, cmpdata)
    o  get_serializers_selection(serializer1, serializer2)
    o  get_data_selection(cmpdata, config)
    o  init_planned_transcodings(serializer1, serializer2, cmpdata, config, filterstr)
"""
import random
import statistics
import time
from rich.console import Console
from rich.progress_bar import ProgressBar

import wisteria.data
import wisteria.globs
from wisteria.globs import VERBOSITY_NORMAL, VERBOSITY_DEBUG, VERBOSITY_DETAILS
from wisteria.globs import PROGRESSBAR_LENGTH
from wisteria.wisteriaerror import WisteriaError
from wisteria.msg import msgdebug, msginfo, msgerror, msgwarning
from wisteria.serializers import func_serialize
from wisteria.serializers_classes import SerializationResults, SerializationResult
from wisteria.utils import strdigest, get_valid_filename
from wisteria.cwc.cwc_utils import is_a_cwc_name, moduleininame_to_modulefullrealname
from wisteria.cwc.cwc_utils import modulefullrealname_to_modulerealname
from wisteria.cwc.cwc_utils import is_this_an_appropriate_module_for_serializer
from wisteria.filterstr import parse_filterstr
from wisteria.helpmsg import help_cmdline_filter
from wisteria.reprfmt import fmt_nounplural
from wisteria.matplotgraphs import vbar2png_subdatagraphs
from wisteria.stats import remove_absurd_values


def average_raw_serializationresults(raw_results):
    """
        average_raw_serializationresults()

        Return a SerializationResults whose each element is a unique
        SerializationResult object.
        <raw_results>:
            SerializationResults[serializer][data_name] = [SerializationResult1,
                                                           SerializationResult2,
                                                           SerializationResult3, ...]

        the Returned value is something like:
            SerializationResults[serializer][data_name] = SerializationResult,

                SerializationResult being the average of SerializationResult1,
            SerializationResul2, SerializationResult3,...

        _______________________________________________________________________

        ARGUMENT: <raw_results> is a SerializationResults full of a list
                  of SerializationResult objects

        RETURNED VALUE:    (SerializationResults, None) if no error occured
                        or (None, (int)exit_code) if an error occured
    """
    ok = True
    res = SerializationResults()

    # let's fill <res>:
    for serializer in raw_results.serializers:
        for data_object in raw_results.dataobjs:
            # ---- fill _graphs_values__* ----
            _graphs_values__encoding_time = []
            _graphs_values__decoding_time = []
            _graphs_values__mem_usage = []
            for index, raw_serialization_result in enumerate(raw_results[serializer][data_object]):

                ok = True

                # Safeguards: for some attributes ('encoding_time', 'decoding_time', 'mem_usage'),
                #             we keep all values to compute later their means.
                _graphs_values__encoding_time.append(raw_serialization_result.encoding_time)
                _graphs_values__decoding_time.append(raw_serialization_result.decoding_time)
                _graphs_values__mem_usage.append(raw_serialization_result.mem_usage)

                # Safeguards: for the other attributes we just check that their value
                #             doesn't change.
                if index == 0:
                    encoded_object = raw_serialization_result.encoded_object
                    encoding_success = raw_serialization_result.encoding_success
                    encoding_strlen = raw_serialization_result.encoding_strlen
                    decoding_success = raw_serialization_result.decoding_success
                    reversibility = raw_serialization_result.reversibility
                elif raw_serialization_result.encoded_object != encoded_object:
                    msgwarning(
                        "(WARNINGID000) Incoherent result: 'encoded_object' changed "
                        f"for '{serializer}' x '{data_object}': "
                        f"'{raw_serialization_result.encoded_object}' != '{encoded_object}'")
                    ok = False
                elif raw_serialization_result.encoding_success != encoding_success:
                    msgwarning(
                        "(WARNINGID001) Incoherent result: 'encoding_success' changed "
                        f"for '{serializer}' x '{data_object}': "
                        f"'{raw_serialization_result.encoding_success}' != '{encoding_success}'")
                    ok = False
                elif raw_serialization_result.encoding_strlen != encoding_strlen:
                    msgwarning(
                        "(WARNINGID002) Incoherent result: 'encoding_strlen' changed "
                        f"for '{serializer}' x '{data_object}': "
                        f"'{raw_serialization_result.encoding_strlen}' != '{encoding_strlen}'")
                    ok = False
                elif raw_serialization_result.decoding_success != decoding_success:
                    msgwarning(
                        "(WARNINGID003) Incoherent result: 'decoding_success' changed "
                        f"for '{serializer}' x '{data_object}': "
                        f"'{raw_serialization_result.decoding_success}' != '{decoding_success}'")
                    ok = False
                elif raw_serialization_result.reversibility != reversibility:
                    msgwarning(
                        "(WARNINGID004) Incoherent result: 'reversibility' changed "
                        f"for '{serializer}' x '{data_object}': "
                        f"'{raw_serialization_result.reversibility}' != '{reversibility}'")
                    ok = False

            if not ok:
                continue

            # Safeguards: what if the results are ill-formed ?
            if not _graphs_values__encoding_time \
               or all(value is None for value in _graphs_values__encoding_time):
                msgwarning("(WARNINGID005) Incorrect 'encoding time' results for "
                           f"'{serializer}' x '{data_object}'. "
                           f"Returned problematic data are: {_graphs_values__encoding_time}")
                ok = False
            if not _graphs_values__decoding_time \
               or all(value is None for value in _graphs_values__decoding_time):
                msgwarning("(WARNINGID006) Incorrect 'decoding time' results for "
                           f"'{serializer}' x '{data_object}'. "
                           f"Returned problematic data are: {_graphs_values__decoding_time}")
                ok = False
            if not _graphs_values__mem_usage \
               or all(value is None for value in _graphs_values__mem_usage):
                msgwarning("(WARNINGID007) Incorrect 'mem usage' results for "
                           f"'{serializer}' x '{data_object}'. "
                           f"Returned problematic data are: {_graphs_values__mem_usage}")
                ok = False

            if not ok:
                continue

            # ---- remove absurd values ----
            _ok, _graphs_values__encoding_time = remove_absurd_values(_graphs_values__encoding_time)
            if not _ok:
                msgwarning("(WARNINGID008) "
                           f"Anomaly: too many absurd values detected in 'encoding time' series;"
                           f"'{serializer}' x '{data_object}'. "
                ok = False
            _ok, _graphs_values__decoding_time = remove_absurd_values(_graphs_values__decoding_time)
            if not _ok:
                msgwarning("(WARNINGID009) "
                           f"Anomaly: too many absurd values detected in 'decoding time' series;"
                           f"'{serializer}' x '{data_object}'. "
                ok = False
            ok, _graphs_values__mem_usage = remove_absurd_values(_graphs_values__mem_usage)
            if not ok:
                msgwarning("(WARNINGID010) "
                           f"Anomaly: too many absurd values detected in 'mem usage' series;"
                           f"'{serializer}' x '{data_object}'. "
                ok = False

            if not ok:
                continue

            # ---- sub data graphs ----
            # TODO
            #  verbosity=DETAILS+, expliciter ce qui suit ("About to create...")
            _filename = f'xyz__{serializer}__{data_object}.encodingtime.png'
            vbar2png_subdatagraphs(
                _graphs_values__encoding_time,
                f"{get_valid_filename(_filename)}",
                "second(s)",
                f"encoding time ('{serializer}' x '{data_object}')",
                "'{0:.1f}'",
                1)
            _filename = f'xyz__{serializer}__{data_object}.decodingtime.png'
            vbar2png_subdatagraphs(
                _graphs_values__decoding_time,
                f"{get_valid_filename(_filename)}",
                "second(s)",
                f"decoding time ('{serializer}' x '{data_object}')",
                "'{0:.1f}'",
                1)
            _filename = f'xyz__{serializer}__{data_object}.memusage.png'
            vbar2png_subdatagraphs(
                _graphs_values__mem_usage,
                f"{get_valid_filename(_filename)}",
                "byte(s)",
                f"mem usage ('{serializer}' x '{data_object}')",
                "'{0}'",
                1)

            averaged_serialization_result = SerializationResult()
            averaged_serialization_result.encoded_object = encoded_object
            averaged_serialization_result.encoding_success = encoding_success
            averaged_serialization_result.encoding_time = statistics.mean(_graphs_values__encoding_time)
            averaged_serialization_result.encoding_strlen = encoding_strlen
            averaged_serialization_result.decoding_success = decoding_success
            averaged_serialization_result.decoding_time = statistics.mean(_graphs_values__decoding_time)
            averaged_serialization_result.reversibility = reversibility
            averaged_serialization_result.mem_usage = statistics.mean(_graphs_values__mem_usage)

            if serializer not in res:
                res[serializer] = {}
            res[serializer][data_object] = averaged_serialization_result
            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                msgdebug(f"* average result for '{serializer}' x '{data_object}':")
                msgdebug(res[serializer][data_object])

    # to compute res.hall and so on:
    if not res.finish_initialization():
        msgerror("(ERRORID015) Incorrect data, the program has to stop.")

        # (pimydoc)exit codes
        # ⋅These exit codes try to take into account the standards, in particular this
        # ⋅one: https://docs.python.org/3/library/sys.html#sys.exit
        # ⋅
        # ⋅Please note that `os` constants like `os.EX_OK` as defined in Python doc
        # ⋅(see https://docs.python.org/3/library/os.html#process-management) are not
        # ⋅used for this project; these constants are only defined for Linux systems
        # ⋅and this project aims Windows/OSX systems.
        # ⋅
        # ⋅*    0: normal exit code
        # ⋅*       normal exit code after --help/--help2
        # ⋅*       normal exit code after --checkup
        # ⋅*       normal exit code after --downloadconfigfile
        # ⋅*       normal exit code after --mymachine
        # ⋅*       normal exit code (no data to handle)
        # ⋅*       normal exit code (no serializer to handle)
        # ⋅*    1: error, given config file can't be read (missing or ill-formed file)
        # ⋅*    2: error, ill-formed --cmp string
        # ⋅*    3: error, ill-formed --output string
        # ⋅*    4: error, missing required module
        # ⋅*    5: error: an inconsistency between the data has been detected
        # ⋅*    6: error: can't open/create report file
        # ⋅*  100: internal error, data can't be loaded
        # ⋅*  101: internal error, an error occured while computing the results
        # ⋅*  102: internal error, an error occured in main()
        # ⋅*  103: internal error, can't initialize PLANNED_TRANSCODINGS
        return None, 100

    return res, None


def compute_results():
    """
        compute_results()

        Create a SerializationResults object and try to fill it with all
        required encodings/decodings defined by PLANNED_TRANSCODINGS
        _______________________________________________________________________

        RETURNED VALUE:    (SerializationResults, None) if no error occured
                        or (None, (int)exit_code) if an error occured
    """
    def erase_progress_bar():
        """
            erase_progress_bar()

            Erase the progress bar so that it is possible to write text over
            the ancient progress bar.

            Show the cursor.

            (pimydoc)progress bar
            ⋅A progress bar is displayed only if verbosity is set to 1 (normal).
            ⋅If verbosity is set to 0 (minimal), the progress bar is hidden since no
            ⋅console output is authorized: it's important for scripts calling the
            ⋅project from the outside.
            ⋅If verbosity is set to 2 (details) or 3 (debug), the progress bar is hidden
            ⋅in order to avoid mixing the progress bar with the text displayed while
            ⋅computing the result, which is unpleasant to see.
        """
        if wisteria.globs.ARGS.verbosity == VERBOSITY_NORMAL:
            # the following lines make the progress bar disappear.
            # the next call to RICHCONSOLE.print() will overwrite the spaces that are about
            # to be added:
            if PROGRESSBAR_LENGTH is None:
                console.file.write(" "*console.width)
            else:
                console.file.write(" "*PROGRESSBAR_LENGTH)
            console.file.write("\r")

            console.show_cursor(True)

    try:
        raw_results = SerializationResults()

        # ---- PLANNED_TRANSCODINGS shuffle ? ----
        # TODO : format, pourquoi _ (bool/success) ?
        planned_transcodings = wisteria.globs.PLANNED_TRANSCODINGS[:]
        _, method_totaliterations, shuffleseed, method_parts = wisteria.globs.METHOD
        if shuffleseed:
            # yes,let's shuffle:
            random.Random(shuffleseed).shuffle(planned_transcodings)
            if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
                msginfo(f"planned transcodings have been shuffled (seed: {shuffleseed}).")

        planned_transcodings_number = len(planned_transcodings)

        # (pimydoc)progress bar
        # ⋅A progress bar is displayed only if verbosity is set to 1 (normal).
        # ⋅If verbosity is set to 0 (minimal), the progress bar is hidden since no
        # ⋅console output is authorized: it's important for scripts calling the
        # ⋅project from the outside.
        # ⋅If verbosity is set to 2 (details) or 3 (debug), the progress bar is hidden
        # ⋅in order to avoid mixing the progress bar with the text displayed while
        # ⋅computing the result, which is unpleasant to see.
        if wisteria.globs.ARGS.verbosity == VERBOSITY_NORMAL:
            console = Console()
            progressbar = ProgressBar(width=PROGRESSBAR_LENGTH,
                                      total=method_totaliterations*len(method_parts))
            console.show_cursor(False)
            progressbar_index = 0

        # ---- real work ------------------------------------------------------
        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo("Please wait until all required encodings/decodings have been computed.")

        for iteration in range(method_totaliterations):
            if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
                msginfo(f"Iteration #{iteration}/{method_totaliterations}.")

            for method_part in method_parts:

                # (pimydoc)progress bar
                # ⋅A progress bar is displayed only if verbosity is set to 1 (normal).
                # ⋅If verbosity is set to 0 (minimal), the progress bar is hidden since no
                # ⋅console output is authorized: it's important for scripts calling the
                # ⋅project from the outside.
                # ⋅If verbosity is set to 2 (details) or 3 (debug), the progress bar is hidden
                # ⋅in order to avoid mixing the progress bar with the text displayed while
                # ⋅computing the result, which is unpleasant to see.
                if wisteria.globs.ARGS.verbosity == VERBOSITY_NORMAL:
                    progressbar_index += 1
                    progressbar.update(progressbar_index)
                    console.print(progressbar)
                    console.file.write("\r")

                if method_part == "rp":
                    time.sleep(random.Random().uniform(0.0001, 0.2))
                    continue

                if method_part == "RP":
                    time.sleep(random.Random().uniform(1, 5))
                    continue

                if method_part == "p1":
                    time.sleep(1)
                    continue

                if method_part == "p10":
                    time.sleep(10)
                    continue

                if method_part == "p100":
                    time.sleep(100)
                    continue

                for (transcoding_index,
                     (serializer,
                      data_name,
                      fingerprint)) in enumerate(planned_transcodings):

                    if serializer not in raw_results:
                        raw_results[serializer] = {}

                    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                        if not is_a_cwc_name(data_name):
                            msgdebug(f"({transcoding_index+1}/{planned_transcodings_number}) "
                                     f"About to call {method_part} {fmt_nounplural('time', method_part)} the transcoding function "
                                     f"for '{serializer}' x '{data_name}' "
                                     f"[{fingerprint}]")
                        else:
                            msgdebug("About to call {fmt_nounplural('time', method_part)} the transcoding function "
                                     f"for '{serializer}' x (cwc)'{data_name}' "
                                     f"[{fingerprint}]")

                    for index in range(method_part):
                        if data_name not in raw_results[serializer]:
                            raw_results[serializer][data_name] = []
                        res_func = func_serialize(serializer,
                                                  data_name,
                                                  fingerprint)
                        raw_results[serializer][data_name].append(res_func)

                    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                        # is serializer/data_name has been skipped, no results[serializer][data_name],
                        # hence the following "if" statement:
                        if data_name in raw_results[serializer]:
                            msgdebug(f"* raw result(s) for '{serializer}' x '{data_name}' "
                                     f"[{fingerprint}]:")
                            for result_part in raw_results[serializer][data_name]:
                                msgdebug(f"  - {result_part}")

        # (pimydoc)progress bar
        # ⋅A progress bar is displayed only if verbosity is set to 1 (normal).
        # ⋅If verbosity is set to 0 (minimal), the progress bar is hidden since no
        # ⋅console output is authorized: it's important for scripts calling the
        # ⋅project from the outside.
        # ⋅If verbosity is set to 2 (details) or 3 (debug), the progress bar is hidden
        # ⋅in order to avoid mixing the progress bar with the text displayed while
        # ⋅computing the result, which is unpleasant to see.
        erase_progress_bar()

        raw_results.finish_initialization(partial=True)
        return average_raw_serializationresults(raw_results)

    except WisteriaError as exception:
        msgerror(f"An error occured: {exception}")

        # (pimydoc)exit codes
        # ⋅These exit codes try to take into account the standards, in particular this
        # ⋅one: https://docs.python.org/3/library/sys.html#sys.exit
        # ⋅
        # ⋅Please note that `os` constants like `os.EX_OK` as defined in Python doc
        # ⋅(see https://docs.python.org/3/library/os.html#process-management) are not
        # ⋅used for this project; these constants are only defined for Linux systems
        # ⋅and this project aims Windows/OSX systems.
        # ⋅
        # ⋅*    0: normal exit code
        # ⋅*       normal exit code after --help/--help2
        # ⋅*       normal exit code after --checkup
        # ⋅*       normal exit code after --downloadconfigfile
        # ⋅*       normal exit code after --mymachine
        # ⋅*       normal exit code (no data to handle)
        # ⋅*       normal exit code (no serializer to handle)
        # ⋅*    1: error, given config file can't be read (missing or ill-formed file)
        # ⋅*    2: error, ill-formed --cmp string
        # ⋅*    3: error, ill-formed --output string
        # ⋅*    4: error, missing required module
        # ⋅*    5: error: an inconsistency between the data has been detected
        # ⋅*    6: error: can't open/create report file
        # ⋅*  100: internal error, data can't be loaded
        # ⋅*  101: internal error, an error occured while computing the results
        # ⋅*  102: internal error, an error occured in main()
        # ⋅*  103: internal error, can't initialize PLANNED_TRANSCODINGS
        return None, 101


def get_serializers_selection(serializer1,
                              serializer2):
    """
        get_serializers_selection()

        Return a tuple of all serializers defined by (str)<serializer1>, (str)<serializer2>.
        _______________________________________________________________________

        ARGUMENTS:
        o    <serializer1> : value returned by read_cmpstring()
        o    <serializer2> : value returned by read_cmpstring()

        RETURNED VALUE: a tuple of str, i.e. all serializers defined by (str)<serializer1>,
                        (str)<serializer2>
    """
    res = set()

    if serializer1 == 'all':
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer1)

    if serializer2 == 'all':
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer2)

    return tuple(res)


def get_data_selection(cmpdata,
                       config):
    """
        get_data_selection()

        Return a tuple of the data objects names selected by the <config>.
        _______________________________________________________________________

        ARGUMENTS:
        o  cmpdata: (str)'all', 'ini', 'cwc' or 'allbutcwc'
        o  config:  (dict) dict returned by read_cfgfile()

        RETURNED VALUE: (tuple) a tuple of (str)data keys
    """
    res = []

    if cmpdata == 'all':
        res = tuple(wisteria.globs.DATA.keys())
    elif cmpdata == 'ini':
        if config["data selection"]["data selection"] == 'all':
            res = tuple(config["objects"].keys())
        elif config["data selection"]["data selection"] == 'only if yes':
            res = tuple(data_name for data_name in config["data objects"]
                        if config["data objects"][data_name])
        elif config["data selection"]["data selection"].startswith("data set/"):
            res = tuple(config["data sets"][config["data selection"]["data selection"]])
        else:
            raise WisteriaError(
                "(ERRORID020) "
                "Can't understand a value given to \\[data selection]'data selection': "
                f"what is '{config['data selection']['data selection']}' ? "
                "Known values are 'all', 'ini' and 'data set/xxx' "
                "where xxx is a string.")
    elif cmpdata == 'cwc':
        res = tuple(data_name for data_name in wisteria.globs.DATA
                    if is_a_cwc_name(data_name))
    elif cmpdata == 'allbutcwc':
        res = tuple(data_name for data_name in wisteria.globs.DATA
                    if not is_a_cwc_name(data_name))
    else:
        raise WisteriaError(
            "(ERRORID021) Can't understand a value given to the 'data' part in --cmp: "
            f"what is '{cmpdata}' ? "
            "Known values are 'all', 'cwc' and 'ini'. ")

    return res


def init_planned_transcodings(serializer1,
                              serializer2,
                              cmpdata,
                              config,
                              filterstr):
    """
        init_planned_transcodings()

        Initialize:
        - wisteria.globs.PLANNED_TRANSCODINGS
        - wisteria.globs.DISCARDED_SERIALIZERS
        - wisteria.globs.DISCARDED_DATA

        (pimydoc)PLANNED_TRANSCODINGS
        ⋅a list:
        ⋅    - (str)serializer,
        ⋅    - (str)data name,
        ⋅    - (str)fingerprint
        ⋅
        ⋅Initialized by results.py:init_planned_transcodings()
        _______________________________________________________________________

        ARGUMENTS:
        o  config               : None if no config file, otherwise the dict
                                  returned by read_cfgfile().
        o  (str)serializer1
        o  (str)serializer2
        o  (str)cmpdata         : 'all', 'ini', 'cwc' or 'allbutcwc'

        o  (str)filterstr       : ARGS.filter

        RETURNED VALUE: ((bool)success,
                         (int)len(serializers),
                         (int)len(dataobjs))

                        NB: about (bool)success: True may be returned even if len(serializers)==0 or
                            if len(dataobjs)==0.
    """
    (parse_filterstr_ok,
     wisteria.globs.DISCARDED_DATA,
     wisteria.globs.DISCARDED_SERIALIZERS) = parse_filterstr(filterstr)

    if not parse_filterstr_ok:
        msgerror("(ERRORID052) Can't set PLANNED_TRANSCODINGS "
                 "since an error occured while parsing the filter string.")
        msginfo("About --filter:")
        msginfo(help_cmdline_filter(details=True))
        return False, None, None

    try:
        wisteria.globs.PLANNED_TRANSCODINGS = []

        # serializers and data to be used through the tests:
        serializers = get_serializers_selection(serializer1, serializer2)
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"serializers to be used are: {serializers}")
        dataobjs = get_data_selection(cmpdata, config)

        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"data objs to be used are: {dataobjs}")

        for serializer in sorted(set(serializers)-set(wisteria.globs.DISCARDED_SERIALIZERS)):
            for dataobj in sorted(set(dataobjs)-set(wisteria.globs.DISCARDED_DATA)):
                fingerprint = strdigest(serializer+dataobj)

                if not is_a_cwc_name(dataobj):
                    # (pimydoc)PLANNED_TRANSCODINGS
                    # ⋅a list:
                    # ⋅    - (str)serializer,
                    # ⋅    - (str)data name,
                    # ⋅    - (str)fingerprint
                    # ⋅
                    # ⋅Initialized by results.py:init_planned_transcodings()
                    wisteria.globs.PLANNED_TRANSCODINGS.append((serializer,
                                                                dataobj,
                                                                fingerprint))
                else:
                    # data_name: e.g. "cwc.pgnreader.cwc_default.chessgames"
                    #                > "cwc.pgnreader.cwc_default.ChessGames"
                    data_name = moduleininame_to_modulefullrealname(dataobj)
                    # data_name__strmodule: e.g. "cwc.pgnreader.cwc_default"
                    data_name__strmodule = modulefullrealname_to_modulerealname(data_name)

                    # e.g. if data_name__strmodule is "cwc.pgnreader.cwc_default" and
                    #      if SERIALIZERS[serializer].cwc is "default" > True
                    #
                    # e.g. if data_name__strmodule is "cwc.pgnreader.cwc_default" and
                    #      if SERIALIZERS[serializer].cwc is "iaswn" > False - we skip.
                    if not is_this_an_appropriate_module_for_serializer(data_name__strmodule,
                                                                        serializer):
                        # we have to skip {serializer, data_name}.
                        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                            msgdebug(
                                f"We skip {serializer=} / {data_name=}, "
                                f"since {data_name=} is a cwc name and "
                                f"since data name module '{data_name__strmodule}' "
                                f"doesn't end with SERIALIZERS['{serializer}'].cwc="
                                f"'{wisteria.globs.SERIALIZERS[serializer].cwc}' .")
                    else:
                        # (pimydoc)PLANNED_TRANSCODINGS
                        # ⋅a list:
                        # ⋅    - (str)serializer,
                        # ⋅    - (str)data name,
                        # ⋅    - (str)fingerprint
                        # ⋅
                        # ⋅Initialized by results.py:init_planned_transcodings()
                        wisteria.globs.PLANNED_TRANSCODINGS.append((serializer,
                                                                    dataobj,
                                                                    fingerprint))

    except WisteriaError as exception:
        msgerror(f"(ERRORID041) Can't set PLANNED_TRANSCODINGS since an error occured: {exception}")
        return False, len(serializers), len(dataobjs)

    return True, len(serializers), len(dataobjs)
