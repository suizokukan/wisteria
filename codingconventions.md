Wisteria / coding conventions (v. 1)
====================================

before pushing
--------------

`$ ./tests.sh`
    
`$ ./code_quality.sh`

if README.md has been modified:
`readmemd2txt --pyinitfile > wisteria/__init__.py`

if the version number (defined in wisteria/aboutproject.py) has been modified:
`$ ./propagate_versionnumber.py`

pimydoc and its forbidden character
-----------------------------------
A large part of the doc relies on `pimydoc` which uses a special
character that must never appear in the code. Use chr(0x22C5) instead.


functions/methods
-----------------

DO:
```
def fmt_list(listitems,
             func=None):
```     

DON'T:
```
def fmt_list(listitems, func=None):
```     
    
```
    """
        fmt_list()

        Return a (str)list of words written in good English, something
        like "a, b, and c" (no Oxford Comma here, confer
        https://www.grammar-monster.com/lessons/commas_the_Oxford_comma.htm)

        If <func> is not None, apply <func> to each item in <listitems>.
        _______________________________________________________________________

        ARGUMENTS:
        o  (list of str)listitems
        o  (callable)   func, the function to be applied to each item in
                        the result.

        RETURNED VALUE: (str)a formatted string with all items in <listitems>.    
```

* if no RETURNED VALUE: don't add a RETURNED VALUE string
* if no ARGUMENT: don't add an ARGUMENT string    

git message: new commit
-----------------------

```
[DONE] task-337

fixed issue #8: in README.md, make it clear that Wisteria can use certain
                types of data.

    * fixed issue #8: in README.md, make it clear that Wisteria can use certain
      types of data.
    
    * tests: 7 tests ok out of 7
    * Pylint: 10/10
```    
    

git message: new version
------------------------
    
v. 0.2.1

* Added another check to checkup(): do all serializers know how to
serialize demonstration_dataobj_a5 ?
* --checkup now display data:lcm, the object data names that can be
(/can't) fully transcoded.


bugfixes:

    * fixed a problem with the console cursor:
      When the program is abruptly stopped, it was possible that the terminal
      cursor did not appear anymore; to solve this problem, when the programs stops,
      the console cursor is shown through a call to .show_cursor(True); this
      function is called in exit_handler().
      (task-292)

code readibility and code quality

    * removed useless space in reports.py .
      (task-297)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

code structure

    * renumbered the error codes, some were duplicates or missing:
      - serializers.py ERRORID051 > ERRORID047
      - wisteria.py ERRORID041 > ERRORID043
      (task-290)

documentation

    * updated documentation: added "(D/04) reset console cursor" string
      to pimydoc "code structure" section.
      (task-292)

interface

    * documentation: improved help message for --verbosity option
      (task-288)

tasks

    * task-322, task-323, task-324, task-325, task-326,
      task-327, task-328, task-329, task-330, task-331,
      task-332   

version

    * set version to '0.2.1'

```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.9.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.16.2 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
|-- colorama >=0.4.0,<0.5.0
|-- commonmark >=0.9.0,<0.10.0
`-- pygments >=2.6.0,<3.0.0
wmi 1.5.1 Windows Management Instrumentation
`-- pywin32 *
```

```
$ check_tools.sh

* about poetry: [...]
```

exit codes
----------

(pimydoc)exit codes
⋅These exit codes try to take into account the standards, in particular this
⋅one: https://docs.python.org/3/library/sys.html#sys.exit
⋅
⋅Please note that `os` constants like `os.EX_OK` as defined in Python doc
⋅(see https://docs.python.org/3/library/os.html#process-management) are not
⋅used for this project; these constants are only defined for Linux systems
⋅and this project aims Windows/OSX systems.
⋅
⋅*    0: normal exit code
⋅*       normal exit code after --checkup
⋅*       normal exit code after --downloadconfigfile
⋅*       normal exit code after --mymachine
⋅*       normal exit code (no data to handle)
⋅*       normal exit code (no serializer to handle)
⋅*    1: error, given config file can't be read (missing or ill-formed file)
⋅*    2: error, ill-formed --cmp string
⋅*    3: error, ill-formed --output string
⋅*    4: error, missing required module
⋅*    5: error: an inconsistency between the data has been detected
⋅*    6: error: can't open/create report file
⋅*  100: internal error, data can't be loaded
⋅*  101: internal error, an error occured while computing the results
⋅*  102: internal error, an error occured in main()
⋅*  103: internal error, can't initialize PLANNED_TRANSCODINGS
*    0: normal exit code
*       normal exit code after --checkup
*       normal exit code after --downloadconfigfile
*       normal exit code after --mymachine
*       normal exit code (no data to handle)
*       normal exit code (no serializer to handle)
*    1: error, given config file can't be read (missing or ill-formed file)
*    2: error, ill-formed --cmp string
*    3: error, ill-formed --output string
*    4: error, missing required module
*    5: error: an inconsistency between the data has been detected
*  100: internal error, data can't be loaded
*  101: internal error, an error occured while computing the results
*  102: internal error, an error occured in main()
*  103: internal error, can't initialize PLANNED_TRANSCODINGS
