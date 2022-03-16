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

    o  compute_results(config, serializer1, serializer2, cmpdata)
    o  get_serializers_selection(serializer1, serializer2)
    o  get_data_selection(cmpdata, config)
    o  init_planned_transcodings(serializer1, serializer2, cmpdata, config, filterstr)
"""
from rich.console import Console
from rich.progress_bar import ProgressBar

import wisteria.data
import wisteria.globs
from wisteria.globs import VERBOSITY_NORMAL, VERBOSITY_DEBUG, VERBOSITY_DETAILS
from wisteria.globs import PROGRESSBAR_LENGTH
from wisteria.wisteriaerror import WisteriaError
from wisteria.msg import msgdebug, msginfo, msgerror
from wisteria.serializers import func_serialize
from wisteria.serializers_classes import SerializationResults
from wisteria.utils import strdigest
from wisteria.cwc.cwc_utils import is_a_cwc_name, moduleininame_to_modulefullrealname
from wisteria.cwc.cwc_utils import modulefullrealname_to_modulerealname
from wisteria.cwc.cwc_utils import is_this_an_appropriate_module_for_serializer
from wisteria.filterstr import parse_filterstr
from wisteria.helpmsg import help_cmdline_filter


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
        results = SerializationResults()

        planned_transcodings_number = len(wisteria.globs.PLANNED_TRANSCODINGS)

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
                                      total=planned_transcodings_number)
            console.show_cursor(False)
            progressbar_index = 0

        # ---- real work ------------------------------------------------------
        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo("Please wait until all required encodings/decodings have been computed.")

        # (pimydoc)PLANNED_TRANSCODINGS
        # ⋅a list:
        # ⋅    - (str)serializer,
        # ⋅    - (int)len(serializers)
        # ⋅    - (int)len(dataobjs)
        # ⋅
        # ⋅Initialized by results.py:init_planned_transcodings()
        for (transcoding_index,
             (serializer,
              data_name,
              fingerprint)) in enumerate(wisteria.globs.PLANNED_TRANSCODINGS):

            if serializer not in results:
                results[serializer] = {}

            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                if not is_a_cwc_name(data_name):
                    msgdebug(f"({transcoding_index+1}/{planned_transcodings_number}) "
                             "About to call transcoding functions "
                             f"for serializer='{serializer}' "
                             f"and data name='{data_name}' "
                             f"[{fingerprint}]")
                else:
                    msgdebug("About to call serialize/unserialize function "
                             f"for serializer='{serializer}' "
                             f"and (cwc) data name='{data_name}' "
                             f"[{fingerprint}]")
            results[serializer][data_name] = func_serialize(serializer,
                                                            data_name,
                                                            fingerprint)

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

            if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                # is serializer/data_name has been skipped, no results[serializer][data_name],
                # hence the following "if" statement:
                if data_name in results[serializer]:
                    msgdebug(f"result: {results[serializer][data_name]} "
                             f"[{fingerprint}]")

        # (pimydoc)progress bar
        # ⋅A progress bar is displayed only if verbosity is set to 1 (normal).
        # ⋅If verbosity is set to 0 (minimal), the progress bar is hidden since no
        # ⋅console output is authorized: it's important for scripts calling the
        # ⋅project from the outside.
        # ⋅If verbosity is set to 2 (details) or 3 (debug), the progress bar is hidden
        # ⋅in order to avoid mixing the progress bar with the text displayed while
        # ⋅computing the result, which is unpleasant to see.
        erase_progress_bar()

        if not results.finish_initialization():
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

        return results, None

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
        ⋅    - (int)len(serializers)
        ⋅    - (int)len(dataobjs)
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
                    # ⋅    - (int)len(serializers)
                    # ⋅    - (int)len(dataobjs)
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
                        # ⋅    - (int)len(serializers)
                        # ⋅    - (int)len(dataobjs)
                        # ⋅
                        # ⋅Initialized by results.py:init_planned_transcodings()
                        wisteria.globs.PLANNED_TRANSCODINGS.append((serializer,
                                                                    dataobj,
                                                                    fingerprint))

    except WisteriaError as exception:
        msgerror(f"(ERRORID041) Can't set PLANNED_TRANSCODINGS since an error occured: {exception}")
        return False, len(serializers), len(dataobjs)

    return True, len(serializers), len(dataobjs)
